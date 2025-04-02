# %%
# This notebook trains LSTM model on the preprocessed forecasted data

# forecast_features= [
#     "forecast_alberta_internal_load", 
#     "rolling_30day_avg_price", 
#     "solar_generation", 
#     "wind_generation", 
#     "temp_calgary", 
#     "temp_edmonton", 
#     "temp_fortmc", 
#     "ws_calgary",
#     "ws_edmonton", 
#     "ws_fortmc",
#     "datetime_", 
#     "hour_of_day", 
#     "day_of_week", 
#     "day_of_month", 
#     "week_of_month", 
#     "month", 
#     "year", 
#     "is_winter" 
# ]


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
# #### Data Loading

# %%
# Load the data
# df2019 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2019/merged_df_2019_cleaned.csv')
# df2020 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2020/merged_df_2020_cleaned.csv')
# df2021 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2021/merged_df_2021_cleaned.csv')
# df2022 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2022/merged_df_2022_cleaned.csv')
# df2023 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2023/merged_df_2023_cleaned.csv')
# df2024 = pd.read_csv('/home/kevin/Downloads/BESS/data/raw/2024/merged_df_2024_cleaned.csv')
df = pd.read_csv('Jobs/Retraining/data/raw/merged_df_cleaned.csv')

# %%
# Concatenate the data
# df2019
# df = pd.concat([df2020, df2021, df2022, df2023, df2024], axis=0, ignore_index=True)

# %%
df.shape

# %%
df.head()

# %%
# remove actual AIL
df.drop(['alberta_internal_load'], inplace=True, axis=1)

# remove forecast_pool_price
df.drop(['forecast_pool_price'], inplace=True, axis=1)

# %%
# Check for missing values
df.isnull().sum().sort_values(ascending=False)

# %%
# Create a distribution plot of the 'pool_price' column
sns.distplot(df['pool_price'], hist=True, kde=True)

# Add labels and title
plt.xlabel('Pool Price')
plt.ylabel('Density')
plt.title('Distribution of Pool Price')

# Show the plot
plt.grid()
plt.show()

# %%
# data filter to remove outliers
# df = df[df['pool_price'] <=200]

# %% [markdown]
# #### Train-Test split

# %%
df.head()

# %%
# remove lag terms except 24 hours lag
# df.drop(columns = [col for col in df.columns if col.startswith('alberta_internal_load_lag') and col!='alberta_internal_load_lag_24'], inplace = True)
# df.drop(columns = [col for col in df.columns if col.startswith('pool_price_lag') and col!='pool_price_lag_24'], inplace = True)

# %%
# Ensure 'datetime_' column is in datetime format
df['datetime_'] = pd.to_datetime(df['datetime_'])

# Get the maximum date in the column
max_date = df['datetime_'].max()

# Calculate the first date of the last month
first_date_last_month = (max_date.replace(day=1) - timedelta(days=1)).replace(day=1)

# Format the date as 'yyyy-mm-dd'
first_date_last_month_str = first_date_last_month.strftime('%Y-%m-%d')

# print("First date of the last month:", first_date_last_month_str)

# %%
# Convert datetime_ column to datetime type
df['datetime_'] = pd.to_datetime(df['datetime_'])

# Filter data for the first 11 months
train_data = df[df['datetime_'] < first_date_last_month_str]
test_data = df[df['datetime_'] >= first_date_last_month_str]

# Define independent variables (features) and target variable
X_train = train_data.drop(columns=['datetime_', 'pool_price'])
y_train = train_data['pool_price']
# Display the shapes of the training data
print(X_train.shape, y_train.shape)

# Define independent variables (features) and target variable
X_test = test_data.drop(columns=['datetime_', 'pool_price'])
y_test = test_data['pool_price']
# Display the shapes of the test data
print(X_test.shape, y_test.shape)

# %%
#Converting dataframe to numpy
X_train = X_train.values
X_test = X_test.values
y_train = y_train.values
y_test = y_test.values

# %%
# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and testing data
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# %%
#Reshaping the train and test data to pass into the LSTM layer
X_train = X_train.reshape((X_train.shape[0], 1, int(X_train.shape[1])))
X_test = X_test.reshape((X_test.shape[0], 1, int(X_test.shape[1])))

# %%
# Display the shapes of the training data
X_train.shape

# %% [markdown]
# #### Model Training

# %%
#Baseline LSTM model
model = tf.keras.Sequential()
model.add(LSTM(128, activation='tanh', input_shape=(X_train.shape[1], X_train.shape[2]))) 
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation=None))

# Compile the model
model.compile(optimizer='adam', loss='mae')

# %%
# display architecture of model shape of different layers
model.summary()

# %%
# Fit the model
history = model.fit(X_train, y_train, epochs=20, batch_size=128, verbose=2, validation_split=0.2)

# %% [markdown]
# #### Model Performance Check

# %%
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# %%
y_train_pred = model.predict(X_train)
y_train_pred = y_train_pred.reshape(-1, 1)
mae_train = mean_absolute_error(y_train, y_train_pred)
r2_train = r2_score(y_train, y_train_pred)

print('y_train shape:', y_train.shape)
print(f'Mean Absolute Error on the train set : {mae_train}')
print(f"R² Score train set: {r2_train}")

# %%
y_test_pred = model.predict(X_test)
y_test_pred = y_test_pred.reshape(-1, 1)
mae_test = mean_absolute_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)

print('y_test_pred shape:', y_test_pred.shape)
print(f'Mean Absolute Error on the test set : {mae_test}')
print(f"R² Score test set: {r2_test}")

# %%
# Create a scatter plot with improved visibility
plt.figure(figsize=(10, 6), dpi=120)  # Higher DPI for sharper visualization

# Scatter plot with larger markers and better color contrast
plt.scatter(y_train, y_train_pred, alpha=0.6, color='royalblue', edgecolor='black', s=50, label='Predicted vs Actual')

# Add reference line (perfect predictions)
plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], 
         color='darkred', linestyle='--', linewidth=2, label='Perfect Fit (y = x)')

# Improve labels and title for better readability
plt.xlabel('Actual Values', fontsize=12, fontweight='bold', color='darkblue')
plt.ylabel('Predicted Values', fontsize=12, fontweight='bold', color='darkblue')
plt.title(f'TRAIN: Scatter Plot of Actual vs Predicted Values\nR² Score: {r2_train:.2f}', 
          fontsize=14, fontweight='bold', color='darkgreen')

# Improve the legend for better clarity
plt.legend(fontsize=12, loc='upper left', frameon=True, facecolor='whitesmoke')

# Customize grid for improved visibility
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

# Enhance tick visibility
plt.xticks(fontsize=10, color='black')
plt.yticks(fontsize=10, color='black')

# Show the plot
plt.show()


# %%
# Create a scatter plot for test data with improved visibility
plt.figure(figsize=(10, 6), dpi=120)  # Higher DPI for sharper visualization

# Scatter plot with larger markers and better color contrast
plt.scatter(y_test, y_test_pred, alpha=0.6, color='royalblue', edgecolor='black', s=50, label='Predicted vs Actual')

# Add reference line (perfect predictions)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 
         color='darkred', linestyle='--', linewidth=2, label='Perfect Fit (y = x)')

# Improve labels and title for better readability
plt.xlabel('Actual Values', fontsize=12, fontweight='bold', color='darkblue')
plt.ylabel('Predicted Values', fontsize=12, fontweight='bold', color='darkblue')
plt.title(f'TEST: Scatter Plot of Actual vs Predicted Values (Test Set)\nR² Score: {r2_test:.2f}', 
          fontsize=14, fontweight='bold', color='darkgreen')

# Improve the legend for better clarity
plt.legend(fontsize=12, loc='upper left', frameon=True, facecolor='whitesmoke')

# Customize grid for improved visibility
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

# Enhance tick visibility
plt.xticks(fontsize=10, color='black')
plt.yticks(fontsize=10, color='black')

# Show the plot
plt.show()


# %%
# # Create a dataframe of the actual and predicted values
# results_df = pd.DataFrame({'y_test':y_test, 'y_test_pred':y_test_pred.flatten()})
# results_df.head()

# %%
# terget_df = results_df[results_df['y_test'] <= 200]

# mae = mean_absolute_error(terget_df.y_test, terget_df.y_test_pred)
# r2 = r2_score(terget_df.y_test, terget_df.y_test_pred)

# print('terget_df shape:', terget_df.shape)
# print(f'Mean Absolute Error on the test set : {mae}')
# print(f"R² Score test set: {r2}")

# %%
# terget_df = results_df[results_df['y_test'] > 200]

# mae = mean_absolute_error(terget_df.y_test, terget_df.y_test_pred)
# r2 = r2_score(terget_df.y_test, terget_df.y_test_pred)

# print('terget_df shape:', terget_df.shape)
# print(f'Mean Absolute Error on the test set : {mae}')
# print(f"R² Score test set: {r2}")

# %% [markdown]
# #### Store Model Artifacts

# %%
# Save the trained model
def save_model(model, save_path):
    model.save(save_path)
    print(f"Model saved to {save_path}")

save_path = f"Jobs/Retraining/artifacts/lstm_model_{datetime.now().strftime('%Y%m%d')}.h5"
save_model(model, save_path)

# %%
# Save the scaler
def save_scaler(scaler, save_path):
    joblib.dump(scaler, save_path)
    print(f"Scaler saved to {save_path}")

save_path = f"Jobs/Retraining/artifacts/scaler_{datetime.now().strftime('%Y%m%d')}.pkl"
print('scaler saved at {save_path}')
save_scaler(scaler, save_path)

# %% [markdown]
# #### Model Inferencing

# %%
# load inference data
# inference_data = pd.read_csv('/home/kevin/Downloads/BESS/Jobs/Inferencing/data/raw/merged_df_cleaned.csv')

# %%
# # Load the saved model
# def load_model(save_path):
#     model = tf.keras.models.load_model(save_path)
#     print(f"Model loaded from {save_path}")
#     return model

# save_path = f"/home/kevin/Downloads/BESS/Jobs/Retraining/artifacts/lstm_model_{datetime.now().strftime('%Y%m%d')}.h5"

# # load trained model
# model = load_model(save_path)

# %%
# # Load the scaler
# def load_scaler(save_path):
#     scaler = joblib.load(save_path)
#     print(f"Scaler loaded from {save_path}")
#     return scaler

# save_path = f"/home/kevin/Downloads/BESS/Jobs/Retraining/artifacts/scaler_{datetime.now().strftime('%Y%m%d')}.pkl"

# scaler = load_scaler(save_path)

# %%
# # data transformation
# X_inference = inference_data.drop(columns=['datetime_'])
# X_inference = scaler.transform(X_inference)
# X_inference = X_inference.reshape((X_inference.shape[0], 1, int(X_inference.shape[1])))

# # make predictions
# y_inference_pred = model.predict(X_inference)
# y_inference_pred = y_inference_pred.reshape(-1, 1)
# y_inference_pred

# %%
# # save the predictions
# pred_df_new = pd.DataFrame()
# pred_df_new['datetime_'] = inference_data['datetime_']
# pred_df_new['predicted_pool_price'] = y_inference_pred

# # load the existing predictions
# try:
#     pred_df = pd.read_csv('/home/kevin/Downloads/BESS/Jobs/Inferencing/data/predictions/pred_df.csv')
# except:
#     pred_df = pd.DataFrame()

# # concatenate the new predictions with the existing predictions
# pred_df = pd.concat([pred_df, pred_df_new], axis=0, ignore_index=True)
# # drop duplicates
# pred_df = pred_df.drop_duplicates(subset=['datetime_'], keep='last')
# # sort the dataframe by datetime
# pred_df = pred_df.sort_values(by='datetime_', ascending=True)
# # reset the index
# pred_df = pred_df.reset_index(drop=True)
# # save the predictions
# pred_df.to_csv('/home/kevin/Downloads/BESS/Jobs/Inferencing/data/predictions/pred_df.csv', index=False)


