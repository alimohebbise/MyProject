import cv2
import numpy as np

MIN_AREA = 2500
MAX_AREA = 9000
ASPECT_RATIO_MIN = 1.2
ASPECT_RATIO_MAX = 2.5
INTENSITY_THRESHOLD = 160

image = cv2.imread("Ghors (4).jpg")
if image is None:
    print("Error: Image not found!")
    exit()

orig = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11, 2
)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < MIN_AREA or area > MAX_AREA:
        continue

    x, y, w, h = cv2.boundingRect(cnt)
    if min(w, h) == 0:
        continue

    aspect_ratio = max(w, h) / min(w, h)

    if ASPECT_RATIO_MIN < aspect_ratio < ASPECT_RATIO_MAX:
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask, [cnt], -1, 255, -1)

        mean_intensity = cv2.mean(gray, mask=mask)[0]

        if mean_intensity < INTENSITY_THRESHOLD:
            count += 1
            cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.putText(orig, f"Pill Count: {count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

cv2.imshow("Pill Counter", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()