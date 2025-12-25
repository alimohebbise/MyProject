#!/usr/bin/env python3
# نسخهٔ تکامل‌یافته با لاگ و fallback بیشتر

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import time
import traceback

def try_read_image(path):
    # تلاش برای خواندن تصویر (پشتیبانی بهتر از یونیکد در ویندوز)
    try:
        arr = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            # fallback به imread معمولی
            img = cv2.imread(path, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None

def detect_pills_np(img_bgr, thresh=100, debug=False, debug_prefix="debug"):
    img = img_bgr.copy()
    scale = 800.0 / max(img.shape[:2])
    if scale < 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    if debug:
        cv2.imwrite(f"{debug_prefix}_gray.jpg", gray)
        cv2.imwrite(f"{debug_prefix}_blur.jpg", gray_blur)

    # اول تلاش با Hough
    circles_list = []
    try:
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
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            circles_list = [(int(x), int(y), int(r)) for (x, y, r) in circles]
    except Exception:
        # اگر Hough خطا داد، نادیده بگیر
        circles_list = []

    # اگر Hough نتیجه نداد، تلاش با blob detector
    if len(circles_list) == 0:
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 80
        params.maxArea = 15000
        params.filterByCircularity = True
        params.minCircularity = 0.4
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gray_blur)
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            r = int(np.sqrt(kp.size / np.pi))
            circles_list.append((x, y, r))

    # fallback با روش کانتور (برای شیت‌های با تفاوت روشن/تاریک مشخص)
    if len(circles_list) == 0:
        th = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 6)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
        if debug:
            cv2.imwrite(f"{debug_prefix}_th.jpg", th)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 80 or area > 20000:
                continue
            perim = cv2.arcLength(cnt, True)
            if perim == 0:
                continue
            circularity = 4 * np.pi * area / (perim * perim)
            if circularity < 0.3:
                continue
            M = cv2.moments(cnt)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            r = int(np.sqrt(area / np.pi))
            circles_list.append((cx, cy, r))

    results = []
    for (x, y, r) in circles_list:
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), max(r - 2, 1), 255, -1)
        mean_val = cv2.mean(gray, mask=mask)[0]
        present = mean_val > thresh
        results.append({'x': x, 'y': y, 'r': r, 'mean_intensity': mean_val, 'present': present})

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

    return {'total_slots': total, 'present': present_count, 'empty': empty_count,
            'details': results, 'visualization_img': vis}

class App:
    def __init__(self, root):
        self.root = root
        root.title("تشخیص مقدار مصرف شده / باقی‌مانده (جعبه قرص) - Debug")
        root.configure(bg='white')
        root.geometry("1000x760")

        tk.Label(root, text="لطفا عکس خود را وارد کنید", font=("Tahoma", 16), bg='white').pack(pady=10)
        tk.Button(root, text="لطفا عکس خود را وارد کنید", command=self.on_load_image,
                  font=("Tahoma", 12), bg='#f0f0f0').pack(pady=6)

        self.frame = tk.Frame(root, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.img_label = tk.Label(self.frame, bg='white')
        self.img_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.info_frame = tk.Frame(self.frame, bg='white')
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.total_var = tk.StringVar(value="تعداد کل: -")
        self.present_var = tk.StringVar(value="پر (باقی‌مانده): -")
        self.empty_var = tk.StringVar(value="خالی (استفاده‌شده): -")
        tk.Label(self.info_frame, textvariable=self.total_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)
        tk.Label(self.info_frame, textvariable=self.present_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)
        tk.Label(self.info_frame, textvariable=self.empty_var, font=("Tahoma", 14), bg='white').pack(anchor='ne', pady=8)

        tk.Label(self.info_frame, text="آستانه شدت (Threshold):", bg='white').pack(anchor='ne', pady=(20,2))
        self.thresh_scale = tk.Scale(self.info_frame, from_=30, to=200, orient=tk.HORIZONTAL, bg='white')
        self.thresh_scale.set(100)
        self.thresh_scale.pack(anchor='ne')

        self.debug_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.info_frame, text="فعال کردن Debug (ذخیره میانی)", variable=self.debug_var, bg='white').pack(anchor='ne', pady=8)

        self.save_btn = tk.Button(self.info_frame, text="ذخیره تصویر خروجی", command=self.save_output, state=tk.DISABLED)
        self.save_btn.pack(anchor='ne', pady=(20,0))

        self.last_vis_np = None

    def on_load_image(self):
        path = filedialog.askopenfilename(title="انتخاب تصویر", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")])
        if not path:
            return
        try:
            img = try_read_image(path)
            if img is None:
                raise RuntimeError("تصویر باز نشد (try_read_image failed). ممکن است مسیر یا فرمت مشکل داشته باشد.")
            # نمایش تصویر اصلی سریع (برای اطمینان)
            self.show_pil_image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), max_w=420)

            debug = self.debug_var.get()
            prefix = f"debug_{int(time.time())}" if debug else "debug_tmp"
            res = detect_pills_np(img, thresh=self.thresh_scale.get(), debug=debug, debug_prefix=prefix)

            if res['total_slots'] == 0:
                messagebox.showwarning("تذکر", "هیچ خانه‌ای شناسایی نشد. علت ممکن است نور، زاویه یا نوع شیت متفاوت باشد.\nاگر مایلید Debug را فعال کنید تا تصاویر میانی ذخیره شود.")
            self.update_ui_with_result(res)
        except Exception as e:
            tb = traceback.format_exc()
            # نمایش traceback کامل در یک کادر برای کمک به دیباگ
            messagebox.showerror("خطا در پردازش تصویر", f"{e}\n\nTraceback:\n{tb}")

    def show_pil_image(self, rgb_array, max_w=420, max_h=700):
        pil = Image.fromarray(rgb_array)
        w, h = pil.size
        scale = min(1.0, max_w / w, max_h / h)
        if scale < 1.0:
            pil = pil.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(pil)
        self.img_label.configure(image=photo)
        self.img_label.image = photo

    def update_ui_with_result(self, res):
        vis_bgr = res['visualization_img']
        vis_rgb = cv2.cvtColor(vis_bgr, cv2.COLOR_BGR2RGB)
        self.show_pil_image(vis_rgb, max_w=700)
        self.total_var.set(f"تعداد کل: {res['total_slots']}")
        self.present_var.set(f"پر (باقی‌مانده): {res['present']}")
        self.empty_var.set(f"خالی (استفاده‌شده): {res['empty']}")
        self.save_btn.config(state=tk.NORMAL)
        self.last_vis_np = vis_bgr

    def save_output(self):
        if self.last_vis_np is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")])
        if not path:
            return
        success, enc = cv2.imencode(os.path.splitext(path)[1] if os.path.splitext(path)[1] else '.jpg', self.last_vis_np)
        if success:
            with open(path, 'wb') as f:
                f.write(enc.tobytes())
            messagebox.showinfo("ذخیره شد", f"تصویر ذخیره شد: {path}")
        else:
            messagebox.showerror("خطا", "خطا در ذخیره تصویر")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()