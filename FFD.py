import requests
import pandas as pd

BASE_URL = "https://www.fema.gov/api/open/v4/HazardMitigationAssistanceProjects"


def get_valmeyer_projects():
    """Get FEMA buyout records for Monroe County, Illinois (where Valmeyer is)."""
    params = {
        "$filter": "state eq 'Illinois' and county eq 'Monroe'",
        "$top": 1000,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    records = data.get("HazardMitigationAssistanceProjects", [])
    return pd.DataFrame(records)


def get_comparison_buyout_projects(state="California", limit=100):
    """
    Get real 'Acquisition' (buyout) projects from another state.
    We use contains() because projectType is a long text field, e.g.
    '901: Acquisition of Real Property' — not an exact word.
    """
    params = {
        "$filter": f"state eq '{state}' and contains(projectType, 'Acquisition')",
        "$top": limit,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    records = data.get("HazardMitigationAssistanceProjects", [])
    return pd.DataFrame(records)


if __name__ == "__main__":
    print("Getting Valmeyer / Monroe County, Illinois records...")
    valmeyer_df = get_valmeyer_projects()
    print(f"Found {len(valmeyer_df)} records.")
    if len(valmeyer_df) > 0:
        valmeyer_df.to_csv("valmeyer_fema_records.csv", index=False)
        print("Saved to valmeyer_fema_records.csv")
    else:
        print("Still 0 records — Monroe County's 1990s buyout may predate this dataset,")
        print("or may be filed under a different county/program. We'll investigate next.")

    print("\nGetting comparison 'Acquisition' buyout records from California...")
    ca_df = get_comparison_buyout_projects(state="California")
    print(f"Found {len(ca_df)} records.")
    if len(ca_df) > 0:
        ca_df.to_csv("california_buyout_records.csv", index=False)
        print("Saved to california_buyout_records.csv")
        print("\nSample projectType values found:")
        print(ca_df["projectType"].unique()[:10])