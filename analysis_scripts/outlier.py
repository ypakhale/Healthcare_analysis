import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def outlier_anomaly_detection(
    df: pd.DataFrame,
    numeric_cols: list[str] | None = None,
    method: str = "iqr",
    contamination: float = 0.01
) -> pd.DataFrame:
    """
    1. Flags univariate outliers using the IQR method.
    2. Flags multivariate anomalies using Isolation Forest.
    Adds two boolean columns to the DataFrame:
      - 'outlier_iqr': True if any numeric value is outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
      - 'anomaly_iforest': True if detected as anomaly by IsolationForest
    Returns the DataFrame with these two new columns.
    """
    df = df.copy()
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
    # Ensure no NaNs for the methods below
    df_numeric = df[numeric_cols].fillna(df[numeric_cols].median())

    # 1. Univariate IQR outlier detection
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # Flag rows where any col is outside the [lower, upper] range
    outlier_mask = ((df_numeric < lower) | (df_numeric > upper)).any(axis=1)
    df["outlier_iqr"] = outlier_mask
    print(f"Univariate IQR outliers detected: {outlier_mask.sum()} rows")

    # 2. Multivariate anomaly detection via Isolation Forest
    iso = IsolationForest(contamination=contamination, random_state=42)
    preds = iso.fit_predict(df_numeric)
    # In sklearn IF, -1 = anomaly, 1 = normal
    anomaly_mask = (preds == -1)
    df["anomaly_iforest"] = anomaly_mask
    print(f"IsolationForest anomalies detected (contamination={contamination}): {anomaly_mask.sum()} rows")

    print(df[['outlier_iqr', 'anomaly_iforest']].sum())
    
    return df

