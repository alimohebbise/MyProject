import matplotlib.pyplot as plt

# داده‌ها
I = [0.736, 1.031, 1.328, 1.608]
V = [5, 7, 9, 11]

# رسم نمودار
plt.plot(I, V, marker='o', linestyle='-', linewidth=2, color='blue')
plt.title("")
plt.xlabel("V(v)")
plt.ylabel("I(mA)")
plt.grid(True)

# ذخیره به‌صورت عکس در کنار فایل پایتون
plt.savefig("Line_slope_graph.png")

# نمایش نمودار
plt.show()

print("✅ نمودار با نام 'IV_chart.png' در کنار فایل پایتون ذخیره شد.")
