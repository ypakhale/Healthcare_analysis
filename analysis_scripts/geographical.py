import pandas as pd
import matplotlib.pyplot as plt

def geographic_analysis(df: pd.DataFrame):
    """
    1. State-level aggregation: mean payment & rating; bar chart.
    2. City-level: top-10 highest & lowest cost cities; bar charts.
    3. RUCA category (rural vs. urban) comparison; bar chart.
    
    Returns:
        state_stats: DataFrame with mean_payment & mean_rating per state
        top10_high_cities: DataFrame of top-10 highest-cost cities
        top10_low_cities: DataFrame of top-10 lowest-cost cities
        ruca_stats: DataFrame with mean_payment & mean_rating per RUCA category
    """
    # ——— 1. State-level aggregation ———
    state_stats = (
        df
        .groupby('facility_state')
        .agg(
            mean_payment=('Avg_Tot_Pymt_Amt', 'mean'),
            mean_rating=('rating', 'mean')
        )
        .sort_values('mean_payment', ascending=False)
    )
    print("\n=== State-Level Mean Payment & Rating ===")
    print(state_stats.head(10))
    
    # Bar chart: top 10 states by mean payment
    state_stats['mean_payment'].head(10).plot(
        kind='bar', figsize=(10, 6), title='Top 10 States by Mean Payment'
    )
    plt.ylabel('Mean Avg_Tot_Pymt_Amt')
    plt.xlabel('State')
    plt.tight_layout()
    plt.show()
    
    # ——— 2. City-level high/low cost ———
    city_stats = (
        df
        .groupby('facility_city')
        .agg(
            mean_payment=('Avg_Tot_Pymt_Amt', 'mean'),
            mean_rating=('rating', 'mean')
        )
        .dropna()
    )
    top10_high_cities = city_stats.nlargest(10, 'mean_payment')
    top10_low_cities  = city_stats.nsmallest(10, 'mean_payment')
    
    print("\n=== Top 10 Highest-Cost Cities ===")
    print(top10_high_cities)
    print("\n=== Top 10 Lowest-Cost Cities ===")
    print(top10_low_cities)
    
    # Bar charts: top/high and low cost cities
    top10_high_cities['mean_payment'].plot(
        kind='bar', figsize=(10, 6), title='Top 10 Highest-Cost Cities'
    )
    plt.ylabel('Mean Avg_Tot_Pymt_Amt')
    plt.xlabel('City')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    top10_low_cities['mean_payment'].plot(
        kind='bar', figsize=(10, 6), title='Top 10 Lowest-Cost Cities'
    )
    plt.ylabel('Mean Avg_Tot_Pymt_Amt')
    plt.xlabel('City')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # ——— 3. RUCA category comparison ———
    ruca_stats = (
        df
        .groupby('Rndrng_Prvdr_RUCA_Desc')
        .agg(
            mean_payment=('Avg_Tot_Pymt_Amt', 'mean'),
            mean_rating=('rating', 'mean')
        )
        .sort_values('mean_payment', ascending=False)
    )
    print("\n=== Mean Payment & Rating by RUCA Category ===")
    print(ruca_stats)
    
    # Bar chart: RUCA mean payment
    ruca_stats['mean_payment'].plot(
        kind='bar', figsize=(8, 6), title='Mean Payment by RUCA Category'
    )
    plt.ylabel('Mean Avg_Tot_Pymt_Amt')
    plt.xlabel('RUCA Category')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    print(state_stats.head())
    print(top10_high_cities.head())
    print(top10_low_cities.head())
    print(ruca_stats.head())
    
    return state_stats, top10_high_cities, top10_low_cities, ruca_stats
