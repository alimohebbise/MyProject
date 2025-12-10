# --- بخش 1: توابع کمکی و تعمیر تصویر ---
import os
import sys
from io import BytesIO
from typing import Optional, List, Tuple

# نیاز به Pillow، OpenCV، numpy داریم
# نصب در صورت نیاز:
# pip install pillow opencv-python numpy matplotlib

from PIL import Image

def read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def write_file_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)

def detect_image_type_from_bytes(b: bytes) -> Optional[str]:
    """تعیین نوع تصویر با استفاده از Pillow (به جای imghdr)."""
    try:
        with Image.open(BytesIO(b)) as img:
            return img.format.lower()
    except Exception:
        return None

# ----------------------------
# روش 1: تلاش ساده با Pillow و OpenCV
# ----------------------------
def try_open_with_pillow_bytes(b: bytes):
    from PIL import UnidentifiedImageError
    try:
        img = Image.open(BytesIO(b))
        img.verify()  # فقط اعتبارسنجی
        img = Image.open(BytesIO(b)).convert("RGB")
        return img
    except UnidentifiedImageError:
        return None
    except Exception:
        return None

def try_open_with_opencv_bytes(b: bytes):
    try:
        import numpy as np
        import cv2
    except Exception:
        return None
    arr = np.frombuffer(b, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    try:
        if img.ndim == 2:
            return Image.fromarray(img)
        elif img.shape[2] == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(img_rgb)
        elif img.shape[2] == 4:
            img_rgba = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            return Image.fromarray(img_rgba)
    except Exception:
        return None

# ----------------------------
# روش 2: استخراج بخش‌های JPEG از بین مارکرها
# ----------------------------
def find_jpeg_ranges(b: bytes) -> List[Tuple[int,int]]:
    starts, ends, ranges = [], [], []
    L = len(b)
    i = 0
    while i < L - 1:
        if b[i] == 0xFF and b[i+1] == 0xD8:
            starts.append(i)
            i += 2
        elif b[i] == 0xFF and b[i+1] == 0xD9:
            ends.append(i + 2)
            i += 2
        else:
            i += 1
    for s in starts:
        e_candidates = [e for e in ends if e > s]
        if e_candidates:
            ranges.append((s, e_candidates[0]))
    return ranges

def extract_jpeg_candidates(b: bytes) -> List[bytes]:
    return [b[s:e] for s, e in find_jpeg_ranges(b)]

# ----------------------------
# روش 3: افزودن هدر ساده به JPEG ناقص
# ----------------------------
def prepend_minimal_jpeg_header(b: bytes) -> bytes:
    jfif_header = bytes.fromhex(
        "FFD8" "FFE00010" "4A46494600" "0101" "00" "0001" "0001" "00" "00"
    )
    return jfif_header + b

# ----------------------------
# روش 4: استخراج تصاویر PNG از داده‌ها
# ----------------------------
def find_png_ranges(b: bytes) -> List[Tuple[int,int]]:
    sig = b'\x89PNG\r\n\x1a\n'
    ranges, i, L = [], 0, len(b)
    while True:
        idx = b.find(sig, i)
        if idx == -1:
            break
        iend = b.find(b'IEND', idx)
        if iend != -1:
            end_candidate = iend + 8
            ranges.append((idx, end_candidate))
            i = end_candidate
        else:
            ranges.append((idx, L))
            break
    return ranges

def extract_png_candidates(b: bytes) -> List[bytes]:
    return [b[s:e] for s, e in find_png_ranges(b)]

# --- بخش 2: اجرای اصلی و نمایش ---
import argparse
from pathlib import Path
from PIL import Image

def try_all_strategies(path: str, out_dir: Optional[str] = None):
    b = read_file_bytes(path)
    basename = Path(path).stem
    out_dir = Path(out_dir or Path(path).parent)
    out_dir.mkdir(parents=True, exist_ok=True)

    guess = detect_image_type_from_bytes(b)
    if guess:
        print(f"📷 فرمت احتمالی فایل: {guess}")

    # 1) امتحان با Pillow
    img = try_open_with_pillow_bytes(b)
    if img:
        out = out_dir / f"{basename}_pillow.jpg"
        img.save(out)
        return {"method": "pillow", "path": str(out)}

    # 2) امتحان با OpenCV
    img = try_open_with_opencv_bytes(b)
    if img:
        out = out_dir / f"{basename}_opencv.jpg"
        img.save(out)
        return {"method": "opencv", "path": str(out)}

    # 3) استخراج JPEG
    for i, cand in enumerate(extract_jpeg_candidates(b)):
        img = try_open_with_pillow_bytes(cand)
        if img:
            out = out_dir / f"{basename}_extract_{i}.jpg"
            img.save(out)
            return {"method": f"jpeg_extract_{i}", "path": str(out)}

    # 4) افزودن هدر به JPEG ناقص
    img = try_open_with_pillow_bytes(prepend_minimal_jpeg_header(b))
    if img:
        out = out_dir / f"{basename}_fixed_header.jpg"
        img.save(out)
        return {"method": "jpeg_fixed_header", "path": str(out)}

    # 5) استخراج PNG
    for i, cand in enumerate(extract_png_candidates(b)):
        img = try_open_with_pillow_bytes(cand)
        if img:
            out = out_dir / f"{basename}_png_{i}.png"
            img.save(out)
            return {"method": f"png_extract_{i}", "path": str(out)}

    # 6) جستجوی offsetهای ممکن
    L = len(b)
    for offset in range(0, min(4096, L//2), 16):
        img = try_open_with_pillow_bytes(b[offset:])
        if img:
            out = out_dir / f"{basename}_offset_{offset}.jpg"
            img.save(out)
            return {"method": f"offset_{offset}", "path": str(out)}

    return {"method": "failed", "reason": "هیچ روش موفق نشد"}

def show_image_with_default_viewer(path: str):
    try:
        Image.open(path).show()
    except Exception as e:
        print("❌ خطا در نمایش تصویر:", e)

def main_cli():
    parser = argparse.ArgumentParser(description="نمایش تصویر ریکاوری‌شده (در صورت امکان)")
    parser.add_argument("input", help="مسیر فایل آسیب‌دیده یا ریکاوری‌شده")
    parser.add_argument("--outdir", "-o", default=None, help="پوشه ذخیره خروجی")
    args = parser.parse_args()

    result = try_all_strategies(args.input, args.outdir)
    if result["method"] == "failed":
        print("❌ متاسفم، تصویر باز نشد.")
        print("💡 احتمالاً فایل واقعاً ناقص یا غیرتصویری است.")
        sys.exit(1)
    else:
        print(f"✅ موفقیت با روش: {result['method']}")
        print(f"📁 فایل ذخیره‌شده در: {result['path']}")
        show_image_with_default_viewer(result["path"])

if __name__ == "__main__":
    main_cli()
