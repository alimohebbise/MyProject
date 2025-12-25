#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pill_counter.py

ورودی: مسیر یک تصویر از بلستر قرص (پیش‌فرض: "Ghors (1).jpg")
خروجی: چاپ تعداد قرص های "پر" و "خالی" و ذخیره‌ی تصویر حاشیه‌گذاری‌شده (annotated_output.png)

نیازمندی‌ها:
  pip install opencv-python numpy imutils

نحوه اجرا:
  python pill_counter.py
  یا
  python pill_counter.py --image "مسیر/به/عکس.jpg" --output out.png --debug
"""

import cv2
import numpy as np
import argparse
import imutils
from collections import namedtuple
import os

Result = namedtuple("Result", ["total", "filled", "empty", "annotated_image"])

def detect_and_classify_pills(image, debug=False):
    orig = image.copy()
    # Resize برای پردازش سریع‌تر (حفظ نسبت)
    h, w = image.shape[:2]
    max_dim = 1200
    if max(h, w) > max_dim:
        image = imutils.resize(image, width = int(w * max_dim / max(h, w)))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # کمی بلور برای کم کردن نویز
    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    # آستانه‌بندی تطبیقی برای جدا کردن خانه‌ها/قرص‌ها
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 21, 10)

    # عملیات مورفولوژیک جهت پر کردن حفره‌ها
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # کانتور یابی
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    candidates = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 200:   # حذف نویزهای کوچک (ممکن است مقدار نیاز به تنظیم داشته باشد)
            continue
        perimeter = cv2.arcLength(c, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity < 0.3:
            continue
        candidates.append(c)

    if len(candidates) == 0:
        if debug:
            print("No candidates found with contour approach.")
        return Result(total=0, filled=0, empty=0, annotated_image=orig)

    # برای هر کانتور میانگین مقدار V (روشنایی) را محاسبه می‌کنیم
    means = []
    masks = []
    bboxes = []
    for c in candidates:
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mean_v = cv2.mean(v, mask=mask)[0]
        means.append(mean_v)
        masks.append(mask)
        bboxes.append(cv2.boundingRect(c))

    means_arr = np.array(means, dtype=np.float32).reshape(-1,1)

    # خوشه‌بندی k=2 با OpenCV kmeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
    K = 2
    attempts = 5
    compactness, labels, centers = cv2.kmeans(means_arr, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    labels = labels.flatten()
    centers = centers.flatten()

    # تعیین اینکه کدام خوشه مربوط به "پر" و کدام "خالی" است
    background_mask = cv2.bitwise_not(cv2.bitwise_or.reduce(masks))
    background_mean_v = cv2.mean(v, mask=background_mask)[0] if np.any(background_mask) else np.mean(v)

    dist_to_bg = np.abs(centers - background_mean_v)
    empty_label = int(np.argmin(dist_to_bg))
    filled_label = 1 - empty_label

    filled_count = int(np.sum(labels == filled_label))
    empty_count = int(np.sum(labels == empty_label))
    total = filled_count + empty_count

    # تولید تصویر حاشیه‌گذاری‌شده برای خروجی
    annotated = image.copy()
    for i, c in enumerate(candidates):
        x,y,wc,hc = bboxes[i]
        label = labels[i]
        if label == filled_label:
            color = (0,255,0)   # سبز = پر (باقی مانده)
            text = "filled"
        else:
            color = (0,0,255)   # قرمز = خالی (استفاده شده)
            text = "empty"
        cv2.rectangle(annotated, (x,y), (x+wc, y+hc), color, 2)
        cv2.putText(annotated, text, (x, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    if debug:
        print(f"Detected candidates: {len(candidates)}, total={total}, filled={filled_count}, empty={empty_count}")
        print(f"Cluster centers (mean V): {centers.tolist()}, background mean V={background_mean_v:.1f}")

    return Result(total=total, filled=filled_count, empty=empty_count, annotated_image=annotated)

def main():
    default_image = "Ghors (1).jpg"  # <-- مسیر پیش‌فرض تصویر شما، اینجا قرار گرفته است
    parser = argparse.ArgumentParser(description="Count pills (filled vs empty) in a blister image")
    parser.add_argument("--image", "-i", default=default_image, help="Path to input image (default: %(default)s)")
    parser.add_argument("--output", "-o", default="annotated_output.png", help="Path to save annotated output")
    parser.add_argument("--debug", action="store_true", help="Enable debug prints")
    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print(f"خطا: فایل تصویر پیدا نشد: {args.image}")
        print("لطفاً مطمئن شوید که فایل در همان پوشه است یا مسیر کامل را وارد کنید.")
        return

    img = cv2.imread(args.image)
    if img is None:
        print("Could not read image (cv2.imread returned None):", args.image)
        return

    result = detect_and_classify_pills(img, debug=args.debug)

    print("Total detected positions:", result.total)
    print("Filled (remaining) :", result.filled)
    print("Empty (used)       :", result.empty)

    cv2.imwrite(args.output, result.annotated_image)
    print("Annotated image saved to", args.output)

if __name__ == "__main__":
    main()