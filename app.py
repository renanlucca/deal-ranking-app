import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("TestData.csv")
    df["Amount"] = df["Amount"].replace('[\$,]', '', regex=True).astype(float)
    df["Close Date"] = pd.to_datetime(df["Close Date"])
    df["Quarter"] = "Q" + df["Close Date"].dt.quarter.astype(str) + "-" + df["Close Date"].dt.year.astype(str)
    df["Expected Value"] = df["Amount"] * df["Deal probability"]
    return df

df = load_data()

st.title("📊 Deal Ranking by Expected Value")
quarter_options = sorted(df["Quarter"].unique().tolist())
quarter = st.selectbox("Select a Quarter", ["Full Year"] + quarter_options)

if quarter == "Full Year":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Quarter"] == quarter]

ranked_df = filtered_df.sort_values(by="Expected Value", ascending=False)

st.subheader(f"Top Deals for {quarter}")
st.dataframe(ranked_df[[
    "Deal Name", "Associated Company (Primary)", "Amount", "Deal probability",
    "Expected Value", "Close Date"
]])
