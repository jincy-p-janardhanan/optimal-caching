import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from simulator import *

def fixed_n(n=5):
    return n

def plot_hn_vs_n(h, n_opt, figname):
    x_vals = list(range(1, len(h) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, h, marker='o', markersize=5)
    plt.vlines(x=n_opt, ymin=min(h) - 0.15, ymax=h[n_opt - 1], colors='red', linewidth=1)
    plt.text(n_opt, min(h) - 0.18, f'{n_opt}', color='red',
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
def get_n(utility_vec, p, f_0, C, plot=True, figname="h_n vs n.png"):
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
    
    if plot == True:
        plot_hn_vs_n(h, n_opt, figname)
    
    return n_opt, h

# ALGO 2 - Online Policy (Learning Utility Vector to compute n*)
def learn_f_to_get_n(t_max, n_max, p, C, f_0, lamda, plot=True):
    t = 1
    fetch = 0
    age = 0
    n_opt = 0
    learn = list(range(1, n_max+1))
    utility_vec = [0] * (n_max+1)    
    R = [0] * (t_max+1)
    
    M, T = 0, 0

    while(t <= t_max):
        x_t = simulate_requests(1, p)[0]
        if x_t == 1:
            if age == 0:
                utility_vec[0] = f_0
                fetch += 1
                R[t] = f_0 - C['C1']
            elif age in learn:
                utility_vec[age] = get_utility(age, f_0, lamda)
                learn.remove(age)
                R[t] = utility_vec[age] - C['C2']
                
            age = (age + 1) if age < n_max else 0
            
        elif age > 0 and age <= n_max:
            age = (age + 1) if age < n_max else 0
            R[t] = -C['C2']
        
        else:
            R[t] = 0
        
        if age == 0 and len(learn) == 0  and n_opt == 0:
            n_opt, _ = get_n(utility_vec, p, f_0, C, figname="h_n vs n-algo2.png")
            n_max = n_opt
            M = fetch
            T = t
        
        t += 1
        
    return n_opt, R, M, T
