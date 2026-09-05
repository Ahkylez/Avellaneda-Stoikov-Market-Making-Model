# Find the midprice of the stock
from enum import Enum
import numpy as np

class MotionType(str, Enum):
    ARITHMETIC = "arithmetic"
    GEOMETRIC = "geometric"

def _generate_brownian_motion(dt: float, point_count: int, seed: float | None, path_count : int = 1) -> np.ndarray:
    """
    Generates a brownian motion with the given time steps and dt.
    """
    rng : np.random.Generator = np.random.default_rng(seed)
    Z : np.ndarray = rng.normal(loc=0.0, scale=1.0, size=(path_count, point_count))
    dW = np.sqrt(dt) * Z

    dW[:, 0] = 0

    Wt = np.cumsum(dW, axis=1) # this gives the actual points of the brownian motion

    return Wt


def generate_midprice(motion_type: MotionType, dt: float, initial_price : float, volatility : float, time_horizon : float, seed: float | None, path_count : int = 1, point_count : int = 1000) -> np.ndarray:
    """
    Uses Arithmetic Brownian Motion to model a stock. Uses arithmetic brownian motion for now.

    S_t = s + sigma * W_t 

    Where W_t = sqrt(dt) * Z
    """
    Wt = _generate_brownian_motion(dt=dt, point_count=point_count, seed=seed, path_count=path_count)

    if motion_type == MotionType.ARITHMETIC:
        S = initial_price + volatility * Wt
    elif motion_type == MotionType.GEOMETRIC:
        t = np.arange(point_count) * dt
        S = initial_price * np.exp((-volatility**2/2) * t + volatility * Wt)
    else:
        raise ValueError(f"Invalid motion type: {motion_type}")
    return S




if __name__ == "__main__":
    seed : int = 1234
    paths : int = 1
    points : int = 100
    initial_price : float = 100
    sigma : float = 0.20
    T : float = 1.0


    import matplotlib.pyplot as plt
    S = generate_midprice(motion_type=MotionType.GEOMETRIC, dt=T/points, initial_price=initial_price,
                        volatility=sigma, time_horizon=T, seed=seed, path_count=paths, point_count=points)
    plt.figure()
    for i in range(paths):
        plt.plot(S[i])
    plt.title("Geometric Brownian Motion")
    plt.xlabel("Time Steps")
    plt.ylabel("Price")
    plt.savefig("geometric_brownian_motion.png")

    S = generate_midprice(motion_type=MotionType.ARITHMETIC, dt=T/points, initial_price=initial_price,
                        volatility=sigma, time_horizon=T, seed=seed, path_count=paths, point_count=points)
    plt.figure()
    for i in range(paths):
        plt.plot(S[i])
    plt.title("Arithmetic Brownian Motion")
    plt.xlabel("Time Steps")
    plt.ylabel("Price")
    plt.savefig("arithmetic_brownian_motion.png")


