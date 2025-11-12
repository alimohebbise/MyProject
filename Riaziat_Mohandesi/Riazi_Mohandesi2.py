import numpy as np
import matplotlib.pyplot as plt

# پارامترها
K = 40               # تعداد جملات فرد (مثلاً 40)
n_points = 3000      # تعداد نقاط x (بالاتر = تصویر نرم‌تر)
x = np.linspace(-np.pi, np.pi, n_points)  # بازه پایه

# تابع اصلی پله‌ای (دوره‌ای با دوره 2pi)
def f_original(x):
    xp = ((x + np.pi) % (2*np.pi)) - np.pi   # بردن x به (-pi, pi]
    # مقدار: 0 برای -pi < xp <= 0 ، 1 برای 0 < xp <= pi ، xp==0 -> 0.5
    y = np.where(xp == 0, 0.5, np.where(xp > 0, 1.0, 0.0))
    return y

# جمع جزئی سری فوریه (K جملهٔ فرد)
def fourier_partial(x, K):
    s = np.full_like(x, 0.5, dtype=float)  # a0/2 = 1/2
    for k in range(K):
        n = 2*k + 1
        s += (2.0 / (n * np.pi)) * np.sin(n * x)
    return s

y_orig = f_original(x)
y_fourier = fourier_partial(x, K)

# نمایش
plt.figure(figsize=(10,4), dpi=200)
plt.plot(x, y_orig, '--', linewidth=1.8, label='Original (step)')
plt.plot(x, y_fourier, linewidth=1.2, label=f'Fourier partial K={K}')
plt.xlim(-np.pi, np.pi)
plt.ylim(-0.2, 1.2)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Fourier series approximation (period 2π)')
plt.legend()
plt.grid(True)
plt.show()

# اگر خواستی خطای بین تقریب و تابع اصلی:
error = y_fourier - y_orig
L2 = np.sqrt(np.mean(error**2))
print("L2 error (RMSE) =", L2)
