import cv2
import matplotlib.pyplot as plt

# خواندن تصویر به صورت خاکستری
I = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
if I is None:
    raise FileNotFoundError("فایل image.png پیدا نشد!")

# نوع 1: تصویر اصلی
plt.subplot(1, 3, 1)
plt.imshow(I, cmap='gray')
plt.title('نوع 1: اصلی')
plt.axis('off')

# نوع 2: تصویر منفی
I_neg = 255 - I
plt.subplot(1, 3, 2)
plt.imshow(I_neg, cmap='gray')
plt.title('نوع 2: منفی')
plt.axis('off')

# نوع 3: تصویر باینری با آستانه Otsu
_, I_bw = cv2.threshold(I, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
plt.subplot(1, 3, 3)
plt.imshow(I_bw, cmap='gray')
plt.title('نوع 3: باینری')
plt.axis('off')

plt.tight_layout()
plt.show()
