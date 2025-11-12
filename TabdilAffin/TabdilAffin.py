import cv2
import numpy as np
import math

# --- 1. خواندن عکس در مقیاس خاکستری ---
img = cv2.imread("input.jpg", cv2.IMREAD_GRAYSCALE)

h, w = img.shape

# --- 2. زاویه چرخش (در رادیان) ---
theta = math.radians(60)

# --- 3. ماتریس تبدیل آفین ---
M = np.float32([
    [ math.cos(theta), -math.sin(theta), 0 ],
    [ math.sin(theta),  math.cos(theta), 0 ]
])

# --- 4. محاسبه اندازه جدید تصویر برای جلوگیری از برش ---
# گوشه‌های تصویر را تبدیل می‌کنیم تا محدوده جدید را پیدا کنیم
corners = np.array([
    [0, 0],
    [w, 0],
    [0, h],
    [w, h]
], dtype=np.float32)

rotated_corners = np.dot(corners, M[:, :2].T)

min_x = np.min(rotated_corners[:, 0])
max_x = np.max(rotated_corners[:, 0])
min_y = np.min(rotated_corners[:, 1])
max_y = np.max(rotated_corners[:, 1])

new_w = int(max_x - min_x)
new_h = int(max_y - min_y)

# انتقال برای اینکه تصویر وسط باشد
M[0, 2] = -min_x
M[1, 2] = -min_y

# --- 5. اعمال تبدیل آفین ---
rotated = cv2.warpAffine(img, M, (new_w, new_h))

# --- 6. ذخیره خروجی ---
cv2.imwrite("rotated_60deg.jpg", rotated)

print("Done!")
