import cv2
import numpy as np

# بارگذاری تصویر
image_path = 'Daneh02.png'  # مسیر تصویر خود را وارد کنید
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # بارگذاری به صورت خاکستری

# بررسی اینکه آیا تصویر به درستی بارگذاری شده است یا خیر
if image is None:
    print("خطا: تصویر بارگذاری نشد.")
    exit()

# محاسبه میانگین شدت پیکسل‌ها
mean_threshold = np.mean(image)

# آستانه‌گذاری تصویر
_, thresholded_image = cv2.threshold(image, mean_threshold, 255, cv2.THRESH_BINARY)

# نمایش تصویر اصلی و تصویر آستانه‌گذاری شده
cv2.imshow('Original Image', image)
cv2.imshow('Thresholded Image', thresholded_image)

# انتظار برای کلید ورودی و بستن پنجره‌ها
cv2.waitKey(0)
cv2.destroyAllWindows()

# ذخیره تصویر آستانه‌گذاری شده
cv2.imwrite('thresholded_image.jpg', thresholded_image)