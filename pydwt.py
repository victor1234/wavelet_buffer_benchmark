#!/usr/bin/env python3

import numpy as np
import pywt
import timeit
import json

result = {}

# Benchmark 1D
b1d = {"x": [], "y": []}
for k in [0.1, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
    print(k)
    x = np.random.uniform(-1, 1, int(k * 48000))

    number = 100
    t = timeit.repeat(
        "pywt.wavedec(x, 'db3', level=9)",
        setup="import pywt",
        globals={"x": x},
        number=number,
    )

    b1d["x"].append(len(x))
    b1d["y"].append(np.mean(t) / number * 1000)

result["Wavelet algorithms benchmark 1D"] = {"pywt": b1d}


# Benchmark 2D
b2d = {"x": [], "y": []}
for s in range(200, 2000, 200):
    print(s)
    x = np.random.uniform(-1, 1, s * s).reshape(s, s)

    number = 10
    t = timeit.repeat(
        "pywt.wavedec2(x, 'db3', level=4)",
        setup="import pywt",
        globals={"x": x},
        number=number,
    )

    b2d["x"].append(s)
    b2d["y"].append(np.mean(t) / number * 1000)

result["Wavelet algorithms benchmark 2D"] = {"pywt": b2d}

# Save
json.dump(result, open("pywt.json", "w"), indent=4)
