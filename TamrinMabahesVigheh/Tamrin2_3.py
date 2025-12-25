import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر به صورت خاکستری
img = cv2.imread('eight.tif', cv2.IMREAD_GRAYSCALE)

# بررسی بارگذاری تصویر
if img is None:
    raise ValueError("تصویر eight.tif پیدا نشد!")

# اضافه کردن نویز Salt & Pepper با شدت 0.03
def salt_pepper_noise(image, amount):
    noisy = image.copy()
    h, w = image.shape
    num_pixels = int(amount * h * w)

    # نویز نمک (سفید)
    coords = [np.random.randint(0, i, num_pixels) for i in image.shape]
    noisy[coords[0], coords[1]] = 255

    # نویز فلفل (سیاه)
    coords = [np.random.randint(0, i, num_pixels) for i in image.shape]
    noisy[coords[0], coords[1]] = 0

    return noisy

noisy_img = salt_pepper_noise(img, 0.03)

# فیلتر میانگین 3×3
avg_img = cv2.blur(noisy_img, (3, 3))

# فیلتر میانه 3×3
median_img = cv2.medianBlur(noisy_img, 3)

# فیلتر ماکزیمم 3×3
kernel = np.ones((3, 3), np.uint8)
max_img = cv2.dilate(noisy_img, kernel)

# فیلتر مینیمم 3×3
min_img = cv2.erode(noisy_img, kernel)

# نمایش نتایج
plt.figure(figsize=(12, 6))

plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(noisy_img, cmap='gray')
plt.title('Salt & Pepper Noise (0.03)')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(avg_img, cmap='gray')
plt.title('Average Filter 3×3')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.imshow(median_img, cmap='gray')
plt.title('Median Filter 3×3')
plt.axis('off')

plt.subplot(2, 3, 5)
plt.imshow(max_img, cmap='gray')
plt.title('Max Filter 3×3')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(min_img, cmap='gray')
plt.title('Min Filter 3×3')
plt.axis('off')

plt.tight_layout()
plt.show()
