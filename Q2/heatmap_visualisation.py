import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

with open("results/results.json", "r") as f:
    results = json.load(f)

K_values = ["K=10", "K=100", "K=1000"]

# Line Plot

fig_line, axes_line = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for idx, K in enumerate(K_values):
    ax = axes_line[idx]
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

fig_line.suptitle("Tabu Search Results - Line Plots")
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.savefig('results/tabu_search_results_line.png')

# Heatmap

fig_heatmap, axes_heatmap = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for idx, K in enumerate(K_values):
    ax = axes_heatmap[idx]
    data = []

    for gamma_key, L_results in results[K].items():
        gamma = int(gamma_key.split('=')[1])
        for L_key, g_best in L_results.items():
            L = int(L_key.split('=')[1])
            data.append((gamma, L, g_best))

    df = pd.DataFrame(data, columns=["gamma", "L", "g_best"])
    pivot = df.pivot(index="gamma", columns="L", values="g_best")

    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", cbar=True)
    ax.set_title(f"K = {K.split('=')[1]}")
    ax.set_xlabel("L")
    ax.set_ylabel("gamma")
    ax.invert_yaxis()  

fig_heatmap.suptitle("Tabu Search Results - Heatmaps")
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.savefig('results/tabu_search_results_heatmap.png')

print("Plots saved: Line plots and heatmaps.")
