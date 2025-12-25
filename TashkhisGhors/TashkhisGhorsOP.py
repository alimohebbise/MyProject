import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np

class PillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("تشخیص تعداد قرص‌ها")
        self.root.geometry("500x300")

        # برچسب معرفی
        self.label = tk.Label(self.root, text="لطفاً عکس جعبه قرص را وارد کنید:", font=("Arial", 14))
        self.label.pack(pady=20)

        # دکمه برای بارگذاری تصویر
        self.load_button = tk.Button(self.root, text="بارگذاری عکس", command=self.load_image, font=("Arial", 12))
        self.load_button.pack(pady=10)

        # برچسب برای نمایش نتیجه
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.img = None

    def load_image(self):
        """ انتخاب فایل عکس توسط کاربر """
        file_path = filedialog.askopenfilename(title="انتخاب عکس", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        if not file_path:
            return

        # بارگذاری تصویر
        self.img = cv2.imread(file_path)
        if self.img is None:
            messagebox.showerror("خطا", "تصویر بارگذاری نشد!")
            return

        self.process_image()

    def process_image(self):
        """ پردازش تصویر برای تشخیص قرص‌ها """
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
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
            self.result_label.config(text="❌ هیچ قرصی پیدا نشد!")
            return

        circles = np.round(circles[0]).astype(int)

        count = 0
        empty_count = 0
        for x, y, r in circles:
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r - 4, 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]

            # تشخیص قرص‌های موجود یا خالی
            if mean_val > 130:
                count += 1
            else:
                empty_count += 1

            # رسم دایره‌ها روی تصویر
            color = (0, 255, 0) if mean_val > 130 else (0, 0, 255)
            cv2.circle(self.img, (x, y), r, color, 2)

        # نمایش نتایج
        self.result_label.config(text=f"قرص‌های موجود: {count}\nقرص‌های خالی: {empty_count}")

        # نمایش تصویر نهایی
        cv2.imshow("Pill Counter", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ایجاد و اجرای پنجره اصلی
root = tk.Tk()
app = PillApp(root)
root.mainloop()

import cv2
import numpy as np

class PillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("تشخیص تعداد قرص‌ها")
        self.root.geometry("500x300")

        # برچسب معرفی
        self.label = tk.Label(self.root, text="لطفاً عکس جعبه قرص را وارد کنید:", font=("Arial", 14))
        self.label.pack(pady=20)

        # دکمه برای بارگذاری تصویر
        self.load_button = tk.Button(self.root, text="بارگذاری عکس", command=self.load_image, font=("Arial", 12))
        self.load_button.pack(pady=10)

        # برچسب برای نمایش نتیجه
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.img = None

    def load_image(self):
        """ انتخاب فایل عکس توسط کاربر """
        file_path = filedialog.askopenfilename(title="انتخاب عکس", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        if not file_path:
            return

        # بارگذاری تصویر
        self.img = cv2.imread(file_path)
        if self.img is None:
            messagebox.showerror("خطا", "تصویر بارگذاری نشد!")
            return

        self.process_image()

    def process_image(self):
        """ پردازش تصویر برای تشخیص قرص‌ها """
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 1.5)

        # تشخیص دایره‌ها با HoughCircles
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
            self.result_label.config(text="❌ هیچ قرصی پیدا نشد!")
            return

        circles = np.round(circles[0]).astype(int)

        count = 0
        empty_count = 0
        for x, y, r in circles:
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r - 4, 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]

            # تشخیص قرص‌های موجود یا خالی
            if mean_val > 130:
                count += 1
            else:
                empty_count += 1

            # رسم دایره‌ها روی تصویر
            color = (0, 255, 0) if mean_val > 130 else (0, 0, 255)
            cv2.circle(self.img, (x, y), r, color, 2)

        # نمایش نتایج
        self.result_label.config(text=f"قرص‌های موجود: {count}\nقرص‌های خالی: {empty_count}")

        # نمایش تصویر نهایی
        cv2.imshow("Pill Counter", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ایجاد و اجرای پنجره اصلی
root = tk.Tk()
app = PillApp(root)
root.mainloop()
