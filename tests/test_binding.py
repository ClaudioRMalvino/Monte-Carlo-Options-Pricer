
import monte_carlo_pricer

def main():
    print("--- Successfully imported C++ module! ---")

    option_random = monte_carlo_pricer.EuropeanOption(
        initStockPrice=100.0,
        strikePrice=100.0,
        riskFreeIntRate=0.05,
        volatility=0.20,
        timeToExpire=1.0,
    )

    option_test = monte_carlo_pricer.EuropeanOption(
        initStockPrice=100.0,
        strikePrice=100.0,
        riskFreeIntRate=0.05,
        volatility=0.20,
        timeToExpire=1.0,
        seed=42,
    )

    print("Calculating with 10M simulations...")
    call_price, put_price = option_test.calculatePrice(10000000)
    rand_call_price, rand_put_price = option_random.calculatePrice(100000000)

    print("--- Results ---")
    print(f"  Call Price: {call_price:.2f}")
    print(f"  Put Price:  {put_price:.2f}")
    print(f"  Call Price (random): {rand_call_price:.2f}")
    print(f"  Put Price (random):  {rand_put_price:.2f}")


if __name__ == "__main__":
    main()
