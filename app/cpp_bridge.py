import ctypes
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "cpp" / "libmarket_math.so"


def moving_average(values, window=7):
    arr = np.array(values, dtype=np.float64)
    if len(arr) == 0:
        return []
    if LIB.exists():
        out = np.zeros_like(arr)
        lib = ctypes.CDLL(str(LIB))
        lib.moving_average.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        lib.moving_average(arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(arr), int(window), out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        return out.tolist()
    # Python fallback
    return [float(np.mean(arr[max(0, i-window+1):i+1])) for i in range(len(arr))]
