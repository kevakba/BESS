'''
use this command from project home directory to run the app:
streamlit run Jobs/Evaluation/app/app.py
'''

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- Page Config ---
st.set_page_config(
    page_title="📈 Pool Price Prediction Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("⚙️ Dashboard Settings")

# Dark Mode
dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode", value=False)

# Trendline Option
show_trend = st.sidebar.checkbox("📉 Add Rolling Average Trendline")

# Rolling window size
if show_trend:
    window_size = st.sidebar.slider("📏 Rolling Window Size (days)", min_value=3, max_value=30, value=7)

# Download Option
show_download = st.sidebar.checkbox("💾 Enable Data Download", value=True)

# --- Load Data ---
@st.cache_data
def load_data():
    actual = pd.read_csv('Jobs/Evaluation/data/actual/price.csv')[['datetime_', 'actual_pool_price']]
    predicted = pd.read_csv('Jobs/Inferencing/data/predictions/pred_df.csv')[['datetime_', 'predicted_pool_price']]
    df = pd.merge(actual, predicted, on='datetime_', how='inner')
    df.dropna(inplace=True)
    df['datetime_'] = pd.to_datetime(df['datetime_'])
    return df

data = load_data()

# --- Header ---
st.markdown(f"""
    <h1 style='text-align: center; color: {"#FFFFFF" if dark_mode else "#2E86AB"};'>📊 Pool Price Prediction Dashboard</h1>
    <p style='text-align: center; font-size:18px; color: {"#AAAAAA" if dark_mode else "#4D4D4D"};'>
        Visualize model predictions, explore metrics, and filter by date ranges.
    </p>
    <hr style='margin-top: 0px;'>
""", unsafe_allow_html=True)

# --- Date Filter ---
st.subheader("📅 Filter by Date Range")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", data['datetime_'].min())
with col2:
    end_date = st.date_input("End date", data['datetime_'].max())

if start_date > end_date:
    st.warning("🚫 Start date must be before end date.")
    filtered_df = data.copy()
else:
    filtered_df = data[
        (data['datetime_'] >= pd.to_datetime(start_date)) &
        (data['datetime_'] <= pd.to_datetime(end_date))
    ].copy()

# --- Compute Metrics based on filtered data ---
y_true_filtered = filtered_df['actual_pool_price']
y_pred_filtered = filtered_df['predicted_pool_price']

if not y_true_filtered.empty and not y_pred_filtered.empty:
    mae_filtered = mean_absolute_error(y_true_filtered, y_pred_filtered)
    mse_filtered = mean_squared_error(y_true_filtered, y_pred_filtered)
    rmse_filtered = np.sqrt(mse_filtered)
    mape_filtered = (np.abs(y_true_filtered - y_pred_filtered) / y_true_filtered).replace([np.inf, -np.inf], np.nan).dropna().mean() * 100
    r2_filtered = r2_score(y_true_filtered, y_pred_filtered)

    # --- Metrics Display for Filtered Data ---
    st.subheader("📌 Model Evaluation Metrics (Filtered Range)")
    col1_f, col2_f, col3_f, col4_f = st.columns(4)
    col1_f.metric("📏 RMSE", f"{rmse_filtered:.2f}")
    col2_f.metric("📉 MAE", f"{mae_filtered:.2f}")
    col3_f.metric("📈 R² Score", f"{r2_filtered:.2f}")
    col4_f.metric("🧮 MAPE (%)", f"{mape_filtered:.2f}")
else:
    st.info("No data available for the selected date range to calculate metrics.")

# Add rolling averages if selected
if show_trend:
    filtered_df['actual_rolling'] = filtered_df['actual_pool_price'].rolling(window=window_size).mean()
    filtered_df['predicted_rolling'] = filtered_df['predicted_pool_price'].rolling(window=window_size).mean()

# --- Chart Section ---
st.subheader("📊 Actual vs Predicted Pool Prices Over Time")

fig = go.Figure()

# Actual & Predicted lines
fig.add_trace(go.Scatter(
    x=filtered_df['datetime_'], y=filtered_df['actual_pool_price'],
    mode='lines+markers', name='Actual', line=dict(color='green')
))
fig.add_trace(go.Scatter(
    x=filtered_df['datetime_'], y=filtered_df['predicted_pool_price'],
    mode='lines+markers', name='Predicted', line=dict(color='blue')
))

# Trendlines
if show_trend:
    fig.add_trace(go.Scatter(
        x=filtered_df['datetime_'], y=filtered_df['actual_rolling'],
        mode='lines', name=f'Actual {window_size}d Rolling Avg', line=dict(color='lightgreen', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['datetime_'], y=filtered_df['predicted_rolling'],
        mode='lines', name=f'Predicted {window_size}d Rolling Avg', line=dict(color='skyblue', dash='dash')
    ))

# Chart Layout
fig.update_layout(
    title="Actual vs Predicted Over Time",
    xaxis_title="Date",
    yaxis_title="Pool Price",
    hovermode="x unified",
    template="plotly_dark" if dark_mode else "plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# --- Table ---
with st.expander("🗂️ Show Filtered Data Table"):
    st.dataframe(filtered_df, use_container_width=True)

# --- Download Section ---
if show_download:
    st.markdown("### 💾 Download Full Merged Dataset")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "predictions.csv", "text/csv", key='download-csv')