from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

# Define the function to execute a script
def run_script(script_path):
    subprocess.run(["python3", script_path], check=True)

# Define your scripts
def fetch_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

directory = "/home/kevin/Downloads/BESS/scripts/historical_data_fetching"
scripts = fetch_python_files(directory)


# Create the DAG
dag = DAG(
    dag_id="historical_data_fetching_pipeline",
    schedule=None,  # Run only when triggered manually
    start_date=datetime(2024, 3, 5),
    catchup=False
)

# Create tasks for each script
for script in scripts:
    task = PythonOperator(
        task_id=f"run_{script.split('/')[-1]}",
        python_callable=run_script,
        op_args=[script],
        dag=dag
    )


