# TashkhisGhorsOPT.py
# نسخه‌ای که هم positional و هم --image را می‌پذیرد

import cv2
import numpy as np
import argparse
import sys

def detect_pills(image_path, thresh=100, visualize_out=None, debug=False):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"تصویر یافت نشد: {image_path}")

    orig = img.copy()
    scale = 800.0 / max(img.shape[:2])
    if scale < 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    circles = cv2.HoughCircles(
        gray_blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=28,
        minRadius=12,
        maxRadius=60
    )

    if circles is None:
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 10000
        params.filterByCircularity = True
        params.minCircularity = 0.6
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gray_blur)
        circles_list = []
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            r = int(np.sqrt(kp.size / np.pi))
            circles_list.append((x, y, r))
    else:
        circles = np.round(circles[0, :]).astype("int")
        circles_list = [(int(x), int(y), int(r)) for (x, y, r) in circles]

    results = []
    for (x, y, r) in circles_list:
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), max(r - 2, 1), 255, -1)
        mean_val = cv2.mean(gray, mask=mask)[0]
        present = mean_val > thresh
        results.append({
            'x': x, 'y': y, 'r': r,
            'mean_intensity': mean_val,
            'present': present
        })

    total = len(results)
    present_count = sum(1 for r in results if r['present'])
    empty_count = total - present_count

    vis = img.copy()
    for res in results:
        color = (0, 255, 0) if res['present'] else (0, 0, 255)
        cv2.circle(vis, (res['x'], res['y']), res['r'], color, 2)
        if debug:
            cv2.putText(vis, f"{int(res['mean_intensity'])}", (res['x']-10, res['y']),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,0), 1)

    if visualize_out:
        cv2.imwrite(visualize_out, vis)

    return {
        'total_slots': total,
        'present': present_count,
        'empty': empty_count,
        'details': results,
        'visualization_image': visualize_out
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect how many pills used/remaining in a blister.")
    # قبول هم positional و هم --image/-i
    parser.add_argument("image", nargs="?", help="Path to input image (positional)")
    parser.add_argument("--image", "-i", dest="image_opt", help="Path to input image (optional flag)")
    parser.add_argument("--threshold", type=int, default=100, help="Intensity threshold to decide present/empty")
    parser.add_argument("--out", default="out.jpg", help="Visualization output image")
    parser.add_argument("--debug", action="store_true", help="Draw debug info")
    args = parser.parse_args()

    # انتخاب تصویر: اگر positional داده شده استفاده کن، در غیر اینصورت از --image استفاده کن
    image_path = args.image if args.image else args.image_opt
    if not image_path:
        parser.print_help()
        print("\nخطا: مسیر تصویر وارد نشده. از یکی از شیوه‌های زیر استفاده کنید:")
        print("  python TashkhisGhorsOPT.py path/to/image.jpg")
        print("  python TashkhisGhorsOPT.py --image path/to/image.jpg")
        sys.exit(1)

    try:
        res = detect_pills(image_path, thresh=args.threshold, visualize_out=args.out, debug=args.debug)
        print(f"Total slots: {res['total_slots']}")
        print(f"Present (not used): {res['present']}")
        print(f"Empty (used): {res['empty']}")
        if res['visualization_image']:
            print(f"Visualization saved to {res['visualization_image']}")
    except Exception as e:
        print("خطا در پردازش تصویر:", e)
        sys.exit(1)