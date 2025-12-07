import time
import statistics
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
    num_runs = data[:, 0]
    py_times = data[:, 1]
    cpp_times = data[:, 2]

    plt.plot(num_runs, py_times)
    plt.plot(num_runs, cpp_times)
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

    :param data: numpy array from benchmark_results.dat
                 column 0: num_paths
                 column 1: python_time
                 column 2: cpp_time
                 column 3: ratio py_time/cpp_time
    """
    num_runs = data[:, 0]
    speedup = data[:, 3]

    plt.plot(num_runs, speedup)
    plt.xlabel("Number of iterations")
    plt.ylabel("Speedup multiplier")
    plt.title("Speed Benchmark (Python implementation / C++ implementation)")
    plt.grid()
    plt.savefig("speedup.svg")
    plt.show()

def benchmark() -> None:
    """
    Function benchmarks the performance of the pure python implementation vs the C++ backend implementation
    as a function of the number of the number of iterations.
    """
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    seed = 48
    num_paths = 1_000_000
    num_runs= 25

    py_opt = EuropeanOptionPython(S0, K, r, sigma, T, seed)
    cpp_opt = monte_carlo_pricer.EuropeanOption(S0, K, r, sigma, T, seed)
    speedup_results = []
    py_runtime_results = []
    cpp_runtime_results = []

    for i in range(1, num_runs + 1):

        # Runs the pure python implementation
        start = time.perf_counter()
        py_price = py_opt.calculate_price(num_paths)
        py_time = time.perf_counter() - start
        py_call_price = py_price[0]
        py_put_price = py_price[1]

        # Runs the C++ backend implementation
        start = time.perf_counter()
        cpp_price = cpp_opt.calculatePrice(num_paths)
        cpp_time = time.perf_counter() - start
        cpp_call_price = cpp_price[0]
        cpp_put_price = cpp_price[1]

        speedup = py_time / cpp_time
        speedup_results.append(speedup)
        py_runtime_results.append(py_time)
        cpp_runtime_results.append(cpp_time)

        print(f"Python: call price={py_call_price:.4f}, put price={py_put_price:.4f}, time={py_time:.2f}s")
        print(f"C++: call price={cpp_call_price:.4f}, put price={cpp_put_price:.4f}, time={cpp_time:.2f}s")
        print(f"Speedup ≈ {speedup:.1f}x\n ")

        f = open("benchmark_results_per_iter.dat", "a")
        f.write(f"{i} {py_time} {cpp_time} {speedup:.3}\n")

    mean_speedup = statistics.mean(speedup_results)
    mean_pytime = statistics.mean(py_runtime_results)
    mean_cpptime = statistics.mean(cpp_runtime_results)

    print(f"mean speed up: {mean_speedup:.2f}x")
    print(f"mean python runtime: {mean_pytime:.2f} s")
    print(f"mean c++ runtime: {mean_cpptime:.2f} s")

    data = np.loadtxt("benchmark_results_per_iter.dat", delimiter=" ")
    plot_python_vs_cpp(data)
    plot_speedup(data)

if __name__ == "__main__":
    benchmark()
