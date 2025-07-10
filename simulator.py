import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

np.random.seed(1)

def simulate_requests(T=100, p=0.3):
    return np.random.binomial(n=1, p=p, size=T)

def plot_requests(requests, figure_name="requests.png"):
    T = len(requests)
    plt.figure(figsize=(12,3))
    plt.stem(range(1, T+1), requests, basefmt=" ")
    plt.title(f"Request Arrival Pattern")
    plt.xlabel("Time Slot")
    plt.ylabel("Request (1=Yes, 0=No)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(figure_name)
    # plt.show()
    plt.close()
    

def get_sensor_value():
    return np.random.uniform(1, 100)

def store_to_cache(value, t):
    return {'obtained_at': t, 'value': value}

def get_AOI(cache_t, t):
    return t - cache_t

def get_utility(age, f_0, lamda):
    return f_0 * np.exp(-lamda * age)

def get_utility_vector(f_0, lamda, cost):
    i = 1
    utility_vec = [f_0]
    while(1):
        utility = get_utility(i, f_0, lamda)
        if (utility > cost):
            utility_vec.append(utility)
        else:
            break
        i+=1
    return utility_vec