#!/usr/bin/env python3

from sys import argv, exit
from untangle import parse
import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    if len(argv) < 3:
        print(f"usage: {argv[0]} wb_report(xml) pywt_data(json)")
        exit()

    # Load wb data
    document = parse(argv[1])

    test_cases = {}
    for tc in document.Catch2TestRun.TestCase:
        plot = {"x": [], "y": []}
        for br in tc.BenchmarkResults:
            plot["x"].append(float(br["name"].split()[1]))
            plot["y"].append(float(br.mean["value"]) / 1e6)

        test_cases[tc["name"]] = {"wavelet_buffer": plot}

    print(test_cases)

    # Load pywt
    pywt = json.load(open(argv[2]))
    print(pywt)

    # Merge wb and pywt data
    for name, tc in test_cases.items():
        tc.update(pywt[name])

    # Plot
    fig, ax = plt.subplots(1, 2)
    i = 0
    for n, tc in test_cases.items():
        ax[i].set_title(n)
        ax[i].set_ylabel("ms")
        for nn, plot in tc.items():
            ax[i].plot(plot["x"], plot["y"], ".-", label=nn)

        i = i + 1

    plt.legend()
    plt.show()
