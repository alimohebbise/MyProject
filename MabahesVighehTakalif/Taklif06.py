import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر
image = cv2.imread('Jozeiat02.png', cv2.IMREAD_GRAYSCALE)

# محاسبه میانگین تصویر
mean_value = np.mean(image)

# آستانه‌گذاری با مقدار میانگین
_, thresholded_image = cv2.threshold(image, mean_value, 255, cv2.THRESH_BINARY)

# تبدیل گاما
c = 1  # پارامتر c
gamma_corrected_image = np.power(thresholded_image / 255.0, c) * 255.0
gamma_corrected_image = gamma_corrected_image.astype(np.uint8)

# نمایش تصاویر
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Thresholded Image')
plt.imshow(thresholded_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Gamma Corrected Image')
plt.imshow(gamma_corrected_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()