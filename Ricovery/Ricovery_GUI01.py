import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from io import BytesIO
from pathlib import Path
import numpy as np
import cv2

# ----------- توابع کمکی -----------
def read_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()

def detect_image_type_from_bytes(b):
    try:
        with Image.open(BytesIO(b)) as img:
            return img.format.lower()
    except Exception:
        return None

def try_open_with_pillow_bytes(b):
    try:
        img = Image.open(BytesIO(b))
        img.verify()
        img = Image.open(BytesIO(b)).convert("RGB")
        return img
    except Exception:
        return None

def try_open_with_opencv_bytes(b):
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

def find_jpeg_ranges(b):
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

def extract_jpeg_candidates(b):
    return [b[s:e] for s, e in find_jpeg_ranges(b)]

def prepend_minimal_jpeg_header(b):
    jfif_header = bytes.fromhex(
        "FFD8" "FFE00010" "4A46494600" "0101" "00" "0001" "0001" "00" "00"
    )
    return jfif_header + b

def find_png_ranges(b):
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

def extract_png_candidates(b):
    return [b[s:e] for s, e in find_png_ranges(b)]

# ----------- منطق اصلی تعمیر -----------
def repair_image(path):
    b = read_file_bytes(path)
    guess = detect_image_type_from_bytes(b)

    img = try_open_with_pillow_bytes(b)
    if img:
        return img, "Pillow", guess

    img = try_open_with_opencv_bytes(b)
    if img:
        return img, "OpenCV", guess

    for i, cand in enumerate(extract_jpeg_candidates(b)):
        img = try_open_with_pillow_bytes(cand)
        if img:
            return img, f"JPEG Extract {i}", guess

    img = try_open_with_pillow_bytes(prepend_minimal_jpeg_header(b))
    if img:
        return img, "Prepended Header", guess

    for i, cand in enumerate(extract_png_candidates(b)):
        img = try_open_with_pillow_bytes(cand)
        if img:
            return img, f"PNG Extract {i}", guess

    # تلاش آخر با offset
    L = len(b)
    for offset in range(0, min(4096, L//2), 16):
        img = try_open_with_pillow_bytes(b[offset:])
        if img:
            return img, f"Offset {offset}", guess

    return None, None, guess

# ----------- رابط گرافیکی (GUI) -----------
class RecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🩵 بازیابی و نمایش تصویر ریکاوری‌شده")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f4ff")

        tk.Label(root, text="برنامه‌ی بازیابی تصویر خراب یا ریکاوری‌شده",
                 bg="#f0f4ff", fg="#002366", font=("B Nazanin", 16, "bold")).pack(pady=10)

        tk.Button(root, text="📂 انتخاب فایل تصویری", font=("B Nazanin", 13),
                  command=self.choose_file, bg="#b3c6ff", relief="raised").pack(pady=10)

        self.info_label = tk.Label(root, text="", bg="#f0f4ff", fg="#333", font=("B Nazanin", 12))
        self.info_label.pack(pady=5)

        self.canvas = tk.Label(root, bg="#fff", width=600, height=400, relief="solid", bd=1)
        self.canvas.pack(pady=10)

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="انتخاب فایل تصویری",
            filetypes=[("All files", "*.*")]
        )
        if not path:
            return

        self.info_label.config(text="در حال تلاش برای تعمیر تصویر...")
        self.root.update_idletasks()

        img, method, guess = repair_image(path)
        if img is None:
            messagebox.showerror("❌ شکست", "متأسفانه نتوانستم تصویر را بازیابی کنم.")
            self.info_label.config(text="نتیجه: شکست")
            return

        # نمایش اطلاعات
        info_text = f"✅ موفقیت با روش: {method}"
        if guess:
            info_text += f" | فرمت احتمالی: {guess.upper()}"
        self.info_label.config(text=info_text)

        # تغییر اندازه تصویر برای نمایش در صفحه
        img_display = img.copy()
        img_display.thumbnail((600, 400))
        self.tk_img = ImageTk.PhotoImage(img_display)
        self.canvas.config(image=self.tk_img)

        # محل ذخیره در خود پوشه برنامه
        base_dir = Path(__file__).parent
        out_path = base_dir / "recovered_fixed.png"
        img.save(out_path)

        messagebox.showinfo("✔ موفقیت", f"تصویر در پوشه‌ی برنامه ذخیره شد:\n{out_path}")

# ----------- اجرای برنامه -----------
if __name__ == "__main__":
    root = tk.Tk()
    app = RecoveryApp(root)
    root.mainloop()
