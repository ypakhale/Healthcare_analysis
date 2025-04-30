"""
Central orchestration script to run full pipeline of data analysis and visualization.
"""

import pandas as pd
from analysis_scripts.basic_eda import data_type_checks, identical_rows_analysis, missing_value_analysis
from analysis_scripts.univariate import univariate_analysis
from analysis_scripts.bivariate import bivariate_analysis
from analysis_scripts.cost_vs_rating import cost_rating_correlation
from analysis_scripts.cost_vs_rating_states import state_cost_rating_analysis
from analysis_scripts.geographical import geographic_analysis
from analysis_scripts.outlier import outlier_anomaly_detection
from analysis_scripts.multivariate_dim_red import multivariate_dimensionality_reduction
from analysis_scripts.summary import summary_report




# === Load data ===
df = pd.read_csv("./data/processed/merged_healthcare_data.csv")
df = df.dropna(axis=1, how="all")
filtered_df = df.dropna(subset=["Avg_Submtd_Cvrd_Chrg", "rating"])

# === Basic EDA ===

filtered_df = data_type_checks(filtered_df)
identical_rows_analysis(filtered_df)
missing_value_analysis(filtered_df)


univariate_analysis(filtered_df)
bivariate_analysis(filtered_df)

# === Cost vs Rating ===
cost_rating_correlation(filtered_df)
state_cost_rating_analysis(filtered_df)

# === Geographic Patterns ===
geographic_analysis(filtered_df)

# === Outlier Detection ===
filtered_df = outlier_anomaly_detection(filtered_df)

# === PCA & Clustering ===
pca_results = multivariate_dimensionality_reduction(filtered_df)
if not pca_results.empty:
    filtered_df = pd.concat([filtered_df, pca_results], axis=1)

# === Summary Report ===
summary_report(filtered_df)