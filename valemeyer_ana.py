import pandas as pd
import matplotlib.pyplot as plt
import folium
from scipy import stats


OLD_SITE = {"name": "Old Valmeyer (pre-1993, floodplain)", "lat": 38.2903, "lon": -90.3225}
NEW_SITE = {"name": "New Valmeyer (post-1993, bluff)", "lat": 38.3059, "lon": -90.2841}

def build_site_map():
    m = folium.Map(location=[38.298, -90.303], zoom_start=13, tiles="OpenStreetMap")

    folium.Marker(
        [OLD_SITE["lat"], OLD_SITE["lon"]],
        popup=OLD_SITE["name"],
        tooltip="Old site (abandoned after 1993 flood)",
        icon=folium.Icon(color="red", icon="tint"),
    ).add_to(m)

    folium.Marker(
        [NEW_SITE["lat"], NEW_SITE["lon"]],
        popup=NEW_SITE["name"],
        tooltip="New site (~2 miles east, 300+ ft higher)",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)

    folium.PolyLine(
        [[OLD_SITE["lat"], OLD_SITE["lon"]], [NEW_SITE["lat"], NEW_SITE["lon"]]],
        color="blue", weight=2, dash_array="5,5",
        tooltip="Relocation path (~2 mi)",
    ).add_to(m)

    return m

population = pd.DataFrame({
    "year": [1980, 1990, 2000, 2010, 2020],
    "population": [900, 895, 608, 1263, 1233],
})

def plot_population_trend():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(population["year"], population["population"], marker="o", color="#2b6cb0")
    ax.axvline(1993, color="red", linestyle="--", alpha=0.6, label="1993 flood / relocation begins")
    ax.set_title("Valmeyer, IL — Population Before & After Relocation")
    ax.set_xlabel("Year")
    ax.set_ylabel("Population")
    ax.legend()
    fig.tight_layout()
    return fig


comparison_towns = pd.DataFrame({
    "town": ["Valmeyer, IL", "Town B", "Town C", "Town D", "Town E"],
    "federal_funding_pct": [90, 60, 75, 40, 55],
    "resident_participation_pct": [95, 55, 80, 35, 60],
    "pop_recovery_pct": [140, 70, 105, 45, 65],
})

def run_regression():
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        comparison_towns["resident_participation_pct"],
        comparison_towns["pop_recovery_pct"],
    )
    return {
        "slope": round(slope, 2),
        "r_squared": round(r_value ** 2, 3),
        "p_value": round(p_value, 4),
    }


if __name__ == "__main__":
    import os

    output_dir = os.path.dirname(os.path.abspath(__file__))

    site_map = build_site_map()
    site_map.save(os.path.join(output_dir, "valemeyer_site_map.html"))

    fig = plot_population_trend()
    fig.savefig(os.path.join(output_dir, "valemeyer_population_trend.png"), dpi=150)

    results = run_regression()
    print("Regression: resident participation % -> population recovery %")
    print(results)