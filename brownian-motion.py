# Find the midprice of the stock
import numpy as np
import matplotlib.pyplot as plt

def generate_midprice(seed : int, path_count : int, point_count : int, initial_price : float, volatility : float) -> np.ndarray:
    T : float      = 2.0
    t : np.ndarray = np.linspace(0, T, point_count)
    dt = t[1] - t[0]

    rng : np.random.Generator = np.random.default_rng(seed=seed)
    Z : np.ndarray = rng.normal(loc=0.0, scale=1.0, size=(path_count, point_count))

    dW = np.sqrt(dt) * Z
    Wt = np.cumsum(dW, axis=1)

    S = initial_price + volatility * Wt
    plot_midprice(t, S)
    return S

def plot_midprice(t: np.ndarray, S : np.ndarray):
    for i in range(paths):
        plt.plot(t, S[i])

    plt.title("Arithmetic Brownian Motion")
    plt.xlabel("Time (Years)")
    plt.ylabel("Stock Price")
    plt.savefig("brownian_plot.png")
    print("Plot saved to brownian_plot.png")

if __name__ == "__main__":
    seed : int = 12345
    paths : int = 10
    points : int = 1000
    initial_price : float = 100
    sigma : float = 10

    generate_midprice(seed=seed, path_count=paths, point_count=points, initial_price=initial_price, volatility=sigma)

#St = s + sigma * Wt

# First we can make Wt
# Sqrt(delta t) * Z








