import pandas as pd

def summary_report(df: pd.DataFrame) -> None:
    """
    Loads merged_data.csv and prints key summary statistics:
      1. Top correlations between cost and quality.
      2. Top/bottom 5 states by mean payment and mean rating.
      3. Top 5 highest‐ and lowest‐cost cities (by avg payment) with their mean ratings.
      4. Counts of outliers and anomalies from previous flags (if present).
      5. Cluster size distribution from PCA/KMeans (if present).
    """
    # 1. Correlations
    num = df.select_dtypes(include="number")
    corr = num.corr()
    if "rating" in corr:
        print("\n=== Top 5 Positive Correlations with 'rating' ===")
        print(corr["rating"].drop("rating").sort_values(ascending=False).head(5))
        print("\n=== Top 5 Negative Correlations with 'rating' ===")
        print(corr["rating"].drop("rating").sort_values().head(5))

    # 2. State‐level payment & rating
    if {"facility_state", "Avg_Tot_Pymt_Amt", "rating"}.issubset(df.columns):
        state_stats = (
            df.groupby("facility_state")
              .agg(mean_payment=("Avg_Tot_Pymt_Amt","mean"),
                   mean_rating=("rating","mean"))
        )
        print("\n=== Top 5 States by Mean Payment ===")
        print(state_stats["mean_payment"].sort_values(ascending=False).head(5))
        print("\n=== Bottom 5 States by Mean Payment ===")
        print(state_stats["mean_payment"].sort_values().head(5))
        print("\n=== Top 5 States by Mean Rating ===")
        print(state_stats["mean_rating"].sort_values(ascending=False).head(5))
        print("\n=== Bottom 5 States by Mean Rating ===")
        print(state_stats["mean_rating"].sort_values().head(5))

    # 3. City‐level cost & rating
    if {"facility_city", "Avg_Tot_Pymt_Amt", "rating"}.issubset(df.columns):
        city_stats = (
            df.groupby("facility_city")
              .agg(mean_payment=("Avg_Tot_Pymt_Amt","mean"),
                   mean_rating=("rating","mean"))
              .dropna()
        )
        print("\n=== Top 5 Highest‐Cost Cities ===")
        print(city_stats["mean_payment"].sort_values(ascending=False).head(5))
        print("\n=== Top 5 Lowest‐Cost Cities ===")
        print(city_stats["mean_payment"].sort_values().head(5))

    # 4. Outlier/anomaly counts
    if "outlier_iqr" in df.columns:
        print(f"\nIQR Outliers: {df['outlier_iqr'].sum()} of {len(df)} rows")
    if "anomaly_iforest" in df.columns:
        print(f"IsolationForest Anomalies: {df['anomaly_iforest'].sum()} of {len(df)} rows")

    # 5. Cluster distribution
    if "cluster" in df.columns:
        print("\n=== Cluster Size Distribution ===")
        print(df["cluster"].value_counts().sort_index())