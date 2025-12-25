import cv2
import numpy as np
import matplotlib.pyplot as plt

# ---------- 1- خواندن تصویر ----------
img = cv2.imread('eight.tif', cv2.IMREAD_GRAYSCALE)

# ---------- 2- افزودن نویز Salt & Pepper ----------
def salt_pepper_noise(image, amount):
    noisy = image.copy()
    h, w = image.shape
    num_noise = int(amount * h * w)

    # Salt
    coords = [np.random.randint(0, i, num_noise) for i in image.shape]
    noisy[coords[0], coords[1]] = 255

    # Pepper
    coords = [np.random.randint(0, i, num_noise) for i in image.shape]
    noisy[coords[0], coords[1]] = 0

    return noisy

noisy_img = salt_pepper_noise(img, 0.03)

# ---------- اندازه فیلترها ----------
filter_sizes = [3, 5, 7]

for k in filter_sizes:

    # ---------- 3- فیلتر میانگین ----------
    avg = cv2.blur(noisy_img, (k, k))

    # ---------- 4- فیلتر میانه ----------
    median = cv2.medianBlur(noisy_img, k)

    # ---------- 5- فیلتر ماکزیمم ----------
    kernel = np.ones((k, k), np.uint8)
    max_filter = cv2.dilate(noisy_img, kernel)

    # ---------- 6- فیلتر مینیمم ----------
    min_filter = cv2.erode(noisy_img, kernel)

    # ---------- نمایش ----------
    plt.figure(figsize=(10, 6))
    plt.suptitle(f'Filter Size {k}x{k}', fontsize=14)

    plt.subplot(2, 3, 1)
    plt.imshow(noisy_img, cmap='gray')
    plt.title('Noisy Image')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(avg, cmap='gray')
    plt.title('Average Filter')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(median, cmap='gray')
    plt.title('Median Filter')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(max_filter, cmap='gray')
    plt.title('Max Filter')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(min_filter, cmap='gray')
    plt.title('Min Filter')
    plt.axis('off')

    plt.show()
