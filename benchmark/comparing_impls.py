import time
import numpy as np
import matplotlib.pyplot as plt
from option_pricer import EuropeanOptionPython
import monte_carlo_pricer


def plot_python_vs_cpp(data) -> None:
    """
    Function plots the benchmark for Python vs C++ implementation.

    :param data: elements from benchmark_results.dat
    :return: None
    """
    plt.plot(data[:, 0], data[:, 1])
    plt.plot(data[:, 0], data[:, 2])
    plt.xlabel("Number of iterations")
    plt.ylabel("Time in seconds")
    plt.title("Benchmark Python vs C++ Implementation")
    labels = ["Python", "C++"]
    plt.legend(labels, loc="upper left")
    plt.grid()
    plt.savefig("python_vs_cpp.svg")
    plt.show()


def plot_speedup(data) -> None:
    """
    Function plots the speedup (ratio) of the python implementation runtime
    with the C++ implementation.

    :param data: elements from benchmark_results.dat
    :return: None
    """
    plt.plot(data[:, 0], data[:, 3])
    plt.xlabel("Number of iterations")
    plt.ylabel("Speedup multiplier")
    plt.title("Speed Benchmark (Python implementation / C++ implementation)")
    plt.grid()
    plt.savefig("speedup.svg")
    plt.show()


def benchmark() -> None:
    """
    Function benchmarks the performance of the pure python implementation vs the C++ backend implementation.

    :return:
    """
    S0, K, r, sigma, T = 100, 100, 0.05, 0.2, 1.0
    num_paths = 1_000_000

    for i in range(1, 26):
        py_opt = EuropeanOptionPython(S0, K, r, sigma, T)
        start = time.perf_counter()
        py_price = py_opt.calculate_price(num_paths)
        py_time = time.perf_counter() - start

        cpp_opt = monte_carlo_pricer.EuropeanOption(S0, K, r, sigma, T)
        start = time.perf_counter()
        cpp_price = cpp_opt.calculatePrice(num_paths)
        cpp_time = time.perf_counter() - start

        print(f"Python call price={py_price[0]:.4f}, time={py_time:.2f}s")
        print(f"C++ call price={cpp_price[0]:.4f}, time={cpp_time:.2f}s")
        print(f"Speedup ≈ {py_time / cpp_time:.1f}x")

        f = open("benchmark_results.txt", "a")
        f.write(f"{i} {py_time} {cpp_time} {py_time / cpp_time:.3}\n")

    data = np.loadtxt("benchmark_results.dat", delimiter=" ")
    plot_python_vs_cpp(data)
    plot_speedup(data)


if __name__ == "__main__":
    benchmark()
