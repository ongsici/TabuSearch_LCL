import json
import matplotlib.pyplot as plt

with open("results/results.json", "r") as f:
    results = json.load(f)

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
K_values = ["K=10", "K=100", "K=1000"]

for idx, K in enumerate(K_values):
    ax = axes[idx]
    for gamma_key, L_results in results[K].items():
        gamma = int(gamma_key.split('=')[1]) 
        L_values = [int(L.split('=')[1]) for L in L_results.keys()]
        g_best_values = list(L_results.values())
        
        L_values, g_best_values = zip(*sorted(zip(L_values, g_best_values)))

        ax.plot(L_values, g_best_values, marker='o', label=f'gamma={gamma}')
    
    ax.set_title(f"K = {K.split('=')[1]}")
    ax.set_xlabel("L")
    ax.set_ylabel("g_best" if idx == 0 else "")
    ax.legend()

fig.suptitle("Tabu Search Results")
plt.tight_layout()
plt.subplots_adjust(top=0.9) 
plt.savefig('results/tabu_search_results.png')
