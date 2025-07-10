import matplotlib.pyplot as plt

def fixed_n(n=5):
    return n

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
        plt.plot(range(1, len(h)+1), h, marker='o')
        plt.xlabel('n (cache duration)')
        plt.ylabel('Expected reward per time slot (h[n])')
        plt.title('Optimal Cache Duration')
        plt.grid(True)
        plt.savefig('h_n vs n.png')
        # plt.show()
        plt.close()
    
    return n_opt, h
