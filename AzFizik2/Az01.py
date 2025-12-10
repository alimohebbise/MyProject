import matplotlib.pyplot as plt

# داده‌ها
T = [2.30, 2.07, 1.79, 1.38]
Ln = [2.44, 3.635, 4.83, 6.93]

# رسم نمودار
plt.plot(T, Ln, marker='o', linestyle='-', linewidth=2, color='blue')
plt.title("Line slope graph")
plt.xlabel("T (Seconds)")
plt.ylabel("Ln (Ln(ε - Vc)")
plt.grid(True)

# ذخیره به‌صورت عکس در کنار فایل پایتون
plt.savefig("Line_slope_graph.png")

# نمایش نمودار
plt.show()

print("✅ نمودار با نام 'IV_chart.png' در کنار فایل پایتون ذخیره شد.")
