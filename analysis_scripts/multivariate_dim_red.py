import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

def multivariate_dimensionality_reduction(
    df: pd.DataFrame,
    n_components: int = 2,
    n_clusters: int = 3
) -> pd.DataFrame:
    """
    1. Imputes missing numeric values via median.
    2. Performs PCA on all numeric columns (with guards for zero rows).
    3. Plots explained variance, 2-D projection, and KMeans clusters.
    Returns a DataFrame with PC coordinates and cluster labels (empty if skipped).
    """
    # 1. Select numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    X_raw = df[numeric_cols]

    # 2. Check for zero rows
    if X_raw.shape[0] == 0:
        print("⚠️ No rows in the dataset—skipping PCA and clustering.")
        return pd.DataFrame()

    # 3. Impute missing values
    imputer = SimpleImputer(strategy='median')
    X = imputer.fit_transform(X_raw)

    # 4. Adjust components if too many samples
    n_samples = X.shape[0]
    if n_samples < n_components:
        print(f"⚠️ Only {n_samples} samples available; reducing n_components→{n_samples}")
        n_components = n_samples

    # 5. PCA
    pca = PCA(n_components=n_components, random_state=42)
    pcs = pca.fit_transform(X)
    pc_cols = [f"PC{i+1}" for i in range(n_components)]
    df_pca = pd.DataFrame(pcs, columns=pc_cols, index=df.index)

    # 6. Explained variance plot
    plt.figure(figsize=(6, 4))
    plt.bar(range(1, n_components + 1), pca.explained_variance_ratio_)
    plt.xlabel("Principal Component")
    plt.ylabel("Explained Variance Ratio")
    plt.title("PCA Explained Variance")
    plt.xticks(range(1, n_components + 1))
    plt.tight_layout()
    plt.show()

    # 7. 2-D scatter if possible
    if n_components >= 2:
        plt.figure(figsize=(6, 6))
        plt.scatter(df_pca["PC1"], df_pca["PC2"], alpha=0.5)
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title("Projection onto First Two Principal Components")
        plt.tight_layout()
        plt.show()

    # 8. KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_pca["cluster"] = kmeans.fit_predict(df_pca[pc_cols])

    # 9. Cluster plot
    if n_components >= 2:
        plt.figure(figsize=(6, 6))
        plt.scatter(df_pca["PC1"], df_pca["PC2"], c=df_pca["cluster"], alpha=0.5)
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title(f"KMeans Clusters (k={n_clusters}) in PCA Space")
        plt.tight_layout()
        plt.show()

    print(df_pca.head())

    return df_pca

