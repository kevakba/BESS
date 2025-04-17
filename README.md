# BESS Problem

## Project Structure
- `.github`: contains github action workflows
- `.gitignore`: Specifies files to be ignored by Git. 📄
- `.venv/`: Contains virtual environment. 🐍
- `airflow`: Contains DAG files. 🌬️
- `data/`: Contains JSON/csv data files. 📊
- `docker/`: Contains docker files. 🐳
- `Jobs/`: Contains retrain, inference & evaluation job file
- `Notebooks/`: Contains Notebooks. 📓
- `README.md`: Project documentation. 📚
- `requirements.txt`: Contains Python package requirements information. 📦
- `scripts/`: Contains Python scripts. 📝
- `secret/`: API keys and others. 🔑

## Environment Setup:

- Create virtual environment: `python3 -m venv bess_venv` 🐍
- Activate virtual environment: `source bess_venv/bin/activate` 🚀
- Install requirements: `pip install -r requirements.txt` 📦
- To update the `requirements.txt` file: `pip freeze > requirements.txt` 🔄
- Go into notebook folder and run `mlflow ui --port 5001` 📊
- To run streamlit app: `streamlit run Jobs/Evaluation/app/app.py`

## Hypothesis: 
Can we predict `electricity price` for the next 24 hours?

| Feature                         | A. Time Series (Past data X LSTM_Window) | B. Regression (Forecast data X LSTM) |
|---------------------------------|-----------------------------|----------------------|
| alberta_internal_load           | ✅ Present                  | ❌ Absent           |
| lag_terms_AIL                   | ❌ Absent                   | ✅ Present          |
| forecast_alberta_internal_load  | ✅ Present                  | ✅ Present          |
| pool_price                      | ✅ Present                  | ❌ Absent           |
| lag_terms_pool_price            | ❌ Absent                   | ✅ Present          |
| forecast_pool_price             | ✅ Present                  | ❌ Absent           |
| rolling_30day_avg_price         | ✅ Present                  | ✅ Present          |
| solar_generation                | ✅ Present                  | ✅ Present          |
| wind_generation                 | ✅ Present                  | ✅ Present          |
| temp_calgary                    | ✅ Present                  | ✅ Present          |
| temp_edmonton                   | ✅ Present                  | ✅ Present          |
| temp_fortmc                     | ✅ Present                  | ✅ Present          |
| ws_calgary                      | ✅ Present                  | ✅ Present          |
| ws_edmonton                     | ✅ Present                  | ✅ Present          |
| ws_fortmc                       | ✅ Present                  | ✅ Present          |
| datetime_                       | ✅ Present                  | ✅ Present          |
| hour_of_day                     | ✅ Present                  | ✅ Present          |
| day_of_week                     | ✅ Present                  | ✅ Present          |
| day_of_month                    | ✅ Present                  | ✅ Present          |
| week_of_month                   | ✅ Present                  | ✅ Present          |
| month                           | ✅ Present                  | ✅ Present          |
| year                            | ✅ Present                  | ✅ Present          |
| is_winter                       | ✅ Present                  | ✅ Present          |


## Model Training: 
|  | Time Series Model| Regression Model |
|-----------------------------|-----------------------------|----------------------|
| Name                | TS_Model                | REG_model       |
| Model                | LSTM_Window                | LSTM       |
| Data               | Past data                | Forecast data       |
| Training frequency               | Weekly                | Weekly       |


## Model Inferencing:
- For every hour `h`, get pool price prediction from TS_Model & REG_model for `h+1` till `h+24`
- Weighted Average the response from both the models


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


## To Do:
    - create inferencing script such that it fetch the required data and predict electricty price for next 24 hours
    - host the inferencing script and make it run daily to predict for next 24 hours
    - store the daily inferencing results and check the performance against the actual pool price



## Links:
- [AESO Developer API](https://developer-apim.aeso.ca/apis) 🌐
- [AESO ETS](http://ets.aeso.ca/) 📊
- [AESO Historical Generation Data](https://www.aeso.ca/market/market-and-system-reporting/data-requests/historical-generation-data) 📈
- [AESO Box](https://aeso.app.box.com/s/qofgn9axnnw6uq3ip1goiq2ngb11txe5) 📦
- [Generation Report Live](http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet) 📅
- [Historical Generation Data](https://aeso.app.box.com/s/qofgn9axnnw6uq3ip1goiq2ngb11txe5/folder/196731538687) 📂

