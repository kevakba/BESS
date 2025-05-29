#Variables for the market data
# Alberta Internal Load (MW)
# Predicted pool price / pool price (for backtesting) ($/MWh)
# Solar generation (MW)
# Wind generation (MW)
# Supply cushion (MW) [ supply cushion = AIL - (solar + wind) ]
# Supply cushion as a percentage of AIL (%)

#Variables for the battery data
# Battery generation (MW) [vBattPower]
# Battery charging power (MW) [vCharge]
# Battery discharging power (MW) [vDischarge]
# Battery state of charge (SOC) (%) [vSOC]
# Battery charging status (charging-1 or discharging-0) [vChargeStatus]

#Constants for the battery data
# Battery Max charging power (MW) [max_charge_rate]
# Battery Max discharging power (MW) [max_discharge_rate]
# Battery initial state of charge (SOC) (%) [init_soc]
# Battery minimum state of charge (SOC) (%) [min_soc]
# Battery maximum state of charge (SOC) (%) [max_soc]
# Battery capacity (MWh) [capacity]
# Battery charging efficiency (%) [charge_eff]
# Battery discharging efficiency (%) [discharge_eff]

#Python version 3.11.2


import pandas as pd
from datetime import datetime, timedelta
import os
import numpy as np
import timeit
import re
from ortools.linear_solver import pywraplp
from backports.zoneinfo import ZoneInfo

# Get the current date and add one day to it
# current_date = datetime.now()
current_date = datetime.now(ZoneInfo('UTC')) 
current_date = current_date.replace(tzinfo=None)

next_date = current_date + timedelta(days=1)

start_date = current_date.strftime('%Y-%m-%d')
end_date = next_date.strftime('%Y-%m-%d')

# Save the results to CSV files
output_dir = 'Jobs/Inferencing/data/processed/'
os.makedirs(output_dir, exist_ok=True)

#Function to get the last row from the latest BESS_Optimization CSV file and return the last SOC value

def get_last_row_from_latest_bess_csv(output_dir):
    # Pattern to match the BESS_Optimization CSV files
    pattern = re.compile(r'^BESS_Optimization_\d{8}_\d{8}\.csv$')

    # List all matching CSV files in the directory
    files = [f for f in os.listdir(output_dir) if pattern.match(f)]

    if not files:
        raise FileNotFoundError("No matching BESS_Optimization CSV files found in the output directory.")

    # Sort files by modified time to get the latest one
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))

    # Read the latest CSV into a DataFrame
    latest_path = os.path.join(output_dir, latest_file)
    df = pd.read_csv(latest_path)

    if df.empty:
        raise ValueError("The latest CSV file is empty.")

    # Return the last row as a Series
    return df.iloc[-1]

last_row = get_last_row_from_latest_bess_csv(output_dir)

# Extract the last SOC value from the latest results CSV file and assign it as the initial SOC for the next run
if 'State-of-charge (SOC)' in last_row and not pd.isna(last_row['State-of-charge (SOC)']):
    iSoC = last_row['State-of-charge (SOC)']
else:
    iSoC = 0.1 # Default value if not found

'''
# Load the data from the CSV file
# predicted pool price
# AIL
# Solar generation
# Wind generation

df (next 24 hours) --> ['datetime_', 'pool_price', 'alberta_internal_load', 'wind_generation', 'solar_generation']

'''

#Define the dataframes for the battery and grid data
batt_df = {
    "max_charge_rate": [9.0],  # Example value in MW
    "max_discharge_rate": [9.0],  # Example value in MW
    "capacity": [20.0],  # Example value in MWh
    "charge_eff": [0.95],  # Example efficiency
    "discharge_eff": [0.95],  # Example efficiency
    "min_soc": [0.1],  # Minimum state of charge
    "max_soc": [0.95],  # Maximum state of charge
    "initial_soc": [iSoC]  # Initial state of charge
}

grid_df = {
    "max_buy_power" : [13000], 
    "max_sell_power" : [13000], 
    "max_import_power" : [13000], 
    "max_export_power" : [13000]
}

battery_df = pd.DataFrame(batt_df)
grid_df = pd.DataFrame(grid_df)


#Create the datetime index for the market dataframe in "%Y-%m-%d %H:%M:%S" format
market_data = pd.read_csv('Jobs/Inferencing/data/cleaned/merged_df_cleaned.csv')
pred_df = pd.read_csv('Jobs/Inferencing/data/predictions/pred_df.csv')

merged_df = pd.merge(market_data, pred_df, on='datetime_', how='inner')

df=merged_df[['datetime_', 'predicted_pool_price', 'forecast_alberta_internal_load', 'wind_generation', 'solar_generation']]

df.fillna(0, inplace=True)
#Convert the datetime column to datetime format and sort the dataframe by time
df['datetime_'] = pd.to_datetime(df['datetime_'])
# df.sort_values(by=["datetime_"], inplace=True)

market1DF = df.copy()
market1DF.sort_values(by=["datetime_"], inplace=True)
market1DF["time_string"] = market1DF.apply(
    lambda x: (x["datetime_"] + timedelta(seconds=0.002)).strftime("%Y-%m-%d %H:%M:%S"), axis=1)
market1DF.set_index("time_string", inplace=True)
marketDF = market1DF


#Converte all the dataframes to dictionaries
marketDict = marketDF.to_dict()
gridDict = grid_df.to_dict()
battDict = battery_df.to_dict()

# Calculate time interval
timeInterval = marketDF.iloc[1]['datetime_'] - marketDF.iloc[0]['datetime_']


# Assign the data to the input structure
input_data = type("input", (dict,), {})()
input_data.update({
    "simData": {
        "startTime": datetime.strptime(marketDF.index[0], "%Y-%m-%d %H:%M:%S"),
        "dt": int(round(timeInterval.total_seconds())) / (60 * 60),  # in hours
        "tIndex": marketDF.shape[0]
    },
    "market": {
        key: {sub_key: sub_item for sub_key, sub_item in marketDict[key].items()}
        for key in marketDict.keys() if key != "datetime_"
    },
    "grid": {key: item[0] for key, item in gridDict.items()},
    "batt": {key: item[0] for key, item in battDict.items()}
})


# Create the mip solver with the CBC backend.
solver = pywraplp.Solver.CreateSolver("CBC")

inf = solver.infinity()

tIndex = input_data["simData"]["tIndex"] # number of timeslots
dt = input_data["simData"]["dt"] # time interval in hour

# Create datetime array
startTime = input_data["simData"]["startTime"].strftime("%Y-%m-%d %H:%M:%S")
tIndex = input_data["simData"]["tIndex"]
timestamp = pd.date_range(startTime, periods=tIndex, freq=str(dt * 60) + "min")
time = [timestamp[i].strftime("%Y-%m-%d %H:%M:%S") for i in range(len(timestamp))]

time_s = timeit.default_timer()


# Adding timeseries variables
vGrid = [solver.NumVar(lb=-inf, ub=inf, name=f"vGrid_{i}") for i in range(tIndex)]
vBattPower = [solver.NumVar(lb=-inf, ub=inf, name=f"vBattPower_{i}") for i in range(tIndex)]
vCharge = [solver.NumVar(lb=-inf, ub=0, name=f"vCharge_{i}") for i in range(tIndex)]
vDischarge = [solver.NumVar(lb=0, ub=inf, name=f"vDischarge_{i}") for i in range(tIndex)]
vChargeStatus = [solver.BoolVar(name=f"vChargeStatus_{i}") for i in range(tIndex)]
vSOC = [solver.NumVar(lb=0, ub=1, name=f"vSOC_{i}") for i in range(tIndex)]

# Adding constraints
for i in range(tIndex):
    t = time[i]

    # Grid constraints
    solver.Add(vGrid[i] == input_data["market"]["forecast_alberta_internal_load"].get(t, 0) - input_data["market"]["solar_generation"].get(t, 0) -
               input_data["market"]["wind_generation"].get(t, 0) - vBattPower[i])  
   
    solver.Add(vBattPower[i] == vCharge[i] + vDischarge[i])  
    solver.Add(vCharge[i] >= -input_data["batt"]["max_charge_rate"] * vChargeStatus[i]) 
    solver.Add(vDischarge[i] <= input_data["batt"]["max_discharge_rate"] * (1 - vChargeStatus[i]))  
    if i == 0:
        solver.Add(vSOC[i] == input_data["batt"]["initial_soc"] - dt / input_data["batt"]["capacity"] *
                   (vCharge[i] * (input_data["batt"]["charge_eff"]) +
                    vDischarge[i] / (input_data["batt"]["discharge_eff"])))  
    else:
        solver.Add(vSOC[i] == vSOC[i-1] - dt / input_data["batt"]["capacity"] *
                   (vCharge[i] * (input_data["batt"]["charge_eff"]) +
                    vDischarge[i] / (input_data["batt"]["discharge_eff"]))) 
    solver.Add(vSOC[i] >= input_data["batt"]["min_soc"])
    solver.Add(vSOC[i] <= input_data["batt"]["max_soc"]) 


# Adding objective
obj = 0
#obj += sum(-[vBattPower[i] * input_data["market"]["pool_price"][time[i]] * dt for i in range(tIndex)])
for i in range(tIndex):
    t = time[i]
    pool_price = input_data["market"]["predicted_pool_price"].get(t, 0)
    #pool_price = input_data["market"]["pool_price"].get(t, 0)  # Use .get() to handle missing keys
    obj += vBattPower[i] * pool_price * dt  # Accumulate the objective function
solver.Maximize(obj)

#

status = solver.Solve()
print("Solver status:", status)

time_e = timeit.default_timer()
runTime = round(time_e - time_s, 4)

if status == solver.OPTIMAL or status == solver.FEASIBLE:
    print("Solution is found.")
    print("Number of variables =", solver.NumVariables())
    print("Number of constraints =", solver.NumConstraints())
    print("Computation time = ", runTime)
    
    # Extracting solution values
    
    objValue = round(solver.Objective().Value() / 100, 2)
    
    objValueDF = pd.DataFrame.from_dict({"obj_value": objValue}, orient="index", columns=["Total P&L of BESS Operation ($)"])
    
    result = list(zip([round(input_data["market"]["predicted_pool_price"].get(time[i], 0), 2) for i in range(tIndex)],
                      [round(vGrid[i].solution_value(), 2) for i in range(tIndex)], 
                      [round(vBattPower[i].solution_value(), 2) for i in range(tIndex)],
                      [round(vCharge[i].solution_value(), 2) for i in range(tIndex)],
                      [round(vDischarge[i].solution_value(), 2) for i in range(tIndex)],
                      [round(vSOC[i].solution_value(), 4) for i in range(tIndex)],
                      [int(vChargeStatus[i].solution_value()) for i in range(tIndex)]
                      ))
    resultDF = pd.DataFrame(result, index=timestamp, columns=["pool_price ($/MWh)","Grid Power Flow (MW)", "Battery Output (MW)", "Charging Power (MW)", "Discharging Power (MW)", "State-of-charge (SOC)", "Charge Status"])
    
else:
    resultDF = pd.DataFrame()
    print("Solution cannot be found.")


resultDF.to_csv(os.path.join(output_dir, f'BESS_Optimization_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv'))
objValueDF.to_csv(os.path.join(output_dir, f'BESS_Optimization_PnL_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv'))