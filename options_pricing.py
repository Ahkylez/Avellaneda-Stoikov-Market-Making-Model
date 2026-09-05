import numpy as np
from scipy.stats import norm

def _black_scholes(S : np.ndarray, K : float, T : float, r : float, sigma : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Copied directly from:
    https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model#Black%E2%80%93Scholes_formula
    """
    sqrt_T = np.sqrt(T)

    dplus = 1/(sigma * sqrt_T) * (np.log(S / K) + (r + 0.5 * sigma * sigma) * T)
    dminus = dplus - sigma * sqrt_T

    return dplus, dminus

def call_price(S : np.ndarray, K : float, T : float, r : float, sigma : float) -> np.ndarray:
    """
    T is time till experation
    """

    if T <= 0:
        return np.maximum(S - K, 0) # Option has expired

    # Non dividend paying 
    dplus, dminus = _black_scholes(S, K, T, r, sigma)
    cost = norm.cdf(dplus) * S - norm.cdf(dminus) * K * np.exp(-r*T)
    return cost

if __name__ == "__main__":
    S = 100
    K = 100
    T = 1.0
    r = 0
    sigma = 0.2

    from brownian_motion import generate_midprice, MotionType
    S = generate_midprice(motion_type=MotionType.GEOMETRIC, dt=T/100, initial_price=S, volatility=sigma, seed=1234, path_count=1, point_count=100)


    price = call_price(S, K, T, r, sigma)

    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(price[0])
    plt.title("Options Price Over Time")
    plt.xlabel("Time Steps")
    plt.ylabel("Price")
    plt.savefig("options_price.png")
