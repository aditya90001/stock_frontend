import streamlit as st
import requests
import pandas as pd

API_URL = "https://stock-price-prediction-7.onrender.com"

st.set_page_config(
    page_title="AI Stock Price Predictor",
    page_icon="",
    layout="wide"
)

# Header
st.title("📈 AI Stock Price Prediction Dashboard")
st.markdown(
    """
    Predict the next **60 trading days** using a Deep Learning model.
    
    ### Example Symbols
    -  AAPL
    -  MSFT
    -  NFLX(netflix)
    -  TCS.NS
    """
)

st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    stock = st.text_input(
        "Enter Stock Symbol",
        placeholder="AAPL"
    )

with col2:
    st.write("")
    st.write("")
    analyze = st.button("🚀 Analyze")

# Quick Examples
st.subheader("Quick Select")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("AAPL"):
        stock = "AAPL"

with c2:
    if st.button("MSFT"):
        stock = "MSFT"

with c3:
    if st.button("TSLA"):
        stock = "TSLA"

with c4:
    if st.button("BAJFINANCE.NS"):
        stock = "BAJFINANCE.NS"

if analyze:

    if not stock:
        st.warning("Please enter a stock symbol.")
        st.stop()

    with st.spinner("Analyzing stock and generating predictions..."):

        try:

            response = requests.post(
                f"{API_URL}/analyze_stock",
                data={"stock": stock}
            )

            if response.status_code != 200:
                st.error(response.json())
                st.stop()

            data = response.json()

            st.success(f"Analysis completed for {stock}")

            st.metric(
                "Last Market Date",
                data["last_market_date"]
            )

            st.subheader("📊 Prediction Chart")

            chart_url = (
                f"{API_URL}"
                f"{data['charts']['prediction']}"
            )

            st.image(chart_url, use_container_width=True)

            st.subheader("📅 Next 60-Day Forecast")

            df = pd.DataFrame(data["data_preview"])

            st.dataframe(
                df,
                use_container_width=True
            )

            csv_url = (
                f"{API_URL}/get_predictions/{stock}"
            )

            pred_response = requests.get(csv_url)

            if pred_response.status_code == 200:

                pred_df = pd.DataFrame(
                    pred_response.json()["next_60_days"]
                )

                csv = pred_df.to_csv(index=False)

                st.download_button(
                    label="⬇ Download Predictions CSV",
                    data=csv,
                    file_name=f"{stock}_predictions.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(str(e))

st.divider()

st.markdown(
    """
    ### Tech Stack
    
    - FastAPI Backend
    - Deep Learning Model (LSTM)
    - 
    - Yahoo Finance Data
    - Streamlit Frontend
    - 
    - Render Deployment
    """
)