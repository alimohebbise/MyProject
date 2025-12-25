import cv2
import numpy as np


class PillDetector:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.img = None
        self.gray = None
        self.circles = None

    def load_image(self):
        """ بارگذاری تصویر از مسیر مشخص شده """
        if self.image_path is None:
            print("❌ لطفاً مسیر تصویر را وارد کنید")
            return False

        self.img = cv2.imread(self.image_path)
        if self.img is None:
            print("❌ تصویر پیدا نشد")
            return False

        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return True

    def detect_pills(self):
        """ تشخیص دایره‌ها (قرص‌ها) """
        if self.img is None:
            print("❌ ابتدا تصویر را بارگذاری کنید")
            return False

        blur = cv2.GaussianBlur(self.gray, (9, 9), 1.5)

        self.circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=35,
            param1=100,
            param2=30,
            minRadius=15,
            maxRadius=40
        )

        if self.circles is not None:
            self.circles = np.round(self.circles[0]).astype(int)
            return True
        else:
            print("❌ دایره‌ای پیدا نشد")
            return False

    def count_and_show_pills(self):
        """ شمارش قرص‌ها و نمایش تصویر با دایره‌ها """
        if self.circles is None:
            print("❌ ابتدا قرص‌ها را تشخیص دهید")
            return

        count = 0
        for x, y, r in self.circles:
            mask = np.zeros(self.gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r - 4, 255, -1)
            mean_val = cv2.mean(self.gray, mask=mask)[0]

            # بررسی روشنایی برای تشخیص قرص‌های موجود یا خالی
            if mean_val > 130:
                count += 1
                color = (0, 255, 0)  # قرص موجود
            else:
                color = (0, 0, 255)  # قرص خالی

            cv2.circle(self.img, (x, y), r, color, 2)

        print(f"✅ تعداد قرص‌های باقی‌مانده: {count}")

        cv2.imshow("Pill Detection", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self):
        """ اجرای کامل تشخیص قرص """
        if self.load_image() and self.detect_pills():
            self.count_and_show_pills()
        else:
            print("❌ خطا در بارگذاری یا تشخیص تصویر.")
