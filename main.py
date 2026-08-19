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
#dt = 0.005
points = 1000
q = 0
gamma = 0.1
k = 1.5
M = 0.5

#S = generate_midprice(s, sigma, T, point_count=int(T/dt) + 1)
S = generate_midprice(s, sigma, T, point_count=points)

#t : np.ndarray = np.linspace(0, T, int(T/dt) + 1)
t : np.ndarray = np.linspace(0, T, points)

r = S[0] - q * gamma * var * (T - t)

db = gamma * q * var * (T - t) + 1/gamma * np.log(1 + gamma/k)
da = -gamma * q * var * (T - t) + 1/gamma * np.log(1 + gamma/k)

plt.figure(figsize=(16, 8))
plt.plot(t, S[0], label="Mid-Price", color="black")
plt.plot(t, r, label="Indifference/Reservation Price", color="blue", linestyle="--")
plt.scatter(t, S[0] + da, label="Optimal Ask", color="red", marker="*")
plt.scatter(t, S[0] - db, label="Optimal Bid", color="green", marker="o")

plt.title("Avellaneda-Stoikov Inventory Strategy")
plt.xlabel("Time (Years)")
plt.ylabel("Price")
plt.legend()
plt.savefig("market_plot.png")
print(db)



# r = s - q * gamma * var * (T - t)

# db = gamma * q * var * (T - t) + 1/gamma









