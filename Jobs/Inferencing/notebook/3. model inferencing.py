# %%
# This notebook do inference on a trained model

# NVIDIA-SMI 535.183.01 
# CUDA Version: 10.1
# CUDNN Version: 
    #define CUDNN_MAJOR 7
    #define CUDNN_MINOR 6
    #define CUDNN_PATCHLEVEL 5
# Tensorflow Version: 2.2.0
# Python Version: 3.8.10

# %% [markdown]
# #### Library

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os

# Set pandas to display all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# Suppress pandas performance warnings
import warnings
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)
from datetime import datetime, timedelta
import joblib

# %%
# check tf version
print('TensorFlow version:', tf.__version__)

#  Check if TensorFlow can access GPUs
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"TensorFlow is using GPU: {gpus}")
else:
    print("No GPU found, using CPU instead.")

# %% [markdown]
# #### Load Inference Data

# %%
# load inference data
inference_data = pd.read_csv('Jobs/Inferencing/data/raw/merged_df_cleaned.csv')

# %% [markdown]
# #### Model Inferencing

# %%
# Load the saved model
def load_model(save_path):
    model = tf.keras.models.load_model(save_path)
    print(f"Model loaded from {save_path}")
    return model

def get_artifact(folder_path, extension):
    # Get all files with the specified extension in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
    
    if not files:
        raise FileNotFoundError(f"No files with extension '{extension}' found in {folder_path}")
    
    # Get the full paths of the files
    full_paths = [os.path.join(folder_path, f) for f in files]
    
    # Find the file with the latest modification time
    latest_file = max(full_paths, key=os.path.getmtime)
    # # latest_file = [full_paths]
    return latest_file

# save_path = f"Jobs/Retraining/artifacts/lstm_model_{datetime.now().strftime('%Y%m%d')}.h5"
folder_path = "Jobs/Retraining/artifacts/" 
# Get the latest .h5 model file
latest_model_path = get_artifact(folder_path, extension=".h5")

# load trained model
model = load_model(latest_model_path)

# %%
# Load the scaler
def load_scaler(save_path):
    scaler = joblib.load(save_path)
    print(f"Scaler loaded from {save_path}")
    return scaler

# save_path = f"Jobs/Retraining/artifacts/scaler_{datetime.now().strftime('%Y%m%d')}.pkl"
folder_path = "Jobs/Retraining/artifacts/"
# Get the latest .pkl scaler file
latest_scaler_path = get_artifact(folder_path, extension=".pkl")

scaler = load_scaler(latest_scaler_path)

# %%
# data transformation
X_inference = inference_data.drop(columns=['datetime_'])
X_inference = scaler.transform(X_inference)
X_inference = X_inference.reshape((X_inference.shape[0], 1, int(X_inference.shape[1])))

# make predictions
y_inference_pred = model.predict(X_inference)
y_inference_pred = y_inference_pred.reshape(-1, 1)
y_inference_pred

# %%
# save the predictions
pred_df_new = pd.DataFrame()
pred_df_new['datetime_'] = inference_data['datetime_']
pred_df_new['predicted_pool_price'] = y_inference_pred

print(pred_df_new)

# load the existing predictions
try:
    pred_df = pd.read_csv('Jobs/Inferencing/data/predictions/pred_df.csv')
except:
    pred_df = pd.DataFrame()

print(pred_df_new)

# concatenate the new predictions with the existing predictions
pred_df = pd.concat([pred_df, pred_df_new], axis=0, ignore_index=True)
# drop null values
pred_df = pred_df.dropna(subset=['predicted_pool_price'])
# drop duplicates
pred_df = pred_df.drop_duplicates(subset=['datetime_'], keep='last')
# sort the dataframe by datetime
pred_df = pred_df.sort_values(by='datetime_', ascending=True)
# reset the index
pred_df = pred_df.reset_index(drop=True)
# save the predictions
pred_df.to_csv('Jobs/Inferencing/data/predictions/pred_df.csv', index=False)


