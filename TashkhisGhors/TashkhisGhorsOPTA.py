#!/usr/bin/env python3
# TashkhisGhorsOPT_gui.py
# GUI ساده با tkinter برای انتخاب عکس و نمایش نتیجهٔ تشخیص قرص

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

def detect_pills_np(img_bgr, thresh=100, debug=False):
    """
    ورودی: تصویر BGR (numpy array)
    خروجی: dict شامل total_slots, present, empty, details و تصویر بصری (BGR numpy array)
    """
    img = img_bgr.copy()
    # scale down برای سرعت
    scale = 800.0 / max(img.shape[:2])
    if scale < 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    circles = cv2.HoughCircles(
        gray_blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=28,
        minRadius=12,
        maxRadius=60
    )

    if circles is None:
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 10000
        params.filterByCircularity = True
        params.minCircularity = 0.6
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gray_blur)
        circles_list = []
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            r = int(np.sqrt(kp.size / np.pi))
            circles_list.append((x, y, r))
    else:
        circles = np.round(circles[0, :]).astype("int")
        circles_list = [(int(x), int(y), int(r)) for (x, y, r) in circles]

    results = []
    for (x, y, r) in circles_list:
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), max(r - 2, 1), 255, -1)
        mean_val = cv2.mean(gray, mask=mask)[0]
        present = mean_val > thresh
        results.append({
            'x': x, 'y': y, 'r': r,
            'mean_intensity': mean_val,
            'present': present
        })

    total = len(results)
    present_count = sum(1 for r in results if r['present'])
    empty_count = total - present_count

    vis = img.copy()
    for res in results:
        color = (0, 255, 0) if res['present'] else (0, 0, 255)
        cv2.circle(vis, (res['x'], res['y']), res['r'], color, 2)
        if debug:
            cv2.putText(vis, f"{int(res['mean_intensity'])}", (res['x']-10, res['y']),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,0), 1)

    return {
        'total_slots': total,
        'present': present_count,
        'empty': empty_count,
        'details': results,
        'visualization_img': vis
    }

class App:
    def __init__(self, root):
        self.root = root
        root.title("تشخیص مقدار مصرف شده / باقی‌مانده (جعبه قرص)")
        root.configure(bg='white')
        # اندازهٔ پنجره
        root.geometry("940x720")
        root.resizable(True, True)

        # متن و دکمه
        self.label = tk.Label(root, text="لطفا عکس خود را وارد کنید", font=("Tahoma", 16), bg='white')
        self.label.pack(pady=(20, 8))

        self.button = tk.Button(root, text="لطفا عکس خود را وارد کنید", command=self.on_load_image,
                                font=("Tahoma", 12), bg='#f0f0f0')
        self.button.pack(pady=(0, 12))

        # فریم برای نمایش تصویر و اطلاعات
        self.frame = tk.Frame(root, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)

        # لیبل تصویر
        self.img_label = tk.Label(self.frame, bg='white')
        self.img_label.pack(side=tk.LEFT, padx=10, pady=10)

        # فریم اطلاعات
        self.info_frame = tk.Frame(self.frame, bg='white')
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.total_var = tk.StringVar(value="تعداد کل: -")
        self.present_var = tk.StringVar(value="پر (باقی‌مانده): -")
        self.empty_var = tk.StringVar(value="خالی (استفاده‌شده): -")

        tk.Label(self.info_frame, textvariable=self.total_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)
        tk.Label(self.info_frame, textvariable=self.present_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)
        tk.Label(self.info_frame, textvariable=self.empty_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)

        # آستانه قابل تنظیم
        tk.Label(self.info_frame, text="آستانه شدت (Threshold):", bg='white').pack(anchor='ne', pady=(20,2))
        self.thresh_scale = tk.Scale(self.info_frame, from_=30, to=200, orient=tk.HORIZONTAL, bg='white')
        self.thresh_scale.set(100)
        self.thresh_scale.pack(anchor='ne')

        # دکمهٔ ذخیره تصویر خروجی
        self.save_btn = tk.Button(self.info_frame, text="ذخیره تصویر خروجی", command=self.save_output, state=tk.DISABLED)
        self.save_btn.pack(anchor='ne', pady=(20,0))

        self.current_vis = None  # نگه داشتن تصویر خروجی (PIL PhotoImage)
        self.last_vis_np = None  # نگه داشتن تصویر numpy BGR برای ذخیره

    def on_load_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="انتخاب تصویر", filetypes=filetypes)
        if not path:
            return
        try:
            img_bgr = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img_bgr is None:
                raise ValueError("نمی‌توان تصویر را باز کرد.")
            # اجرای تشخیص
            thresh = self.thresh_scale.get()
            res = detect_pills_np(img_bgr, thresh=thresh, debug=False)
            self.update_ui_with_result(res)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در پردازش تصویر:\n{e}")

    def update_ui_with_result(self, res):
        vis_bgr = res['visualization_img']
        # تبدیل به PIL برای نمایش در tkinter
        vis_rgb = cv2.cvtColor(vis_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(vis_rgb)
        # تغییر اندازه برای نمایش بهتر در پنجره (حداکثر عرض 700px)
        max_w = 700
        max_h = 650
        w, h = pil_img.size
        scale = min(1.0, max_w / w, max_h / h)
        if scale < 1.0:
            new_size = (int(w*scale), int(h*scale))
            pil_img = pil_img.resize(new_size, Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(pil_img)
        self.img_label.configure(image=photo)
        self.img_label.image = photo  # نگهداری مرجع

        self.total_var.set(f"تعداد کل: {res['total_slots']}")
        self.present_var.set(f"پر (باقی‌مانده): {res['present']}")
        self.empty_var.set(f"خالی (استفاده‌شده): {res['empty']}")

        # فعال کردن دکمه ذخیره
        self.save_btn.config(state=tk.NORMAL)
        self.current_vis = photo
        self.last_vis_np = res['visualization_img']

    def save_output(self):
        if self.last_vis_np is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
                                            title="ذخیره تصویر خروجی")
        if not path:
            return
        # برای جلوگیری از مشکلات یونیکد در ویندوز از imencode و tofile استفاده می‌کنیم
        try:
            ext = os.path.splitext(path)[1].lower()
            # BGR numpy -> encode -> write with fromfile compatibility
            success, encoded = cv2.imencode(ext if ext else '.jpg', self.last_vis_np)
            if success:
                with open(path, 'wb') as f:
                    f.write(encoded.tobytes())
                messagebox.showinfo("ذخیره شد", f"تصویر خروجی در:\n{path}\nذخیره شد.")
            else:
                raise IOError("خطا در رمزگذاری تصویر برای ذخیره.")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ذخیره‌سازی تصویر:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()