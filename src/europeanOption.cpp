#include "../include/europeanOption.hpp"
#include <algorithm>
#include <stdexcept>

EuropeanOption::EuropeanOption(double initStockPrice, double strikePrice,
                               double riskFreeIntRate, double volatility,
                               double timeToExpire, unsigned int seed)
    : m_S0{initStockPrice}, m_K{strikePrice}, m_r{riskFreeIntRate},
      m_sigma{volatility}, m_T{timeToExpire}, m_seed{seed}, m_generator{seed} {

  if (volatility < 0) {
    throw std::invalid_argument("volatility can only be a positive value");
  }
  if ((initStockPrice < 0) || (strikePrice < 0)) {
    throw std::invalid_argument(
        "initStockPrice and strikePrice can only be a positive value");
  }
  if (timeToExpire < 0) {
    throw std::invalid_argument("timeToExpire can only be a positive value");
  }
}

EuropeanOption::EuropeanOption(double initStockPrice, double strikePrice,
                               double riskFreeIntRate, double volatility,
                               double timeToExpire)
    : EuropeanOption(initStockPrice, strikePrice, riskFreeIntRate, volatility,
                     timeToExpire, std::random_device()()) {}

double EuropeanOption::_calculateST(double Z) const {
  // the analytic solution for Geometric Brownian motion (GMB)
  return m_S0 * std::exp((m_r - 0.5 * (m_sigma * m_sigma)) * m_T +
                         (m_sigma * std::sqrt(m_T) * Z));
}
std::pair<double, double>
EuropeanOption::calculatePrice(int numSimulations) const {
  m_generator.seed(m_seed);
  std::normal_distribution<double> randGaussian(0.0, 1.0);
  double payoffCall{0.0};
  double payoffPut{0.0};

  for (int i = 0; i < numSimulations; i++) {
    double randGaussianNum = randGaussian(m_generator);
    double pricePath = _calculateST(randGaussianNum);

    // Calculates the pay off for call and put options
    payoffCall += std::max((pricePath - m_K), 0.0);
    payoffPut += std::max((m_K - pricePath), 0.0);
  }

  // Takes the average of each payoff and multiplies it by the discounted rate
  // passes into the pair to be returned
  double avgPayoffCall = payoffCall / static_cast<double>(numSimulations);
  double avgPayoffPut = payoffPut / static_cast<double>(numSimulations);
  double discounted{std::exp(-m_r * m_T)};

  return std::make_pair(avgPayoffCall * discounted, avgPayoffPut * discounted);
}
