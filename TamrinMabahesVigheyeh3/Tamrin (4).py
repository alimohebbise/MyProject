import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def load_image():
    # اول تلاش برای باز کردن pout.tif از پوشه جاری
    if os.path.exists("pout.tif"):
        img = cv2.imread("pout.tif", cv2.IMREAD_GRAYSCALE)
    else:
        # اگر نبود، پنجره انتخاب فایل باز شود
        Tk().withdraw()
        file_path = askopenfilename(
            title="تصویر pout.tif را انتخاب کنید",
            filetypes=[("TIF files", "*.tif *.tiff"), ("All files", "*.*")]
        )
        if not file_path:
            print("هیچ فایلی انتخاب نشد!")
            return None
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("خطا در باز کردن تصویر!")
        return None

    return img


def show_images_and_histograms(img, img_eq):
    # هیستوگرام‌ها
    hist_in = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_out = cv2.calcHist([img_eq], [0], None, [256], [0, 256])

    plt.figure(figsize=(12, 8))

    # تصویر ورودی
    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title("تصویر ورودی (pout.tif)")
    plt.axis("off")

    # تصویر خروجی بعد از تعدیل
    plt.subplot(2, 2, 2)
    plt.imshow(img_eq, cmap='gray', vmin=0, vmax=255)
    plt.title("تصویر خروجی (Histogram Equalization)")
    plt.axis("off")

    # هیستوگرام ورودی
    plt.subplot(2, 2, 3)
    plt.plot(hist_in)
    plt.title("هیستوگرام تصویر ورودی")
    plt.xlabel("سطح خاکستری")
    plt.ylabel("تعداد پیکسل")

    # هیستوگرام خروجی
    plt.subplot(2, 2, 4)
    plt.plot(hist_out)
    plt.title("هیستوگرام تصویر خروجی")
    plt.xlabel("سطح خاکستری")
    plt.ylabel("تعداد پیکسل")

    plt.tight_layout()
    plt.show()


# ----------------- main -----------------
img = load_image()
if img is not None:
    # تعدیل هیستوگرام (افزایش کنتراست)
    img_eq = cv2.equalizeHist(img)

    # نمایش تصویر و هیستوگرام‌ها
    show_images_and_histograms(img, img_eq)
