import cv2
from cv2 import dnn_superres

# خواندن تصویر
image = cv2.imread("super_resolition.py.jpg")

# ساخت شیء سوپر رزولوشن
sr = dnn_superres.DnnSuperResImpl_create()

# دانلود مدل EDSR_x4 از آدرس زیر و بگذار کنار کد:
# https://github.com/Saafke/EDSR_Tensorflow/tree/master/models
path = "EDSR_x4.pb"

# خواندن مدل
sr.readModel(path)

# تنظیم نام و فاکتور بزرگنمایی
sr.setModel("edsr", 4)

# اعمال به تصویر
result = sr.upsample(image)

# ذخیره تصویر جدید
cv2.imwrite("friedgee.jpg", result)

print("✅ تصویر با مدل Super Resolution بزرگ و باکیفیت‌تر شد!")
