#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pill_counter.py
نسخه بهبود یافته: چند روش تشخیص (HoughCircles، کانتورها، SimpleBlob) و طبقه‌بندی
پیش‌فرض تصویر: "Ghors (1).jpg"

نیازمندی‌ها:
  pip install opencv-python numpy imutils scikit-learn

استفاده:
  python pill_counter.py
  python pill_counter.py --image "Ghors (1).jpg" --output annotated.png --debug
"""
import cv2
import numpy as np
import argparse
import imutils
import os
from sklearn.cluster import KMeans

def resize_max(image, max_dim=1200):
    h, w = image.shape[:2]
    if max(h, w) > max_dim:
        return imutils.resize(image, width = int(w * max_dim / max(h, w)))
    return image

def classify_means(means, method="kmeans"):
    # means: list or np.array از مقادیر روشنایی هر جایگاه
    means = np.array(means).reshape(-1, 1).astype(np.float32)
    if len(means) == 0:
        return [], None
    if len(means) == 1:
        # تنها یک مورد، فرض می‌کنیم پر است
        return [1], np.array([means[0][0]])
    if method == "otsu":
        # آستانه اوتسو روی مقادیر میانگین
        _, th = cv2.threshold(means.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        labels = (means.flatten() > np.mean(means)) .astype(int)  # تقریبی
        centers = np.array([means[labels==0].mean() if np.any(labels==0) else 0,
                            means[labels==1].mean() if np.any(labels==1) else 0])
        return labels.tolist(), centers
    else:
        # kmeans با k=2
        kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(means)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_.flatten()
        return labels.tolist(), centers

def detect_circles_hough(gray, dp=1.2, minDist=30, param1=100, param2=28, minRadius=10, maxRadius=80):
    # برگشت: لیست دایره‌ها (x,y,r)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles is None:
        return []
    circles = np.round(circles[0, :]).astype("int")
    return circles.tolist()

def detect_candidates_by_contours(binimg, min_area=300, circularity_thresh=0.35):
    contours = cv2.findContours(binimg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    candidates = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        perim = cv2.arcLength(c, True)
        if perim == 0:
            continue
        circularity = 4 * np.pi * area / (perim * perim)
        if circularity < circularity_thresh:
            # ممکن است سلول بزرگ‌تر یا شکل نامناسب باشد -> می‌توانیم نگه داریم یا حذف کنیم
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        # تبدیل به مرکز و شعاع تقریبی
        radius = int(0.5 * (w + h) / 2)
        cx = int(x + w/2)
        cy = int(y + h/2)
        candidates.append((cx, cy, radius))
    return candidates

def mask_mean_value(gray_or_v, cx, cy, r):
    mask = np.zeros_like(gray_or_v, dtype=np.uint8)
    cv2.circle(mask, (cx, cy), max(1, int(r*0.9)), 255, -1)
    meanv = cv2.mean(gray_or_v, mask=mask)[0]
    return meanv, mask

def try_hough_and_classify(image, debug=False):
    img = image.copy()
    small = resize_max(img, max_dim=1000)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    # Blur کمتر برای نگه داشتن لبه‌ها
    blurred = cv2.medianBlur(gray, 5)
    # آزمایش پارامترهای مختلف Hough (اولین تلاش)
    circles = detect_circles_hough(blurred, dp=1.2, minDist=25, param1=100, param2=30, minRadius=8, maxRadius=80)
    if debug:
        print(f"Hough found {len(circles)} circles")
    if len(circles) < 4:
        # تلاش دوم با پارامتر کیفی‌تر
        circles = detect_circles_hough(blurred, dp=1.0, minDist=20, param1=50, param2=24, minRadius=6, maxRadius=120)
        if debug:
            print(f"Hough second attempt found {len(circles)} circles")
    if len(circles) == 0:
        return None  # نشد با Hough
    # برای هر دایره میانگین V در HSV یا خاکستری را محاسبه می‌کنیم
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    means = []
    masks = []
    for (x, y, r) in circles:
        meanv, mask = mask_mean_value(v, x, y, r)
        means.append(meanv)
        masks.append((x, y, r, mask))
    labels, centers = classify_means(means, method="kmeans")
    # مشخص کنیم که کدام برچسب = empty (خالی) و کدام filled. معمولاً مرکز روشن‌تر یا تیره‌تر نزدیک به پس‌زمینه
    background_mask = np.ones_like(v, dtype=np.uint8)*255
    for _,_,_,m in masks:
        background_mask = cv2.bitwise_and(background_mask, cv2.bitwise_not(m))
    bg_mean = cv2.mean(v, mask=background_mask)[0] if np.any(background_mask>0) else np.mean(v)
    centers = np.array(centers)
    empty_label = int(np.argmin(np.abs(centers - bg_mean)))
    filled_label = 1 - empty_label
    annotated = small.copy()
    filled_count = 0
    empty_count = 0
    for i, (x,y,r,mask) in enumerate(masks):
        lab = labels[i]
        if lab == filled_label:
            color = (0,255,0); txt = "filled"
            filled_count += 1
        else:
            color = (0,0,255); txt = "empty"
            empty_count += 1
        cv2.circle(annotated, (x,y), r, color, 2)
        cv2.putText(annotated, txt, (x-r, y-r-6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    if debug:
        print("Hough centers:", centers, "bg_mean:", bg_mean)
    return {"annotated": annotated, "total": filled_count+empty_count, "filled": filled_count, "empty": empty_count}

def try_contour_and_classify(image, debug=False):
    img = image.copy()
    small = resize_max(img, max_dim=1200)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    v = hsv[:,:,2]
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    # افزایش کنتراست محلی
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    # آستانه adaptive یا آستانه ثابت با Otsu را امتحان کن
    th_adapt = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 21, 7)
    _, th_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # ترکیب دو تصویر برای پوشش بهتر
    combined = cv2.bitwise_or(th_adapt, th_otsu)
    # مورفولوژی برای پر کردن حفره‌ها و جدا کردن نویز
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    closed = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel, iterations=2)
    # گزینه اضافی: برش مناطق بزرگ با opening
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)
    candidates = detect_candidates_by_contours(opened, min_area=250, circularity_thresh=0.30)
    if debug:
        print(f"Contours-based found {len(candidates)} candidates")
    if len(candidates) == 0:
        return None
    means = []
    info = []
    for (cx,cy,r) in candidates:
        meanv, mask = mask_mean_value(v, cx, cy, r)
        means.append(meanv)
        info.append((cx,cy,r,mask))
    labels, centers = classify_means(means, method="kmeans")
    # تعیین empty/filled بر مبنای فاصله تا پس‌زمینه
    background_mask = np.ones_like(v, dtype=np.uint8)*255
    for _,_,_,m in info:
        background_mask = cv2.bitwise_and(background_mask, cv2.bitwise_not(m))
    bg_mean = cv2.mean(v, mask=background_mask)[0] if np.any(background_mask>0) else np.mean(v)
    centers = np.array(centers)
    empty_label = int(np.argmin(np.abs(centers - bg_mean)))
    filled_label = 1 - empty_label
    annotated = small.copy()
    filled_count = 0
    empty_count = 0
    for i, (cx,cy,r,mask) in enumerate(info):
        lab = labels[i]
        if lab == filled_label:
            color = (0,255,0); txt = "filled"; filled_count += 1
        else:
            color = (0,0,255); txt = "empty"; empty_count += 1
        cv2.circle(annotated, (cx,cy), max(4, int(r)), color, 2)
        cv2.putText(annotated, txt, (cx-int(r), cy-int(r)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
    if debug:
        print("Contour centers:", centers, "bg_mean:", bg_mean)
    return {"annotated": annotated, "total": filled_count+empty_count, "filled": filled_count, "empty": empty_count}

def detect_and_classify(image, debug=False):
    # ابتدا با Hough تلاش کن (برای قرص‌های دایره‌ای یا خانه‌های گرد بلستر خوب است)
    res = try_hough_and_classify(image, debug=debug)
    if res is not None and res["total"] >= 4:
        if debug:
            print("Using Hough result")
        return res
    # fallback: کانتورها و مورفولوژی (برای بلسترهای منظم)
    res = try_contour_and_classify(image, debug=debug)
    if res is not None and res["total"] >= 4:
        if debug:
            print("Using contour result")
        return res
    # تلاش نهایی: کاهش محدودیت‌ها و دوباره امتحان کردن کانتورها
    if debug:
        print("Fallback: trying relaxed contour params")
    # تغییر پارامترها با اعمال blur متفاوت
    img = resize_max(image, max_dim=1200)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (9,9), 0)
    _, th = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=3)
    candidates = detect_candidates_by_contours(closed, min_area=150, circularity_thresh=0.22)
    if len(candidates) == 0:
        # واقعاً هیچ چیزی پیدا نشد
        if debug:
            print("No candidates found in any method.")
        return {"annotated": img, "total": 0, "filled": 0, "empty": 0}
    # طبقه‌بندی مثل قبل
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:,:,2]
    means = []
    info = []
    for (cx,cy,r) in candidates:
        meanv, mask = mask_mean_value(v, cx, cy, r)
        means.append(meanv)
        info.append((cx,cy,r,mask))
    labels, centers = classify_means(means, method="kmeans")
    bg_mask = np.ones_like(v, dtype=np.uint8)*255
    for _,_,_,m in info:
        bg_mask = cv2.bitwise_and(bg_mask, cv2.bitwise_not(m))
    bg_mean = cv2.mean(v, mask=bg_mask)[0] if np.any(bg_mask>0) else np.mean(v)
    centers = np.array(centers)
    empty_label = int(np.argmin(np.abs(centers - bg_mean)))
    filled_label = 1 - empty_label
    annotated = img.copy()
    filled_count = 0
    empty_count = 0
    for i, (cx,cy,r,mask) in enumerate(info):
        lab = labels[i]
        if lab == filled_label:
            color=(0,255,0); txt="filled"; filled_count+=1
        else:
            color=(0,0,255); txt="empty"; empty_count+=1
        cv2.circle(annotated, (cx,cy), max(4,int(r)), color, 2)
        cv2.putText(annotated, txt, (cx-int(r), cy-int(r)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
    return {"annotated": annotated, "total": filled_count+empty_count, "filled": filled_count, "empty": empty_count}

def main():
    parser = argparse.ArgumentParser(description="Count pills (filled vs empty) in a blister/image")
    parser.add_argument("--image", "-i", default="Ghors (5).jpg", help="Path to input image (default: %(default)s)")
    parser.add_argument("--output", "-o", default="annotated_output.png", help="Path to save annotated output")
    parser.add_argument("--debug", action="store_true", help="Enable debug prints and save intermediate images")
    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print("خطا: فایل تصویر پیدا نشد:", args.image)
        return

    img = cv2.imread(args.image)
    if img is None:
        print("خطا: نمیتوان تصویر را خواند (cv2.imread برگشت None). مطمئن شوید فرمت پشتیبانی‌شده است.")
        return

    result = detect_and_classify(img, debug=args.debug)

    print("Total detected positions:", result["total"])
    print("Filled (remaining) :", result["filled"])
    print("Empty (used)       :", result["empty"])

    cv2.imwrite(args.output, result["annotated"])
    print("Annotated image saved to", args.output)

if __name__ == "__main__":
    main()