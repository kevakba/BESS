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
        Get the data for past 6 month (01062024 - 31122024s)

        Targer Variable:
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

## links:

- [AESO Developer API](https://developer-apim.aeso.ca/apis)
- [AESO ETS](http://ets.aeso.ca/)
- [AESO Historical Generation Data](https://www.aeso.ca/market/market-and-system-reporting/data-requests/historical-generation-data)
- [AESO Box](https://aeso.app.box.com/s/qofgn9axnnw6uq3ip1goiq2ngb11txe5)
- [Generation Report Live](http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet)
