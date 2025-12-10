import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# ------------------ بارگذاری تصویر ------------------
def load_image():
    if os.path.exists("pout.tif"):
        img = cv2.imread("pout.tif", cv2.IMREAD_GRAYSCALE)
    else:
        Tk().withdraw()
        path = askopenfilename(
            title="تصویر pout.tif را انتخاب کنید",
            filetypes=[("TIF files", "*.tif *.tiff"), ("All files", "*.*")]
        )
        if not path:
            print("هیچ تصویری انتخاب نشد!")
            return None
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("خطا در بارگذاری تصویر!")
        return None

    return img


# ------------------ ساخت هیستوگرام گوسی هدف ------------------
def gaussian_histogram(mu=70, sigma=30):
    x = np.arange(256)
    g = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    # نرمال‌سازی برای تبدیل به PDF
    g = g / np.sum(g)

    return g


# ------------------ تطبیق هیستوگرام ------------------
def histogram_matching(img, target_pdf):
    # هیستوگرام تصویر ورودی
    hist = cv2.calcHist([img], [0], None, [256], [0, 256]).ravel()
    hist = hist / hist.sum()   # PDF ورودی

    # CDF ورودی و CDF هدف
    cdf_input = np.cumsum(hist)
    cdf_target = np.cumsum(target_pdf)

    # جدول نگاشت (Mapping Function)
    mapping = np.zeros(256, dtype=np.uint8)

    for i in range(256):
        diff = np.abs(cdf_input[i] - cdf_target)
        mapping[i] = np.argmin(diff)

    # اعمال نگاشت روی تصویر
    matched_img = mapping[img]

    return matched_img


# ------------------ رسم تصاویر و هیستوگرام‌ها ------------------
def show_all(img, img_out, target_pdf):
    hist_in = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_out = cv2.calcHist([img_out], [0], None, [256], [0, 256])

    plt.figure(figsize=(14, 10))

    # تصویر ورودی
    plt.subplot(2, 3, 1)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title("تصویر ورودی (pout.tif)")
    plt.axis("off")

    # تصویر خروجی
    plt.subplot(2, 3, 2)
    plt.imshow(img_out, cmap='gray', vmin=0, vmax=255)
    plt.title("تصویر خروجی (Histogram Matching)")
    plt.axis("off")

    # هیستوگرام ورودی
    plt.subplot(2, 3, 4)
    plt.plot(hist_in)
    plt.title("هیستوگرام ورودی")
    plt.xlabel("سطح خاکستری")
    plt.ylabel("تعداد پیکسل")

    # هیستوگرام خروجی
    plt.subplot(2, 3, 5)
    plt.plot(hist_out)
    plt.title("هیستوگرام خروجی")
    plt.xlabel("سطح خاکستری")
    plt.ylabel("تعداد پیکسل")

    # هیستوگرام گوسی هدف
    plt.subplot(2, 3, 6)
    plt.plot(target_pdf)
    plt.title("هیستوگرام گوسی هدف\nμ=70 , σ=30")
    plt.xlabel("سطح خاکستری")
    plt.ylabel("چگالی احتمال")

    plt.tight_layout()
    plt.show()


# ------------------ main ------------------
img = load_image()

if img is not None:
    target_pdf = gaussian_histogram(mu=70, sigma=30)
    img_matched = histogram_matching(img, target_pdf)
    show_all(img, img_matched, target_pdf)
