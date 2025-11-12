import numpy as np

# ماتریس f
f = np.array([
    [128, 55],
    [80, 100],
    [69, 124]
])

# بردار ستونی نوع اول (column-major)
vec_col_major = f.flatten(order='F')

# بردار ستونی نوع دوم (row-major)
vec_row_major = f.flatten(order='C')

print("بردار ستونی نوع اول:")
print(vec_col_major.reshape(-1, 1))

print("\nبردار ستونی نوع دوم:")
print(vec_row_major.reshape(-1, 1))
