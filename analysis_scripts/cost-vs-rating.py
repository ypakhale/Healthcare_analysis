import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def cost_rating_correlation(df: pd.DataFrame,
                            cost_col: str = "Avg_Tot_Pymt_Amt",
                            rating_col: str = "rating"):
    """
    1. Computes Pearson and Spearman correlations between cost and rating.
    2. Prints correlation coefficients and p-values.
    3. Plots a scatter of cost vs. rating with a linear fit line.
    """
    # 1. Drop rows with missing cost or rating    
    sub = df[[cost_col, rating_col]].dropna()
    cost = sub[cost_col].values
    rating = sub[rating_col].values

    # 2. Compute correlations
    pearson_r, pearson_p = stats.pearsonr(cost, rating)
    spearman_rho, spearman_p = stats.spearmanr(cost, rating)

    print(f"Pearson r = {pearson_r:.3f}, p-value = {pearson_p:.3e}")
    print(f"Spearman ρ = {spearman_rho:.3f}, p-value = {spearman_p:.3e}")

    # 3. Scatter + regression line
    plt.figure(figsize=(6, 6))
    plt.scatter(cost, rating, alpha=0.5, edgecolor='k', linewidth=0.3)
    # Fit least-squares line
    m, b = np.polyfit(cost, rating, 1)
    x_line = np.linspace(cost.min(), cost.max(), 100)
    plt.plot(x_line, m * x_line + b, linestyle='--', linewidth=2,
             label=f"fit: y = {m:.2e}x + {b:.2f}")
    plt.xlabel(cost_col)
    plt.ylabel(rating_col)
    plt.title(f"{cost_col} vs. {rating_col}")
    plt.legend()
    plt.tight_layout()
    plt.show()