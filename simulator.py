import math
import numpy as np
import matplotlib.pyplot as plt
import json

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

def get_noisy_utility(age, f_0, lamda, noise_std=0.1):
    return f_0 * np.exp(-lamda * age) + np.random.normal(0, noise_std)

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

def simulate_policy_evaluation(T, requests, C, lamda, f_0, n):
    beta = f_0 - C['C1']     # instantaneous reward at the time of fetch of the file
    y_i = 0                     # number of time slots between the end of the cache period and the next request, initialized to zero
    Y = []                      # list of y_i
    
    cached_val = None           
    cumulative_utility = 0
    total_cost_incurred = 0
    t=0
    n_i = 0
    prev_t = 0
    for r in requests:
        if r == 1 and cached_val == None:
            value = get_sensor_value()
            cached_val = store_to_cache(value, t)
            cumulative_utility += beta
            cycle_cost = C['C1'] + n * C['C2']
            total_cost_incurred += cycle_cost
            # print(f"t = {t}, total cost update: {total_cost_incurred}")
            n_i = 0
            y_i = t - prev_t
            Y.append(y_i)
            
        if r == 1  and cached_val != None:
            age = get_AOI(cached_val['obtained_at'], t)
            cumulative_utility += get_utility(age, f_0, lamda)
            # print(f"t = {t}, Cumulative Utility update: {cumulative_utility}")
            n_i += 1

            
        if n_i == n and cached_val != None:
            # print(f"t = {t}, Cache reset")
            cached_val = None
            prev_t = t
            
        t+=1

    total_reward = (cumulative_utility - total_cost_incurred)/T
    # print(total_reward)
    
    return total_reward, Y