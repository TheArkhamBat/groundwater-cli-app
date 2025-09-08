import typer
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing_extensions import Annotated

# Create a Typer application
app = typer.Typer(help="A CLI tool to fetch and plot groundwater level data from India-WRIS.")

def fetch_data_from_api(state: str, district: str, start_date: str, end_date: str):
    """Connects to the API and fetches the raw data."""
    url = "https://indiawris.gov.in/Dataset/Ground Water Level"
    params = {
        'stateName': state,
        'districtName': district,
        'agencyName': 'CGWB',
        'startdate': start_date,
        'enddate': end_date,
        'download': 'false',
        'page': '0',
        'size': '2000'  # Increased size for more data
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        api_data = response.json()
        if api_data.get("data"):
            return pd.DataFrame(api_data["data"])
        else:
            typer.secho(f"API Warning: {api_data.get('message', 'No data returned.')}", fg=typer.colors.YELLOW)
            return None
    except requests.exceptions.RequestException as e:
        typer.secho(f"API Request Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

def create_plot(df: pd.DataFrame, state: str, district: str):
    """Generates and displays a plot from the DataFrame."""
    # --- Data Preparation ---
    df['dataTime'] = pd.to_datetime(df['dataTime'])
    df['dataValue'] = pd.to_numeric(df['dataValue'])
    df = df.sort_values(by='dataTime').reset_index(drop=True)
    
    # Check if there is data to plot
    if df.empty:
        typer.echo("No data available to generate a plot.")
        return

    # --- Plotting ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(15, 8))
    
    # Group by station to plot separate lines if multiple stations exist
    for station_name, group_data in df.groupby('stationName'):
        sns.lineplot(data=group_data, x='dataTime', y='dataValue', marker='o', label=station_name)
    
    unit = df["unit"].iloc[0] if not df.empty else 'units'
    plt.title(f"Groundwater Level in {district.title()}, {state.title()}", fontsize=18, weight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(f"Water Level ({unit})", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Monitoring Station")
    plt.tight_layout()
    plt.show()

@app.command()
def fetch_and_plot(
    state: Annotated[str, typer.Option(help="The name of the state (e.g., 'Odisha').")],
    district: Annotated[str, typer.Option(help="The name of the district (e.g., 'Baleshwar').")],
    start_date: Annotated[str, typer.Option(help="Start date in YYYY-MM-DD format.")],
    end_date: Annotated[str, typer.Option(help="End date in YYYY-MM-DD format.")]
):
    """
    Fetch groundwater data for a given location and date range, then generate a plot.
    """
    typer.secho(f"Fetching data for {district}, {state}...", fg=typer.colors.CYAN)
    
    groundwater_df = fetch_data_from_api(state, district, start_date, end_date)
    
    if groundwater_df is not None and not groundwater_df.empty:
        typer.secho("Data fetched successfully!", fg=typer.colors.GREEN)
        typer.echo("First 5 rows of data:")
        print(groundwater_df.head())
        
        typer.secho("\nGenerating plot...", fg=typer.colors.CYAN)
        create_plot(groundwater_df, state, district)
    else:
        typer.secho("Could not process data. Exiting.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()