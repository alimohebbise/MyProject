import cv2
import numpy as np
import matplotlib.pyplot as plt

# دانلود مدل از قبل آموزش‌دیده (فقط یکبار نیاز است)
# مدل‌ها را از این لینک بگیر و در کنار فایل پایتون ذخیره کن:
# https://github.com/chuanqi305/MobileNet-SSD
# فایل‌ها: MobileNetSSD_deploy.prototxt و MobileNetSSD_deploy.caffemodel

prototxt = "MobileNetSSD_deploy.prototxt"
model = "MobileNetSSD_deploy.caffemodel"

# بارگذاری شبکه
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# کلاس‌هایی که مدل می‌تواند تشخیص دهد
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# رنگ‌ها برای رسم جعبه
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# مسیر تصویر
image_path = "imagebusandcars.png"   # مسیر تصویر خودت
image = cv2.imread(image_path)
(h, w) = image.shape[:2]

# پیش‌پردازش تصویر برای ورودی شبکه
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
                             (300, 300), 127.5)
net.setInput(blob)
detections = net.forward()

# پردازش نتایج
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    # اگر اطمینان بیشتر از ۲۰٪ بود
    if confidence > 0.2:
        idx = int(detections[0, 0, i, 1])
        label = CLASSES[idx]

        # مختصات جعبه
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # انتخاب رنگ (bus = سبز، car = آبی، بقیه = قرمز)
        if label == "bus":
            color = (0, 255, 0)
        elif label == "car":
            color = (0, 0, 255)
        else:
            color = COLORS[idx]

        # رسم جعبه و نام
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
        text = f"{label}: {confidence:.2f}"
        cv2.putText(image, text, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# نمایش تصویر خروجی
plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()
