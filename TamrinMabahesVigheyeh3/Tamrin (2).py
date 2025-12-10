#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بارگذاری تصویر tire.tif و رسم هیستوگرام و PDF (تابع چگالی احتمال)
نحوه اجرا:
    python tire_hist_pdf.py
یا
    python tire_hist_pdf.py path/to/tire.tif
"""

import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_image(path=None):
    # اگر مسیر داده شده و فایل وجود داشت از آن استفاده کن
    if path and os.path.exists(path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    else:
        # سعی کن فایل پیش‌فرض را از پوشهٔ جاری باز کنی
        default = "tire.tif"
        if os.path.exists(default):
            img = cv2.imread(default, cv2.IMREAD_UNCHANGED)
        else:
            # پنجره انتخاب فایل برای کاربر باز شود
            Tk().withdraw()
            file_path = askopenfilename(
                title="انتخاب تصویر (tire.tif یا هر تصویر)",
                filetypes=[("Image files", "*.tif *.tiff *.png *.jpg *.bmp"), ("All files", "*.*")]
            )
            if not file_path:
                print("هیچ فایلی انتخاب نشد. خروج.")
                return None
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print("نشد تصویر را باز کرد — مسیر/فرمت را بررسی کن.")
        return None

    # اگر تصویر رنگی است، تبدیل به خاکستری کن
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    return gray

def plot_hist_and_pdf(gray, bins=256, title_prefix="tire.tif"):
    # هیستوگرام: counts و لبه‌ها
    counts, bin_edges = np.histogram(gray.flatten(), bins=bins, range=(0, 256))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # PDF: نرمال‌سازی تا مجموع فضا = 1 (یا مساحت زیر منحنی = 1)
    pdf = counts.astype(np.float64) / counts.sum()
    # اگر می‌خواهیم PDF به صورت تابع چگالی بر حسب شدت و با مساحت 1 باشه:
    # برای bins مساوی، pdf_area_normalized = counts / (N * bin_width)  => bin_width = 1 برای 0..255 با 256 بین
    bin_width = bin_edges[1] - bin_edges[0]
    pdf_area_normalized = counts.astype(np.float64) / (counts.sum() * bin_width)

    # رسم
    plt.figure(figsize=(12,5))

    # نمایش تصویر خاکستری سمت چپ
    plt.subplot(1,3,1)
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.title(f"{title_prefix} (Gray)")
    plt.axis('off')

    # هیستوگرام (تعداد پیکسل‌ها) وسط
    plt.subplot(1,3,2)
    plt.bar(bin_centers, counts, width=bin_width, align='center')
    plt.title("Histogram (counts)")
    plt.xlabel("Intensity")
    plt.ylabel("Number of pixels")
    plt.xlim(0,255)

    # PDF سمت راست (مساحت نرمال شده = 1)
    plt.subplot(1,3,3)
    plt.plot(bin_centers, pdf_area_normalized, lw=1.5)
    plt.fill_between(bin_centers, pdf_area_normalized, alpha=0.2)
    plt.title("PDF (probability density function, area=1)")
    plt.xlabel("Intensity")
    plt.ylabel("Probability density")
    plt.xlim(0,255)

    plt.tight_layout()
    plt.show()

    # (اختیاری) نمایش PDF به صورت احتمال (sum=1) نیز چاپ می‌کنیم:
    print("Sum of pdf (probabilities per bin):", np.round(pdf.sum(), 8))
    print("Integral (area) of area-normalized pdf:", np.round(pdf_area_normalized.sum() * bin_width, 8))

if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    gray_img = load_image(path_arg)
    if gray_img is not None:
        plot_hist_and_pdf(gray_img, bins=256, title_prefix=(path_arg if path_arg else "tire.tif"))
