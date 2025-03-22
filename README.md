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
- Objective of this project is to minimize the operational cost of the BESS (Power purchase cost i.e. charging) and maximize the returns on selling the power during volatile periods (discharging).

## Model Training: 
	- Data:
        Get the data for past 6 month (01/06/2024 - 31/12/2024)

        Objective function:
        Minimizing the cost and maximize the profits (Ideal Buy Low Sell High with Threshold price set for both transactions)

        Target Variable:
            - Integer variable (0, 1 or 2) - Idle (0), Charge (1), Discharge (2) for specified time slot (1 hour min time)

        Independent Variables:

            Time dependent variables--
            - actual demand (AIL): history present & predicted present
            - actual solar production: history present & predicted present
            - actual wind production: history present & predicted present
            - hourly forecast price
            - inter_tie: history present (non-tested) but not sure of predicted data (model required it for inferencing)
            - Power supplied by BESS
            - Current state of charge (SOC) (%)
            - Charging power of BESS (in that interval)
            - Discharging power of BESS (in that interval)

            
            Constants or coefficients--
            - 
            - Energy capacity (or ampacity)
            - Max & Min SOC (%)
            - Charging/Discharging efficiency
            - BESS max charging power
            - BESS max discharging power
            - Max power required to be bought
            - Max power required to be sold
            - 
        

## Model Inferencing:
	

## Tasks:
    



## Performance Goal:
 



## links:



