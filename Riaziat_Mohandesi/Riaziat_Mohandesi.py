# ----------------------------------------
#   Math Expression Builder (Python)
#   نسخه کامل – پشتیبانی از نمادهای مهندسی، دیفرانسیل، انتگرال، سری‌ها و...
#   نویسنده: ChatGPT
# ----------------------------------------

from pathlib import Path
import matplotlib.pyplot as plt

# فهرست نمادها و علائم رایج
SYMBOLS = {
    "alpha": r"\alpha", "beta": r"\beta", "gamma": r"\gamma", "delta": r"\Delta",
    "epsilon": r"\epsilon", "zeta": r"\zeta", "eta": r"\eta", "theta": r"\theta",
    "lambda": r"\lambda", "mu": r"\mu", "pi": r"\pi", "sigma": r"\sigma",
    "omega": r"\omega", "infty": r"\infty",

    "sum": r"\sum", "prod": r"\prod", "int": r"\int", "oint": r"\oint",
    "lim": r"\lim", "partial": r"\partial", "nabla": r"\nabla",
    "frac": r"\frac", "sqrt": r"\sqrt",

    "d": r"\mathrm{d}", "dt": r"\,\mathrm{d}t", "dx": r"\,\mathrm{d}x",

    "laplace": r"\mathcal{L}", "fourier": r"\mathcal{F}",
    "omega_n": r"\omega_n", "zeta": r"\zeta",

    "cdot": r"\cdot", "times": r"\times", "approx": r"\approx"
}

# تبدیل ورودی کاربر به LaTeX
def tokens_to_latex(template: str):
    out = template
    for key, val in SYMBOLS.items():
        out = out.replace("{" + key + "}", val)
    return out

# رندر خروجی به تصویر PNG
def render_math_to_png(latex_math: str, filename="output.png"):
    fig = plt.figure(figsize=(6, 1.5))
    ax = fig.add_subplot(111)
    ax.axis("off")

    ax.text(0.5, 0.5, f"${latex_math}$",
            ha="center", va="center", fontsize=20)

    Path(".").mkdir(exist_ok=True)
    plt.savefig(filename, dpi=200, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

    print(f"\n✅ تصویر با موفقیت ساخته شد: {filename}")

# ------------------------------
#   اجرای برنامه
# ------------------------------
if __name__ == "__main__":
    print("=== سازنده عبارات ریاضی ===")
    print("نمونه ورودی مثلاً:")
    print("{sum}_{ {n=1} }^{ {infty} } {frac}{1}{n^2}")
    print("{laplace}{ {f(t)} } = {int}_0^{infty} e^{-s t} f(t) {dt}")
    print("-----------------------------------------")

    expr = input("عبارت خود را وارد کنید:\n> ")

    # تبدیل به LaTeX
    latex = tokens_to_latex(expr)
    print("\nLaTeX نهایی:")
    print(latex)

    # ذخیره تصویر
    render_math_to_png(latex, "output.png")
