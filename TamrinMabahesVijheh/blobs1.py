import cv2
import matplotlib.pyplot as plt

# خواندن تصویر به صورت خاکستری (grayscale)
Igray = cv2.imread('blobs.png', cv2.IMREAD_GRAYSCALE)
if Igray is None:
    raise FileNotFoundError("فایل blobs.png پیدا نشد. آن را در همان پوشه قرار دهید.")

# نوع 1: نمایش خاکستری
plt.figure(figsize=(6,6))
plt.imshow(Igray, cmap='gray')
plt.title('نوع 1: تصویر خاکستری')
plt.axis('off')

# نوع 3: بایناریزه با آستانه Otsu
# OpenCV Otsu expects 0..255 uint8 image
_, Ibw = cv2.threshold(Igray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

plt.figure(figsize=(6,6))
plt.imshow(Ibw, cmap='gray')
plt.title(f'نوع 3: تصویر باینری (Otsu, level={_})')
plt.axis('off')

plt.show()
