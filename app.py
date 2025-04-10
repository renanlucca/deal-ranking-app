import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Deal Ranking & Simulation", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("TestData.csv")
    df["Amount"] = df["Amount"].replace('[\$,]', '', regex=True).astype(float)
    df["Close Date"] = pd.to_datetime(df["Close Date"])
    df["Quarter"] = "Q" + df["Close Date"].dt.quarter.astype(str) + "-" + df["Close Date"].dt.year.astype(str)
    df["Expected Value"] = df["Amount"] * df["Deal probability"]
    return df

df = load_data()

# --- UI: Quarter Selection ---
st.title("📊 Deal Ranking Dashboard")

quarter_options = sorted(df["Quarter"].unique().tolist())
quarter = st.selectbox("Select a Quarter", ["Full Year"] + quarter_options)

if quarter == "Full Year":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Quarter"] == quarter]

# --- Rank Deals by Expected Value ---
ranked_df = filtered_df.sort_values(by="Expected Value", ascending=False)

st.subheader(f"Top Deals for {quarter}")
st.dataframe(ranked_df[[
    "Deal Name", "Associated Company (Primary)", "Amount", "Deal probability",
    "Expected Value", "Close Date"
]])

# --- Monte Carlo Simulation ---
st.subheader("📈 Monte Carlo Simulation: Pipeline Revenue Outcomes")

num_simulations = st.slider("Number of Simulations", 100, 10000, 1000, step=100)

simulated_totals = []

for _ in range(num_simulations):
    simulated_revenue = 0
    for _, row in ranked_df.iterrows():
        win = np.random.rand() < row["Deal probability"]
        if win:
            simulated_revenue += row["Amount"]
    simulated_totals.append(simulated_revenue)

# Plot histogram
fig, ax = plt.subplots()
ax.hist(simulated_totals, bins=30, color='skyblue', edgecolor='black')
ax.set_title("Distribution of Simulated Pipeline Revenue")
ax.set_xlabel("Total Revenue ($)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Show statistics
st.markdown(f"**Mean Expected Revenue:** ${np.mean(simulated_totals):,.0f}")
st.markdown(f"**10th Percentile (pessimistic):** ${np.percentile(simulated_totals, 10):,.0f}")
st.markdown(f"**90th Percentile (optimistic):** ${np.percentile(simulated_totals, 90):,.0f}")
