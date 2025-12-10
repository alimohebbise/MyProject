import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def show_bit_planes(img_path):
    # خواندن تصویر
    img = cv2.imread(img_path)
    if img is None:
        print("خطا در خواندن تصویر!")
        return

    # تبدیل به خاکستری
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ساخت صفحه نمایش 8 تایی
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    fig.suptitle("هشت صفحه بیتی تصویر", fontsize=16)

    for i in range(8):
        bit_plane = ((gray >> i) & 1) * 255
        r = i // 4
        c = i % 4

        axes[r, c].imshow(bit_plane, cmap="gray")
        axes[r, c].set_title(f"Bit {i}")
        axes[r, c].axis("off")

    plt.tight_layout()
    plt.show()


# ---------- انتخاب فایل از داخل ویندوز ----------
Tk().withdraw()  # مخفی کردن پنجره اصلی
file_path = askopenfilename(
    title="یک تصویر انتخاب کنید",
    filetypes=[
        ("Image files", "*.jpg *.png *.bmp *.jpeg"),
        ("All files", "*.*")
    ]
)

# اگر کاربر فایلی انتخاب کرد
if file_path:
    show_bit_planes(file_path)
else:
    print("هیچ عکسی انتخاب نشد!")
