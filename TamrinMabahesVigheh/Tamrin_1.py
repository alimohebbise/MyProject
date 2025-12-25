import numpy as np

# تصویر ورودی
A = np.array([
    [12, 60, 191, 20],
    [5, 185, 285, 15],
    [0, 25, 79, 171],
    [82, 51, 97, 132]
])

# فیلتر
w = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# برعکس کردن هسته (برای convolution واقعی)
kernel = np.flipud(np.fliplr(w))

# ---------- Full Convolution ----------
pad = kernel.shape[0] - 1
A_padded = np.pad(A, pad_width=pad, mode='constant', constant_values=0)

full_out = np.zeros((
    A_padded.shape[0] - kernel.shape[0] + 1,
    A_padded.shape[1] - kernel.shape[1] + 1
))

for i in range(full_out.shape[0]):
    for j in range(full_out.shape[1]):
        region = A_padded[i:i+3, j:j+3]
        full_out[i, j] = np.sum(region * kernel)

# ---------- Valid Convolution ----------
valid_out = np.zeros((
    A.shape[0] - kernel.shape[0] + 1,
    A.shape[1] - kernel.shape[1] + 1
))

for i in range(valid_out.shape[0]):
    for j in range(valid_out.shape[1]):
        region = A[i:i+3, j:j+3]
        valid_out[i, j] = np.sum(region * kernel)

print("Full Convolution Output:")
print(full_out)

print("\nValid Convolution Output:")
print(valid_out)
