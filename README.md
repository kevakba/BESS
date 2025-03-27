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

        Binary Variable:
            - Z [Integer variable (0 or 1) - Discharge (0), Charge (1) for specified time slot (1 hour min time)]

        Independent Variables:

            Time dependent variables--
            - actual demand (AIL): history present & predicted present
            - actual solar production: history present & predicted present
            - actual wind production: history present & predicted present
            - hourly market price (Et)
            - inter_tie: history present (non-tested) but not sure of predicted data (model required it for inferencing)
            - Power transaction from/to grid [Pt,grid] 
            - Power supplied/absorbed by BESS [Pt,batt]
            - BESS station load [Pt,load]
            - Current state of charge (SOC) (%)
            - Charging power of BESS (in that interval) [Pt,batt,charge]
            - Discharging power of BESS (in that interval) [Pt,batt,discharge]

            
            Constants or coefficients--
            - 
            - Energy capacity (or ampacity) [Cbatt]
            - Max & Min SOC (%)
            - Charging/Discharging efficiency (n)
            - BESS max charging power [Pt,batt,charge,max]
            - BESS max discharging power [Pt,batt,discharge,max]
            - Max power required to be bought
            - Max power required to be sold
            - Time interval (Dt)

        Equality constraints:

        Power balance euqation -
        
        Pt,batt - Pt,load = Pt,grid

        OR 

        Pt,batt,charge - Pt,load = Pt,grid
        Pt,batt,discharge + Pt,load = Pt,grid

        Inequality constraints:

        Assuming there is a contractual agreement between the retailer and the producer regarding the quantity of power that can be bought and sold, we have the following constraint:
            Pmax,sell <= Pt,grid <= Pmax,buy

            Charge (-ve power) and discharge (+ve power)
            Pt,batt = Pt,batt,charge (-ve) + Pt,batt,discharge (+ve)

        The binary variable σ ensures that charging and discharging cannot occur simultaneously. Additionally, the battery power has to respect the power limit as required by the BESS' rating.

        Pt,batt,charge >= Z * Pt,batt,charge,max
        Pt,batt,discharge <= (1-Z) * Pt,batt,discharge,max

        SOCt,batt = SOCt-1,batt - Dt * [n*Pt,batt,charge + (Pt,batt,discharge/n)] / Cbatt

        SOCbatt,min <= SOCt,batt <= SOCbatt,max

        Objective:

        While charging,

        min sum[Pt,grid * Et * Dt]

        While discharging,

        max sum[Pt,grid * Et * Dt]



## Model Inferencing:
	

## Tasks:
    



## Performance Goal:
 



## links:



