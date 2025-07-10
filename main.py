from simulator import *
from optimal_caching import *

T = 100                     # number of timeslots
p = 0.6                     # probability of requests
fetch_cost = 10             # alpha (per request)
cache_storage_cost = 0.5    # s (per time slot)
y_i = 0                     # number of time slots between the end of the cache period and the next request, initialized to zero
Y = []                      # list of y_i
lamda = 0.15                # decay rate for exponentially decreasing utility
f_0 = 25                    # utility of serving at the same time when value is fetched
beta = f_0 - fetch_cost     # instantaneous reward at the time of fetch of the file

utility_vec = get_utility_vector(f_0, lamda, fetch_cost + cache_storage_cost)

C = { 'C1': fetch_cost, 'C2': cache_storage_cost}

n, _ = get_n(utility_vec, p, f_0, C)               # n = number of time-slots until which cached value is retained
cached_val = None           
cumulative_utility = 0
total_cost_incurred = 0

requests = simulate_requests(T, p)
plot_requests(requests)


t=0
n_i = 0
prev_t = 0
for r in requests:
    if r == 1 and cached_val == None:
        value = get_sensor_value()
        cached_val = store_to_cache(value, t)
        cumulative_utility += beta
        cycle_cost = fetch_cost + n * cache_storage_cost
        total_cost_incurred += cycle_cost
        n_i = 0
        y_i = t - prev_t
        Y.append(y_i)
        
    if r == 1  and cached_val != None:
        age = get_AOI(cached_val['obtained_at'], t)
        cumulative_utility += get_utility(age, f_0, lamda)
        
    if n_i != 0:
        n_i += 1
        
    if n_i == n:
        cached_val = None
        prev_t = t
        
    t+=1

total_reward = (cumulative_utility - total_cost_incurred)/T
print(total_reward)
