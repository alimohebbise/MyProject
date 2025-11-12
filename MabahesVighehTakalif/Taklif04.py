import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر tire.tif
img = cv2.imread("tire.tif", cv2.IMREAD_GRAYSCALE)

if img is None:
    print("فایل tire.tif پیدا نشد!")
    exit()

# تبدیل به float
f = img.astype(np.float64)

# مقادیر c
c_values = [1, 2, 3, 4, 5]

plt.figure(figsize=(12, 8))

# نمایش تصویر اصلی
plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.axis("off")

# اعمال تبدیل لگاریتمی
for i, c in enumerate(c_values, start=2):
    log_img = c * np.log(1 + f)

    # نرمال سازی به 0 تا 255
    log_img = 255 * (log_img / np.max(log_img))
    log_img = log_img.astype(np.uint8)

    plt.subplot(2, 3, i)
    plt.imshow(log_img, cmap='gray')
    plt.title(f"c = {c}")
    plt.axis("off")

plt.tight_layout()
plt.show()
