import cv2
import numpy as np

# خواندن تصویر
img = cv2.imread("rice.png", cv2.IMREAD_GRAYSCALE)

# اگر فایل پیدا نشود
if img is None:
    print("تصویر rice.png پیدا نشد!")
    exit()

# تبدیل به آرایه NumPy
pixels = img.astype(np.float64)

# میانگین
mean_val = np.mean(pixels)

# واریانس
var_val = np.var(pixels)

# انحراف معیار
std_val = np.std(pixels)

print("میانگین شدت روشنایی:", mean_val)
print("واریانس:", var_val)
print("انحراف معیار:", std_val)
