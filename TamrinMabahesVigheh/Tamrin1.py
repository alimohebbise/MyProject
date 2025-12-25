import numpy as np

# تصویر ورودی (4x4)
A = np.array([
    [12, 60, 191, 20],
    [5, 185, 255, 15],
    [0, 25, 79, 171],
    [82, 51, 97, 132]
])

# فیلتر (3x3)
w = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# -------------------------
# تابع پیچش کامل
def full_convolution(img, kernel):
    m, n = img.shape
    k, l = kernel.shape

    pad_h = k - 1
    pad_w = l - 1

    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')

    output = np.zeros((m + k - 1, n + l - 1))

    kernel_flipped = np.flip(kernel)

    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            region = padded[i:i+k, j:j+l]
            output[i, j] = np.sum(region * kernel_flipped)

    return output

# -------------------------
# تابع پیچش کوتاه‌شده (Valid)
def valid_convolution(img, kernel):
    m, n = img.shape
    k, l = kernel.shape

    output = np.zeros((m - k + 1, n - l + 1))
    kernel_flipped = np.flip(kernel)

    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            region = img[i:i+k, j:j+l]
            output[i, j] = np.sum(region * kernel_flipped)

    return output

# -------------------------
# محاسبه
full_result = full_convolution(A, w)
valid_result = valid_convolution(A, w)

print("Full Convolution Result:\n", full_result)
print("\nValid Convolution Result:\n", valid_result)
