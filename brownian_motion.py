# Find the midprice of the stock
import numpy as np
import matplotlib.pyplot as plt


def generate_midprice(initial_price : float, volatility : float, time_horizon : float, seed : float | None, path_count : int = 1, point_count : int = 1000) -> np.ndarray:
    """
    Uses brownian motion to model a stock. Uses arthmetic brownian motion for now.

    S_t = s + sigma * W_t 

    Where W_t = sqrt(dt) * Z
    """

    t : np.ndarray = np.linspace(0, time_horizon, point_count)
    dt = t[1] - t[0]
    rng : np.random.Generator = np.random.default_rng(seed)
    
    Z : np.ndarray = rng.normal(loc=0.0, scale=1.0, size=(path_count, point_count))

    dW = np.sqrt(dt) * Z

    # make sure inital price is actually the inital price.
    dW[:, 0] = 0
    
    Wt = np.cumsum(dW, axis=1) # this gives the actual points of the brownian motion
    
    S = initial_price + volatility * Wt
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
    T : float = 2.0

    generate_midprice(seed=seed, path_count=paths, time_horizon=T, point_count=points,  initial_price=initial_price, volatility=sigma)









