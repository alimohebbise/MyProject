import cv2
import numpy as np
import sys

class PillApp:
    def __init__(self):
        print("🚀 برنامه شروع شد")

    def get_image_from_user(self):
        path = input("📷 مسیر عکس قرص را وارد کنید (مثلاً pills2.jpg): ").strip()
        img = cv2.imread(path)

        if img is None:
            print("❌ تصویر لود نشد")
            sys.exit()

        print("✅ تصویر با موفقیت لود شد")
        return img

    def process(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 1.5)

        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=35,
            param1=100,
            param2=30,
            minRadius=15,
            maxRadius=40
        )

        if circles is None:
            print("❌ هیچ قرصی تشخیص داده نشد")
            cv2.imshow("Result", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return

        circles = np.round(circles[0]).astype(int)
        print(f"🔵 تعداد دایره‌های تشخیص داده شده: {len(circles)}")

        count = 0
        for x, y, r in circles:
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r - 4, 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]

            if mean_val > 130:
                count += 1
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            cv2.circle(img, (x, y), r, color, 2)

        print("✅ تعداد قرص‌های باقی‌مانده:", count)

        cv2.imshow("Pill Counter", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self):
        img = self.get_image_from_user()
        self.process(img)


if __name__ == "__main__":
    app = PillApp()
    app.run()
