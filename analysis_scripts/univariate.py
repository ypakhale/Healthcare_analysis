import pandas as pd
import matplotlib.pyplot as plt

def univariate_analysis(
    df: pd.DataFrame,
    numeric_cols: list[str] | None = None,
    categorical_cols: list[str] | None = None
):
    """
    1. Prints descriptive statistics for numeric columns.
    2. Plots histograms and boxplots for each numeric column.
    3. Prints top-20 value counts for categorical columns and plots bar charts.
    
    Parameters:
        df: your pandas DataFrame
        numeric_cols: list of column names to treat as numeric;
                      by default, inferred via df.select_dtypes(include='number')
        categorical_cols: list of column names to treat as categorical;
                          by default, inferred via df.select_dtypes(include=['object','category'])
    """
    # 1. Infer columns if not provided
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if categorical_cols is None:
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 2. Numeric summaries
    print("\n=== Numeric Descriptive Statistics ===")
    desc = df[numeric_cols].describe().transpose()
    print(desc)
    
    # 3. Histograms and boxplots for numeric columns
    for col in numeric_cols:
        # Histogram
        plt.figure(figsize=(6, 4))
        df[col].hist(bins=30)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
        
        # Boxplot
        plt.figure(figsize=(4, 6))
        df.boxplot(column=col)
        plt.title(f"Boxplot of {col}")
        plt.ylabel(col)
        plt.tight_layout()
        plt.show()
    
    # 4. Categorical counts and bar charts
    for col in categorical_cols:
        counts = df[col].value_counts().head(20)
        if counts.empty:
            continue
        print(f"\n=== Top 20 categories for {col} ===")
        print(counts.to_string())
        
        plt.figure(figsize=(8, 4))
        counts.plot(kind="bar")
        plt.title(f"Top 20 Categories: {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

univariate_analysis(df)