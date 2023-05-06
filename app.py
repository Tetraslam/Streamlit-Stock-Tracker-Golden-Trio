import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io

def main():
    st.set_page_config(layout="wide", page_title="Stock Price Comparison", page_icon=":chart_with_upwards_trend:")

    # Set dark theme
    dark_theme = "dark"
    st.markdown(f"""
        <style>
            .reportview-container .main .block-container {{
                color: white;
                background-color: #262730;
            }}
            .reportview-container .main {{
                color: white;
                background-color: #262730;
            }}
        </style>
        """, unsafe_allow_html=True)

    st.title("Stock Price Comparison")

    # Define the tickers
    tickers = ['AMD', 'INTC', 'NVDA']

    # Get the historical data for the tickers
    data = yf.download(tickers, period='1mo', interval='1d')['Adj Close']

    # Create a dataframe with dates as index and stock prices as columns
    df = pd.DataFrame(data)
    df.columns = tickers

    # Convert the index to DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Plot the stock prices
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Stock Price Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")

    # Format the x-axis labels
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))

    # Plot the line graph
    for ticker in tickers:
        ax.plot(df.index, df[ticker], label=ticker)

    # Initialize session_state.x
    if 'x' not in st.session_state:
        st.session_state.x = 0

    # Get the mouse position
    xdata = ax.get_xaxis().get_data_interval()
    x_min = max(int(xdata[0]), 0)
    x_max = min(int(xdata[1]), len(df) - 2)

    # Limit the session_state.x value within the valid range
    st.session_state.x = max(min(st.session_state.x, x_max), x_min)

    # Get the updated mouse position
    x_index = min(st.session_state.x, len(df) - 1)
    x_date = df.index[x_index] if len(df) > 0 else None

    # Display the stock prices based on mouse position
    if x_date is not None:
        st.write("Date:", x_date.strftime("%Y-%m-%d"))
        for ticker in tickers:
            st.write(f"{ticker} Price:", round((df.loc[x_date, ticker]), 2))

    # Create a BytesIO object to save the figure
    fig_buffer = io.BytesIO()

    # Save the figure to the BytesIO object
    plt.savefig(fig_buffer, format='png')

    # Move the file cursor
    # Move the file cursor to the beginning of the buffer
    fig_buffer.seek(0)

    # Display the figure using st.image
    st.image(fig_buffer)

if __name__ == "__main__":
    main()
