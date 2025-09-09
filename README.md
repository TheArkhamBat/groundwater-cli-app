# Groundwater Data Fetcher CLI (Backend Prototype)

### Working Prototype Demo (Frontend + Backend)

<video src="" width = "800" controls>
    Your browser does not support the video tag.
</video>

The working prototype can be found here : (https://github.com/OoONANCY/AquaMonitor).

### CLI Application Demo

<video src="https://github.com/TheArkhamBat/groundwater-cli-app/raw/refs/heads/main/demo.mp4?download=" width="800" controls>
    Your browser does not support the video tag.
</video>

## Project Overview

Fetches data from India-WRIS API to create and use json data for anaylsis and prediction of groundwater level in all districts of India. This project is a backend prototype for fetching and visualizing groundwater level data from the official India-WRIS (Water Resources Information System of India) public API. It is built as a command-line interface (CLI) tool using Python, allowing users to specify a location and date range to generate a time-series plot of the water levels.

## Features

* **Command-Line Interface:** Uses `Typer` to provide a clean, user-friendly CLI for interacting with the application.
* **API Integration:** Fetches data by making POST requests to the India-WRIS API endpoint.
* **Dynamic Data Fetching:** Accepts user inputs for state, district, and a start/end date range to retrieve specific datasets.
* **Data Processing:** Parses the JSON response from the API and loads it into a `pandas` DataFrame for manipulation and analysis.
* **Data Visualization:** Generates and displays a time-series line graph of the groundwater levels using `matplotlib` and `seaborn`.

## How to Use

This tool is designed to be run from the command line within a Python virtual environment.

1.  **Create and Activate Environment:** Create a Python virtual environment and activate it.
    ```bash
    # Create the environment
    python -m venv venv
    # Activate the environment (Linux/macOS)
    source venv/bin/activate
    ```

2.  **Install Dependencies:** Install the required Python libraries using pip.
    ```bash
    pip install "typer[all]" requests pandas matplotlib seaborn
    ```

3.  **Run the Tool:** Execute the script with the required command-line options.
    ```bash
    python groundwater_cli.py --state "Odisha" --district "Baleshwar" --start-date "2023-11-01" --end-date "2024-10-31"
    ```

## Core Dependencies

* **typer**: For building the command
