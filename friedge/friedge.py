import cv2

# مسیر تصویر ورودی
image_path = "friedge.png"

# خواندن تصویر
img = cv2.imread(image_path)

# اندازه جدید (مثلاً 2 برابر)
scale = 2
width = int(img.shape[1] * scale)
height = int(img.shape[0] * scale)

# تغییر اندازه با الگوریتم باکیفیت‌تر
resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

# ذخیره تصویر جدید
cv2.imwrite("output_resized.jpg", resized)

print("✅ تصویر با موفقیت بزرگ و ذخیره شد.")
