import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from simulator import *

def fixed_n(n=5):
    return n

def plot_hn_vs_n(h, n_opt, figname="h_n vs n.png"):
    x_vals = list(range(1, len(h) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, h, marker='o', markersize=5)
    plt.vlines(x=n_opt, ymin=min(h) - 0.15, ymax=h[n_opt - 1], colors='red', linewidth=1)
    plt.text(n_opt, min(h) - 0.18, f'n* = {n_opt}', color='red',
            ha='center', va='top', fontsize=11)

    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))  
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  
    ax.set_xticks(range(0, max(x_vals)+3, 5))  
    plt.xlim(0, max(x_vals) + 2)
    plt.ylim(min(h) - 0.1, max(h) + 0.25)

    plt.xlabel('n (cache duration)')
    plt.ylabel('Expected reward per time slot: h(n)')
    plt.title('Optimal Cache Duration')
    plt.grid(True, which='both', linestyle=':', linewidth=0.6)
    plt.tight_layout()

    plt.savefig(figname, dpi=300)
    # plt.show()
    plt.close()

# ALGO 1 - Finding Optimal n with  Known Utility Vector
def get_n(utility_vec, p, f_0, C, plot=True):
    n = 2
    b = f_0 - C['C1']
    G = [utility_vec[1]]   #starting from age 1 since utility_vec[0] = f_0
    h = [(b + p * utility_vec[1] - C['C2'])/(1 + (1/p))]
    n_opt = 0
    
    while(n < len(utility_vec)):
        G.append(G[-1] + utility_vec[n])
        h.append( (b + p * G[-1] - n * C['C2'])/(n + (1/p)) )
        if h[-1] < h[-2] and n_opt == 0:
            n_opt = n-1
        n += 1
    
    # print(h)
    # print(n_opt)
    
    if plot == True:
        plot_hn_vs_n(h, n_opt, 'h_n_vs_n-algo1.png')
    
    return n_opt, h

# ALGO 2 - Online Policy (Learning Utility Vector to compute n*)
def learn_f_to_get_n(t_max, n_max, p, C, plot=True):
    t = 1
    i = 0
    a = 0
    n_opt = 0
    n = n_max
    while(t <= t_max):
        x_t = simulate_requests(1, p)[0]
        if x_t == 1:
            if a == 0:
                #f_0 = get
                pass

