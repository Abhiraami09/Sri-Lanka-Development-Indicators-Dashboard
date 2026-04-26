import pandas as pd
import os

RAW_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
LKA_OUT  = os.path.join(os.path.dirname(__file__), "cleaned_lka.csv")
ALL_OUT  = os.path.join(os.path.dirname(__file__), "cleaned_all.csv")


def load_and_clean() -> pd.DataFrame:
    """Load the World Bank wide-format CSV and return a tidy long-format DataFrame."""
    # The file has 4 header rows before the actual data header
    # Line 1: "Data Source","World Development Indicators"
    # Line 2: blank
    # Line 3: "Last Updated Date","2026-04-08"
    # Line 4: blank
    # Line 5: actual column headers
    raw = pd.read_csv(RAW_PATH, skiprows=4, header=0)

    # Drop trailing empty columns produced by the trailing comma
    raw = raw.dropna(axis=1, how="all")

    # Rename first 4 fixed columns
    raw.columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + list(raw.columns[4:])

    # Year columns are strings like "1960", "1961", …
    year_cols = [c for c in raw.columns if c.isdigit()]

    # Melt to long format
    df = raw.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
        value_vars=year_cols,
        var_name="Year",
        value_name="Value",
    )
    df["Year"]  = df["Year"].astype(int)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # Drop rows with no value
    df = df.dropna(subset=["Value"])
    return df


def save_outputs(df: pd.DataFrame) -> None:
    lka = df[df["Country Code"] == "LKA"].copy()
    lka = lka.sort_values(["Indicator Name", "Year"]).reset_index(drop=True)
    lka.to_csv(LKA_OUT, index=False)
    print(f"Saved {len(lka)} rows → {LKA_OUT}")

    df.to_csv(ALL_OUT, index=False)
    print(f"Saved {len(df)} rows → {ALL_OUT}")


if __name__ == "__main__":
    df = load_and_clean()
    save_outputs(df)
    print("Done.")