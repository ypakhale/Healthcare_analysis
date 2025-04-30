import pandas as pd
import matplotlib.pyplot as plt

def bivariate_analysis(
    df: pd.DataFrame,
    numeric_cols: list[str] | None = None,
    scatter_pairs: list[tuple[str, str]] | None = None,
    cat_group_cols: list[str] | None = None
) -> pd.DataFrame:
    """
    1. Prints and plots the correlation matrix for numeric columns.
    2. Generates scatter plots for specified column pairs.
    3. Creates boxplots of Avg_Tot_Pymt_Amt and rating grouped by categorical columns.
    
    Parameters:
        df: pandas DataFrame
        numeric_cols: list of numeric column names (defaults to all numeric columns)
        scatter_pairs: list of (x, y) column pairs for scatter plots
        cat_group_cols: list of categorical columns for boxplots
    Returns:
        corr: the correlation DataFrame
    """
    # 1. Determine numeric columns
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
    
    # 2. Correlation matrix
    corr = df[numeric_cols].corr()
    print("\n=== Correlation Matrix ===")
    print(corr, end="\n\n")
    
    # 3. Plot heatmap of correlations
    plt.figure(figsize=(10, 8))
    plt.imshow(corr, aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns, rotation=90)
    plt.yticks(range(len(corr)), corr.index)
    plt.title("Correlation Matrix Heatmap")
    plt.tight_layout()
    plt.show()
    
    # 4. Scatter plots
    if scatter_pairs is None:
        scatter_pairs = [
            ("Avg_Tot_Pymt_Amt", "rating"),
            ("Avg_Mdcr_Pymt_Amt", "Avg_Submtd_Cvrd_Chrg")
        ]
    for x_col, y_col in scatter_pairs:
        if x_col in df.columns and y_col in df.columns:
            plt.figure(figsize=(6, 4))
            plt.scatter(df[x_col], df[y_col], alpha=0.5)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f"Scatter: {x_col} vs. {y_col}")
            plt.tight_layout()
            plt.show()
    
    # 5. Boxplots by categorical group
    if cat_group_cols is None:
        cat_group_cols = ["payment_category", "value_of_care_category"]
    for cat in cat_group_cols:
        if cat in df.columns:
            if "Avg_Tot_Pymt_Amt" in df.columns:
                plt.figure(figsize=(8, 6))
                df.boxplot(column="Avg_Tot_Pymt_Amt", by=cat, rot=45)
                plt.suptitle("")
                plt.title(f"Avg_Tot_Pymt_Amt by {cat}")
                plt.xlabel(cat)
                plt.ylabel("Avg_Tot_Pymt_Amt")
                plt.tight_layout()
                plt.show()
            if "rating" in df.columns:
                plt.figure(figsize=(8, 6))
                df.boxplot(column="rating", by=cat, rot=45)
                plt.suptitle("")
                plt.title(f"rating by {cat}")
                plt.xlabel(cat)
                plt.ylabel("rating")
                plt.tight_layout()
                plt.show()
    
    return corr

# Run the bivariate analysis
corr_matrix = bivariate_analysis(df)
print(corr_matrix)