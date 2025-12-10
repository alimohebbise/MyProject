#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نمایش هشت صفحه بیتی (bit-planes) تصویر
نحوه اجرا: python show_bitplanes.py path/to/dollar.jpg
"""

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_bit_planes(img.png):
    # خواندن تصویر (BGR)
    img = cv2.imread('img.png')
    if img is None:
        print("نمی‌توان تصویر را باز کرد. مسیر را بررسی کنید:", 'img.png')
        return

    # تبدیل به خاکستری
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # آماده‌سازی شکل نمایش: 2 ردیف × 4 ستون
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    fig.suptitle('هشت صفحه بیتی تصویر (bit-planes)', fontsize=16)

    # استخراج و نمایش هر صفحه بیتی
    for i in range(8):
        # شیفت به راست و ماسک کردن بیت کم ارزش
        bit_plane = ((gray >> i) & 1) * 255  # 0 یا 255 برای نمایش واضح
        r = i // 4
        c = i % 4
        ax = axes[r, c]
        ax.imshow(bit_plane, cmap='gray', vmin=0, vmax=255)
        ax.set_title(f'Bit plane {i} (2^{i})')
        ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # (اختیاری) بازسازی تصویر فقط از بیت‌های مهم (مثال: بیت‌های 7 تا 4)
    recon = np.zeros_like(gray, dtype=np.uint8)
    for i in range(4, 8):  # بیت‌های 4،5،6،7
        recon += ((gray >> i) & 1) << i
    plt.figure(figsize=(6,6))
    plt.imshow(recon, cmap='gray', vmin=0, vmax=255)
    plt.title('بازسازی از بیت‌های 7..4 (مثال)')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python show_bitplanes.py path/to/image.jpg")
    else:
        show_bit_planes(sys.argv[1])
