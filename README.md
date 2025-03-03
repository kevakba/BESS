# BESS Problem

## Project Structure

- `data/`: Contains JSON/csv data files.
- `scripts/`: Contains Python scripts.
- `Notebooks/`: Contains Notebooks.
- `docker/`: Contains docker files.
- `secret/`: API keys and others
- `.gitignore`: Specifies files to be ignored by Git.
- `.venv/`: Contains virtual environment.
- `requirements.txt`: contains python package requirements information.
- `README.md`: Project documentation.

## Hypotehsis:
- Can we predict `electricity price` from `generation (solar, wind, gas & hydro)` and `demand (AIL)` and `inter_tie (MATL, BC, SK)` prediction?

## Model Training: 
	- Data:
        Get the data for past 6 month (01/06/2024 - 31/12/2024)

        Target Variable:
            - actual electricity price: have a python script which fetch actual & predicted price data on hourly basis (CAD/MWH)

        Independent Variables:
            - actual demand (AIL): history present & predicted present
            - actual solar production: history present & predicted present
            - actual wind production: history present & predicted present
            - Others_proxy (proxy = AIL - solar - wind): history present & predicted present (for later use)
            - temperature_Calgary: history present & predicted present
            - temperature_Edmonton: history present & predicted present
            - temperature_FortMacmurrey: history present & predicted present

            - inter_tie: history present (non-tested) but not sure of predicted data (model required it for inferencing)

            - actual gas production: Others_proxy would takre care
            - actual hydro production: Others_proxy would takre care

                        "MC": Maximum Capability
                        "MBO OUT": Mothball (MBO) outage
                        "OP OUT": Operational (OP) outage 
                        "AC": Available Capacity
                                AC = MC - (MBO OUT + OP OUT)
                                Others_proxy = predicted_AIL - predicted_solar - predicted_wind

## Model Inferencing:
	- demand:
		- accurately being predicted for next 24 hours

	- electricity price:

	- supply:
		- solar: accurately being predicted for next 24 hours
		- wind: accurately being predicted for next 24 hours

## Tasks:
    - download data for Dec 2024
    - train ML model to predict price using variables solar, wind and demand


## Performance Goal:
    - High prices (>200 $/MWh) will require high precision (Target > 70%) and high recall (Target > 70%)
        - price > 200: try to make good performance (MAE < 50) 
        - 120 < price <= 200: try to keep (MAE < 50)
        - price < 120: try to keep (MAE < 30)

    - Low prices, the model will require high accuracy.

    - Several factors causing the price spikes:
        - Tight supply cushion (low renewable power penetration net to the grid with high demand)
        - Available transfer capacity on interties
        - High AIL  
        - Extreme weather conditions
        - Unexpected major outages such as large generating assets going offline, and transmission congestion due to faults/maintenance outages in the Alberta Interconnected Electric System.


## Current Status:
    - we have LSTM model which can predict electricity price for next 24 hours with good performance
    


## To Do:
    - create inferencing script such that it fetch the required data and predict electricty price for next 24 hours
    - host the inferencing script and make it run daily to predict for next 24 hours
    - store the daily inferencing results and check the performance against the actual electricity price


## links:

- [AESO Developer API](https://developer-apim.aeso.ca/apis)
- [AESO ETS](http://ets.aeso.ca/)
- [AESO Historical Generation Data](https://www.aeso.ca/market/market-and-system-reporting/data-requests/historical-generation-data)
- [AESO Box](https://aeso.app.box.com/s/qofgn9axnnw6uq3ip1goiq2ngb11txe5)
- [Generation Report Live](http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet)
- [Historical Generation Data](https://aeso.app.box.com/s/qofgn9axnnw6uq3ip1goiq2ngb11txe5/folder/196731538687)

