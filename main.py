# Summary:
# First solve PDE 3.3 to get the reservation bid and ask.

# "Indifference Price, also known as Reservation Price or 
# Private Valuation, refers to the specific price at which 
# an individual is indifferent between buying or selling an 
# asset, or between alternative investments."

# Second solve the implicit eqautions 3.6 and 3.7 to obtain 
# the optimial distances between mid price and optimal bid and 
# ask quotes.


# ================================
from brownian_motion import generate_midprice
import matplotlib.pyplot as plt
import numpy as np

# First we obtain the indifference bid and ask prices using the average of the suboptimial bid and ask prices
# for both rb and ra

s = 100
T = 1.0
sigma = 2
var = sigma*sigma

points = 1000
q = 0
gamma = 0.1
k = 1.5
M = 0.5
cash = 0

# duplicate code fix later
t : np.ndarray = np.linspace(0, T, points)
dt = t[1] - t[0]

# arrival parameter
A = np.exp(-k * M/2) / dt
S = generate_midprice(s, sigma, T, point_count=points, path_count=1000)
rng : np.random.Generator = np.random.default_rng(seed=12345)
for path in S:
    q = 0
    cash = 0
    arrival_bid = np.zeros_like(path)
    arrival_ask= np.zeros_like(path)

    profits = []
    final_qs = []

    for i in range(len(path)):
        r = path - q * gamma * var * (T - t[i])

        db = gamma * q * var * (T - t[i]) + 1/gamma * np.log(1 + gamma/k)
        da = -gamma * q * var * (T - t[i]) + 1/gamma * np.log(1 + gamma/k)

        bid_price = path[i] - db
        ask_price = path[i] + da

        arrival_bid[i] = A * np.exp(-k * db)
        arrival_ask[i] = A * np.exp(-k * da)

        p_bid = arrival_bid[i] * dt
        p_ask = arrival_ask[i] * dt

        if rng.uniform(0, 1) < p_bid:
            q += 1
            cash -= bid_price

        if rng.uniform(0, 1) < p_ask:
            q -= 1
            cash += ask_price

    profit = cash + q * path[-1]  
    profits.append(profit)
    final_qs.append(q)

print("Mean profit:", np.mean(profits), "Std:", np.std(profits))
print("Mean final q:", np.mean(final_qs), "Std:", np.std(final_qs))
        
        










