from dataclasses import dataclass
import numpy as np
from brownian_motion import generate_midprice

@dataclass
class ModelParameters:
    simulations : int
    s : float           # Inital Price
    T : float           # Time horizon
    sigma : float       # Volatility
    N : int             # Amount of points in the path
    init_q : int        # Inital Inventory
    gamma : float       # Risk aversion parameter
    k : float           # Represents the liquidity of the market
    M : float           # Represent Market Spread, ie. the difference between the best bid and ask
    init_cash : float   # Inital Cash to invest

@dataclass
class SimulationResults:
    S : np.ndarray
    t : np.ndarray
    reservations : np.ndarray
    bid_prices : np.ndarray
    ask_prices : np.ndarray
    bid_arrive : np.ndarray
    ask_arrive : np.ndarray
    profits : np.ndarray
    final_q : np.ndarray


def run_avellaneda_model(p : ModelParameters, seed: int) -> SimulationResults:
    rng : np.random.Generator = np.random.default_rng(seed=seed)
    var = p.sigma*p.sigma

    dt = p.T/p.N
    t : np.ndarray = np.linspace(0.0, p.N*dt, p.N)
    # add rng as input instead of seed. More customizable that way.
    S : np.ndarray = generate_midprice(dt=dt, initial_price=p.s, volatility=p.sigma, time_horizon=p.T, seed=seed, point_count=p.N, path_count=p.simulations)
    

    reservations = np.empty_like(S)
    bid_prices = np.empty_like(S)
    ask_prices = np.empty_like(S)

    bid_arrive = np.zeros_like(S)
    ask_arrive = np.zeros_like(S)

    profits = np.zeros(p.simulations)
    final_q = np.zeros(p.simulations)
    
    # solving for A
    A = np.exp(-p.k * p.M / 2)

    for path_idx, path in enumerate(S):
        q = p.init_q
        cash = p.init_cash

        for i in range(len(path)):
            reservations[path_idx, i] = path[i] - q * p.gamma * var * (p.T - t[i])

            db = p.gamma * q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)
            da = -p.gamma * q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)

            bid_prices[path_idx, i] = path[i] - db
            ask_prices[path_idx, i] = path[i] + da

            prob_bid = A * np.exp(-p.k * db)
            prob_ask = A * np.exp(-p.k * da)

            if prob_bid > rng.uniform(0,1):
                bid_arrive[path_idx, i] = 1
                q += 1
                cash -= bid_prices[path_idx, i]
            if prob_ask > rng.uniform(0,1):
                ask_arrive[path_idx, i] = 1
                q -= 1
                cash += ask_prices[path_idx, i]

        profits[path_idx] = cash + q * path[-1]
        final_q[path_idx] = q

    return SimulationResults(S, t, reservations, bid_prices, ask_prices, bid_arrive, ask_arrive, profits, final_q)
