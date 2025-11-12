import cv2
import numpy as np

# بارگذاری تصویر
image_path = 'Jozeiat.png'  # مسیر تصویر خود را وارد کنید
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # بارگذاری به صورت خاکستری

# بررسی اینکه آیا تصویر به درستی بارگذاری شده است یا خیر
if image is None:
    print("خطا: تصویر بارگذاری نشد.")
    exit()

# تبدیل گاما
c = 1  # ثابت
gamma = 2.0  # مقدار گاما برای تقویت جزئیات

# محاسبه LUT (جدول جستجو) برای تبدیل گاما
lookup_table = np.array([(c * (i / 255.0) ** gamma) * 255 for i in range(256)], dtype=np.uint8)

# اعمال تبدیل گاما به تصویر
gamma_corrected_image = cv2.LUT(image, lookup_table)

# نمایش تصویر اصلی و تصویر تقویت شده
cv2.imshow('Original Image', image)
cv2.imshow('Gamma Corrected Image', gamma_corrected_image)

# انتظار برای کلید ورودی و بستن پنجره‌ها
cv2.waitKey(0)
cv2.destroyAllWindows()

# ذخیره تصویر تقویت شده
cv2.imwrite('gamma_corrected_image.jpg', gamma_corrected_image)