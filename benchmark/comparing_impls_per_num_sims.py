import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from option_pricer import EuropeanOptionPython
import monte_carlo_pricer

def calc_perc_diff(val1: float, val2: float) -> float:
    numer: float = abs(val1 - val2)
    denom: float = abs(val1 + val2) / 2.0
    return (numer / denom) * 100.0

def plot_python_vs_cpp(data) -> None:
    """
    Function plots the benchmark for Python vs C++ implementation.

    :param data: numpy array from benchmark_results.dat
                 column 0: num_paths
                 column 1: python_time
                 column 2: cpp_time
                 column 3: ratio py_time/cpp_time
    """
    num_paths = data[:, 0]
    py_time = data[:, 1]
    cpp_time = data[:, 2]

    ticks = num_paths
    labels = [f"{x / 1e6:.1f}M" if x >= 1e6 else f"{x / 1e3:.0f}K" for x in num_paths]

    plt.xscale("log")
    plt.yscale("linear")
    plt.xticks(ticks, labels, rotation=45)
    plt.plot(num_paths, py_time,label="Python", marker="o")
    plt.plot(num_paths, cpp_time,label="C++", marker="o")
    plt.title("Benchmark: Python vs C++ implementation")
    plt.xlabel("Number of paths")
    plt.ylabel("Time, [s]")
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig("python_vs_cpp_num_paths.svg")
    plt.show()

def plot_speedup(data) -> None:
    """
    Function plots the speedup (ratio) of the python implementation runtime
    with the C++ implementation.

    :param data: numpy array from benchmark_results.dat
                 column 0: num_paths
                 column 1: python_time
                 column 2: cpp_time
                 column 3: ratio py_time/cpp_time
    """
    num_paths = data[:, 0]
    speedup = data[:, 3]

    plt.plot(num_paths, speedup)
    plt.title("Benchmark: Python vs C++ implementation (speedup)")
    plt.xlabel("Number of paths")
    plt.ylabel("Speedup")
    plt.grid()
    plt.savefig("python_vs_cpp_num_paths_speedup.svg")
    plt.show()

def benchmark() -> None:
    """
    Function benchmarks the performance of the pure python implementation vs the C++ backend implementation
    as a function of the number of paths.
    """
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    seed = 48
    num_paths_list = [
        500_000,
        750_000,
        1_000_000,
        5_000_000,
        10_000_000,
        15_000_000,
        20_000_000,
        30_000_000,
        40_000_000,
        50_000_000,
    ]
    py_opt = EuropeanOptionPython(S0, K, r, sigma, T, seed)
    cpp_opt = monte_carlo_pricer.EuropeanOption(S0, K, r, sigma, T, seed)

    for num_paths in num_paths_list:
        # Runs the pure python implementation
        start = time.perf_counter()
        py_price = py_opt.calculate_price(num_paths)
        py_time = time.perf_counter() - start
        py_call = py_price[0]
        py_put = py_price[1]

        # Runs the C++ backend implementation
        start = time.perf_counter()
        cpp_price = cpp_opt.calculatePrice(num_paths)
        cpp_time = time.perf_counter() - start
        cpp_call = cpp_price[0]
        cpp_put = cpp_price[1]

        print(f"Num paths: {num_paths}")
        print(f"Python call price={py_call:.4f}, Python put price={py_put:.4f}, time={py_time:.2f}s")
        print(f"C++ call price={cpp_call:.4f}, C++ call price={cpp_put:.4f}, time={cpp_time:.2f}s")
        print(f"Speedup ≈ {py_time / cpp_time:.1f}x")
        print(f"% difference for call price={calc_perc_diff(py_call, cpp_call):.2f}")
        print(f"% difference for put price={calc_perc_diff(py_put, cpp_put):.2f}\n")
        f = open("benchmark_results_num_sims.dat", "a")
        f.write(f"{num_paths} {py_time} {cpp_time} {py_time / cpp_time:.3}\n")

    data = np.loadtxt("benchmark_results_num_sims.dat", delimiter=" ")
    plot_python_vs_cpp(data)
    plot_speedup(data)


if __name__ == "__main__":
    benchmark()
