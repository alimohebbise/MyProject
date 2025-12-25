import cv2
import numpy as np

# بارگذاری تصویر
img = cv2.imread("pills2.jpg")
if img is None:
    print("❌ تصویر پیدا نشد")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9, 9), 1.5)

# تشخیص دایره‌ها
circles = cv2.HoughCircles(
    blur,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=35,
    param1=100,
    param2=30,
    minRadius=15,
    maxRadius=40
)

count = 0

for x, y, r in circles:
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.circle(mask, (x, y), r-4, 255, -1)
    mean_val = cv2.mean(gray, mask=mask)[0]

    if mean_val > 130:   # اینو بر اساس مرحله قبل تنظیم کن
        count += 1
        color = (0, 255, 0)
    else:
        color = (0, 0, 255)

    cv2.circle(img, (x, y), r, color, 2)

print("✅ تعداد قرص‌های باقی‌مانده:", count)


cv2.imshow("Pill Counter", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
