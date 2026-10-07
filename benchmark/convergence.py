"""Convergence of the Monte Carlo price to the Black-Scholes closed form.

For each path count N the engine is run with several independent seeds and the
RMS error of the call and put prices against the analytic Black-Scholes value
is recorded. A correct Monte Carlo estimator has a standard error of
sigma_payoff / sqrt(N), where sigma_payoff is the standard deviation of the
discounted payoff; that prediction is computed analytically and plotted
alongside the measured error.

Run from the benchmark/ directory:

    PYTHONPATH=../build/python python convergence.py
"""

from math import erf, exp, log, sqrt

import matplotlib.pyplot as plt
import numpy as np

import monte_carlo_pricer

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
PATH_COUNTS = [10**k for k in range(2, 9)]
NUM_SEEDS = 32
# Thread t of a run seeded with s draws from stream s + t, so base seeds must
# be further apart than the thread count for the runs to be independent.
SEED_STRIDE = 1000


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def black_scholes() -> tuple[float, float]:
    """Analytic European call and put prices."""
    d1 = (log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call = S0 * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)
    put = K * exp(-r * T) * norm_cdf(-d2) - S0 * norm_cdf(-d1)
    return call, put


def payoff_std() -> tuple[float, float]:
    """Analytic standard deviation of the discounted call and put payoffs."""
    d1 = (log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    d3 = d1 + sigma * sqrt(T)
    disc = exp(-r * T)
    s2 = S0**2 * exp((2.0 * r + sigma**2) * T)  # E[S_T^2] prefactor
    fwd = S0 * exp(r * T)

    call_m1 = fwd * norm_cdf(d1) - K * norm_cdf(d2)
    call_m2 = s2 * norm_cdf(d3) - 2.0 * K * fwd * norm_cdf(d1) + K**2 * norm_cdf(d2)
    put_m1 = K * norm_cdf(-d2) - fwd * norm_cdf(-d1)
    put_m2 = K**2 * norm_cdf(-d2) - 2.0 * K * fwd * norm_cdf(-d1) + s2 * norm_cdf(-d3)

    return disc * sqrt(call_m2 - call_m1**2), disc * sqrt(put_m2 - put_m1**2)


def measure() -> np.ndarray:
    """RMS pricing error over NUM_SEEDS independent runs, per path count.

    :return: array with columns N, call RMS error, put RMS error
    """
    bs_call, bs_put = black_scholes()
    rows = []
    for n in PATH_COUNTS:
        call_err, put_err = [], []
        for i in range(NUM_SEEDS):
            opt = monte_carlo_pricer.EuropeanOption(
                S0, K, r, sigma, T, 1 + i * SEED_STRIDE
            )
            call, put = opt.calculatePrice(n)
            call_err.append(call - bs_call)
            put_err.append(put - bs_put)
        rows.append(
            (n, sqrt(np.mean(np.square(call_err))), sqrt(np.mean(np.square(put_err))))
        )
        print(f"N={n:>11,}  call RMS error={rows[-1][1]:.2e}  put RMS error={rows[-1][2]:.2e}")
    return np.array(rows)


def plot(data: np.ndarray) -> None:
    n = data[:, 0]
    call_std, put_std = payoff_std()

    plt.figure(figsize=(7, 4.5))
    plt.loglog(n, call_std / np.sqrt(n), "--", color="tab:blue", alpha=0.6,
               label=r"Call: predicted $\sigma_{\mathrm{payoff}}/\sqrt{N}$")
    plt.loglog(n, put_std / np.sqrt(n), "--", color="tab:orange", alpha=0.6,
               label=r"Put: predicted $\sigma_{\mathrm{payoff}}/\sqrt{N}$")
    plt.loglog(n, data[:, 1], "o", color="tab:blue", label="Call: measured RMS error")
    plt.loglog(n, data[:, 2], "s", color="tab:orange", label="Put: measured RMS error")
    plt.title("Convergence to the Black-Scholes price")
    plt.xlabel("Number of paths, N")
    plt.ylabel("Pricing error")
    plt.grid(True, which="major", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./plots/convergence_black_scholes.svg")


def main() -> None:
    bs_call, bs_put = black_scholes()
    print(f"Black-Scholes: call={bs_call:.6f}, put={bs_put:.6f}")
    data = measure()
    np.savetxt("./data/convergence.dat", data, header="N call_rms_error put_rms_error")

    slope_call = np.polyfit(np.log(data[:, 0]), np.log(data[:, 1]), 1)[0]
    slope_put = np.polyfit(np.log(data[:, 0]), np.log(data[:, 2]), 1)[0]
    print(f"Fitted convergence order: call={slope_call:.3f}, put={slope_put:.3f} (expected -0.5)")
    plot(data)


if __name__ == "__main__":
    main()
