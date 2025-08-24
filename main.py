from simulator import *
from optimal_caching import *
import pandas as pd
import seaborn as sns
import sys
import json

if len(sys.argv) < 3:
    print("Usage: python3 main.py <simulator_params_file.json>  'algo1'|'algo2'|'algo3'|'algo4'")
    sys.exit(1)

sim_params_file = sys.argv[1]

try:
    with open(sim_params_file, 'r') as file:
        sim_params_list = json.load(file)
except FileNotFoundError:
    print(f"Error: File '{sim_params_file}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

Ts = list(range(100, 1001, 100))
ps = [i / 10 for i in range(1, 11)]
rewards = []
result = []
# print(Ts)
# print(ps)

if sys.argv[2] == 'algo4':
    for sim_params in sim_params_list:
        # print(json.dumps(sim_params, indent=4))
        with open("requests.txt", "w") as f:
            for p in ps:
                get_n_ucb_utility(1000, sim_params['n_max'], p, sim_params['C'], sim_params['f_0'], sim_params['lamda'])
                print("__________________________________________\n")
    sys.exit(0)                
                    
                    
for sim_params in sim_params_list:
    # print(json.dumps(sim_params, indent=4))
    with open("requests.txt", "w") as f:
        for p in ps:
            for T in Ts:
                requests = simulate_requests(T, p)
                # plot_requests(requests, f"requests_T-{T}_p-{p}.png")
                f.write("".join(str(r) for r in requests) + "\n")

                if sys.argv[2] == 'algo1':
                    utility_vec = get_utility_vector(sim_params['f_0'], sim_params['lamda'], sim_params['C']['C1'] + sim_params['C']['C2'])
                    n, _ = get_n(utility_vec, p, sim_params['f_0'], sim_params['C'], False)
                elif sys.argv[2] == 'algo2':
                    n, r, m, _ = learn_f_to_get_n(sim_params['t_max'], sim_params['n_max'], p, sim_params['C'], sim_params['f_0'], sim_params['lamda'], False)
                elif sys.argv[2] == 'algo3':
                    n, r, m, _, _ = get_n_with_early_est(sim_params['t_max'], sim_params['n_max'], p, sim_params['C'], sim_params['f_0'], sim_params['lamda'], False)
                else:
                    print("Invalid algorithm parameter.")
                    break
                    
                reward, _ = simulate_policy_evaluation(T, requests, sim_params['C'], sim_params['lamda'], sim_params['f_0'], n)
                rewards.append(reward)
                print(f"T:{T}, p:{p}, n_opt:{n} avg_reward:{reward}")
                result.append({
                    "T": T,
                    "p": p,
                    "sim_params": sim_params,
                    "requests": requests.tolist(),
                    "reward": reward
                })
            print("__________________________________________\n")
                
with open("simulation_results.json", "w") as f:
    json.dump(result, f, indent=2)

df = pd.DataFrame(result)
pivot_table = df.pivot_table(index="T", columns="p", values="reward")

if len(sim_params_list) == 1:
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Average Reward Heatmap (T vs p)")
    plt.xlabel("p")
    plt.ylabel("T")
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"T vs p - {sys.argv[2]}.png", dpi=300)
    plt.close()