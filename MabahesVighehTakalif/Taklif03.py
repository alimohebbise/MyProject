import cv2
import numpy as np

# خواندن تصویر
img = cv2.imread("xray.png", cv2.IMREAD_GRAYSCALE)

# اگر پیدا نشود
if img is None:
    print("فایل xray.png پیدا نشد!")
    exit()

# نگاتیو تصویر
negative = 255 - img

# نمایش
cv2.imshow("Original Image", img)
cv2.imshow("Negative Image", negative)

cv2.waitKey(0)
cv2.destroyAllWindows()
