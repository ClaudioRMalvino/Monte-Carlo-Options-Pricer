#pragma once
#include <random>
#include <utility>

class EuropeanOption {
public:
  // --- The Constructor ---
  // This is how we create an option.
  // We need to pass in all its parameters.
  EuropeanOption(double initStockPrice, double strikePrice,
                 double riskFreeIntRate, double volatility,
                 double timeToExpire);

  EuropeanOption(double initStockPrice, double strikePrice,
                 double riskFreeIntRate, double volatility, double timeToExpire,
                 unsigned int seed);

  // --- The "Worker" Method ---
  // This will run the Monte Carlo simulation.
  // It takes the number of paths to simulate as an argument.
  std::pair<double, double> calculatePrice(int numSimulations) const;

private:
  // --- Member Variables ---
  // What data does our class need to hold?
  // We need to store all the parameters that are
  // passed into the constructor.

  const double m_S0;
  const double m_K;
  const double m_r;
  const double m_sigma;
  const double m_T;
  // --- The "Engine" ---
  // We can also store our random number generator
  // as a private member, so it's ready to be used.
  mutable std::mt19937 m_generator;

  double _calculateST(double Z) const;
};
