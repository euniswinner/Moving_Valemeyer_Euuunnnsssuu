import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def load_data():
    df = pd.read_csv("california_buyout_records.csv")
    print(f"Loaded {len(df)} records.")
    return df


def summary_stats(df):
    print("\n--- Summary Stats ---")
    print("Average project amount: $", round(df["projectAmount"].mean(), 2))
    print("Average cost share percentage:", round(df["costSharePercentage"].mean(), 3))
    print("Average benefit-cost ratio:", round(df["benefitCostRatio"].mean(), 3))
    print("\nProjects by status:")
    print(df["status"].value_counts())


def projects_by_county(df):
    counts = df["county"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="barh", ax=ax, color="#2b6cb0")
    ax.set_title("California FEMA Buyout Projects by County (Top 10)")
    ax.set_xlabel("Number of Projects")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig("ca_projects_by_county.png", dpi=150)
    print("\nSaved chart: ca_projects_by_county.png")


def cost_share_vs_benefit(df):
    # Drop rows where either value is missing or zero (can't use those)
    clean = df.dropna(subset=["costSharePercentage", "benefitCostRatio"])
    clean = clean[(clean["costSharePercentage"] > 0) & (clean["benefitCostRatio"] > 0)]

    print(f"\n{len(clean)} records have usable cost-share and benefit-cost data.")

    if len(clean) < 5:
        print("Not enough data points to run a meaningful regression.")
        return

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        clean["costSharePercentage"], clean["benefitCostRatio"]
    )
    print("\n--- Regression: cost share % -> benefit-cost ratio ---")
    print(f"slope = {round(slope, 3)}")
    print(f"r-squared = {round(r_value ** 2, 3)}")
    print(f"p-value = {round(p_value, 4)}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(clean["costSharePercentage"], clean["benefitCostRatio"], alpha=0.6, color="#2b6cb0")
    ax.set_title("Federal Cost Share % vs. Benefit-Cost Ratio\n(California FEMA Buyout Projects)")
    ax.set_xlabel("Federal Cost Share (%)")
    ax.set_ylabel("Benefit-Cost Ratio")
    fig.tight_layout()
    fig.savefig("ca_cost_share_vs_benefit.png", dpi=150)
    print("Saved chart: ca_cost_share_vs_benefit.png")


if __name__ == "__main__":
    df = load_data()
    summary_stats(df)
    projects_by_county(df)
    cost_share_vs_benefit(df)