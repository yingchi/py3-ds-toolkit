import numpy as np

a = np.array([1, 2, 3])

print(a <= 2)
"""
[ True False False]
"""

print(a[a <= 2])
"""
[1 2]
"""
