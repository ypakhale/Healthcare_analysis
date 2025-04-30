import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def state_cost_rating_analysis(
    df: pd.DataFrame,
    cost_col: str = "Avg_Tot_Pymt_Amt",
    rating_col: str = "rating",
    min_count: int = 20
) -> pd.DataFrame:
    """
    For each state with at least `min_count` valid cost–rating pairs:
      1. Computes Pearson and Spearman correlations.
      2. Fits a least-squares regression line.
      3. Plots cost vs. rating scatter with the regression line and annotates r & p.
    Returns a DataFrame of state‐level metrics:
      state, n, pearson_r, pearson_p, spearman_rho, spearman_p, slope, intercept
    """
    records = []
    for state, group in df.groupby("facility_state"):
        sub = group[[cost_col, rating_col]].dropna()
        n = len(sub)
        if n < min_count:
            continue

        cost = sub[cost_col].values
        rating = sub[rating_col].values

        # Correlations
        pearson_r, pearson_p = stats.pearsonr(cost, rating)
        spearman_rho, spearman_p = stats.spearmanr(cost, rating)

        # Regression fit
        slope, intercept = np.polyfit(cost, rating, 1)
        x_line = np.linspace(cost.min(), cost.max(), 100)

        # Plot
        plt.figure(figsize=(6, 6))
        plt.scatter(cost, rating, alpha=0.5, edgecolor="k", linewidth=0.3)
        plt.plot(x_line, slope * x_line + intercept,
                 linestyle="--", linewidth=2,
                 label=f"y = {slope:.2e}x + {intercept:.2f}")
        plt.xlabel(cost_col)
        plt.ylabel(rating_col)
        plt.title(f"{state} (n={n})\nPearson r={pearson_r:.2f}, p={pearson_p:.2e}")
        plt.legend()
        plt.tight_layout()
        plt.show()

        records.append({
            "state": state,
            "n": n,
            "pearson_r": pearson_r,
            "pearson_p": pearson_p,
            "spearman_rho": spearman_rho,
            "spearman_p": spearman_p,
            "slope": slope,
            "intercept": intercept
        })

    results = pd.DataFrame(records).sort_values("pearson_r", ascending=False)
    print("\n=== State‐Level Correlation Metrics ===")
    print(results[["state","n","pearson_r","pearson_p","spearman_rho","spearman_p"]]
          .to_string(index=False,
                     formatters={
                         "pearson_r":"{:.3f}".format,
                         "pearson_p":"{:.2e}".format,
                         "spearman_rho":"{:.3f}".format,
                         "spearman_p":"{:.2e}".format
                     }))
    
    
    return results
