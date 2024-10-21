import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* General Layout Styles */
    body {
        background-color: #1E2D56; /* Dark background for a professional look */
    }

    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 40px;
        letter-spacing: 1.5px;
    }

    .subheader {
        font-size: 1.6rem;
        color: #ffffff;
        margin-bottom: 10px;
        margin-top: 30px;
        font-weight: 600;
        border-bottom: 2px solid #ffffff;
        padding-bottom: 5px;
    }

    .description {
        font-size: 1rem;
        color: #ffffff;
        margin-bottom: 20px;
        text-align: justify;
    }

    .info-box {
        background-color: #1E2D56;
        border: 2px solid #ffffff;
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 5px;
        color: #ffffff;
    }

    .calculator-box {
        background-color: #1E2D56;
        border: 2px solid #ffffff;
        box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 10px;
        margin-top: 20px;
        color: #ffffff;
    }

    .calculator-header {
        font-weight: bold;
        font-size: 1.2rem;
        color: #ffffff;
    }

    .highlight {
        color: #ffffff;
        font-weight: bold;
    }

    .btn-primary {
        background-color: #ffffff;
        color: #1E2D56;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .btn-primary:hover {
        background-color: #CCCCCC;
    }

    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #888888;
        margin-top: 40px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Load scheme code to name mapping
with open('scheme_code_to_name.json', 'r') as f:
    scheme_code_to_name = json.load(f)

# Load date to NAV mapping
with open('date_to_nav_mapping.json', 'r') as f:
    date_to_nav_mapping = json.load(f)

# Utility functions
def calculate_returns(nav_list):
    returns = []
    for i in range(1, len(nav_list)):
        if nav_list[i - 1] == 0:
            returns.append(0)
        else:
            returns.append((nav_list[i] - nav_list[i - 1]) / nav_list[i - 1] * 100)
    return returns

def calculate_sharpe_ratio(returns):
    if len(returns) == 0:
        return np.nan
    avg_return = np.mean(returns)
    return_stdev = np.std(returns)
    if return_stdev == 0:
        return np.inf
    sharpe_ratio = avg_return / return_stdev
    return sharpe_ratio

def get_scheme_nav(scheme_code):
    scheme_nav = {}
    for date, schemes in date_to_nav_mapping.items():
        if scheme_code in schemes:
            scheme_nav[date] = schemes[scheme_code]
    return scheme_nav

def get_top_funds_by_metric(metric="returns"):
    scheme_metrics = {}
    for scheme_code, scheme_name in scheme_code_to_name.items():
        scheme_nav = get_scheme_nav(scheme_code)
        if len(scheme_nav) > 1:
            sorted_nav = [nav for date, nav in sorted(scheme_nav.items(), key=lambda x: datetime.strptime(x[0], '%d-%b-%Y'))]
            returns = calculate_returns(sorted_nav)
            if metric == "returns":
                scheme_metrics[scheme_name] = np.sum(returns)
            elif metric == "sharpe":
                scheme_metrics[scheme_name] = calculate_sharpe_ratio(returns)

    top_schemes = sorted(scheme_metrics.items(), key=lambda x: x[1], reverse=True)[:5]
    return top_schemes

def plot_nav_trend(scheme_code):
    scheme_nav = get_scheme_nav(scheme_code)
    if len(scheme_nav) == 0:
        st.write(f"No data available for scheme: {scheme_code_to_name[scheme_code]}")
        return

    # Sort the dates and corresponding NAV values
    dates = [datetime.strptime(date, '%d-%b-%Y') for date in scheme_nav.keys()]
    nav_values = [nav for _, nav in sorted(zip(dates, scheme_nav.values()))]

    # Plotting the NAV trend with a visible line color
    fig, ax = plt.subplots()
    ax.plot(sorted(dates), nav_values, color='yellow', linewidth=2)  # Changed the color to yellow for better visibility
    ax.set_facecolor('#1E2D56')  # Set the background color of the plot to match the page
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("NAV", color='white')
    ax.set_title(f"NAV Trend for {scheme_code_to_name[scheme_code]}", color='white')
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.tick_params(colors='white')  # Change tick colors to white for better visibility
    st.pyplot(fig)

def sip_calculator(sip_amount, sip_duration, expected_annual_return):
    monthly_rate_of_return = (1 + expected_annual_return / 100) ** (1 / 12) - 1
    future_value = sip_amount * ((1 + monthly_rate_of_return) ** sip_duration - 1) * (1 + monthly_rate_of_return) / monthly_rate_of_return
    return future_value

# Streamlit app layout
st.markdown('<div class="title">Mutual Fund NAV Analysis Dashboard</div>', unsafe_allow_html=True)

# Display all elements in a grid format for better alignment
st.markdown('<div class="subheader">Top 5 Mutual Funds by Returns</div>', unsafe_allow_html=True)
st.markdown('<div class="description">This section lists the top-performing mutual funds based on their cumulative returns, providing a clear insight into which funds have delivered the best performance over the selected period.</div>', unsafe_allow_html=True)
top_returns_funds = get_top_funds_by_metric(metric="returns")
returns_df = pd.DataFrame(top_returns_funds, columns=["Scheme", "Total Returns"])
st.table(returns_df)

st.markdown('<div class="subheader">Top 5 Mutual Funds by Sharpe Ratio</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Discover the mutual funds that offer the best risk-adjusted returns, ranked by their Sharpe Ratio to highlight those with the most consistent performance relative to their risk.</div>', unsafe_allow_html=True)
top_sharpe_funds = get_top_funds_by_metric(metric="sharpe")
sharpe_df = pd.DataFrame(top_sharpe_funds, columns=["Scheme", "Sharpe Ratio"])
st.table(sharpe_df)

st.markdown('<div class="subheader">Historical NAV Trend</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Explore the historical performance of mutual funds by analyzing the Net Asset Value (NAV) trend over time. This visual representation aids in understanding the fund\'s growth trajectory.</div>', unsafe_allow_html=True)
selected_scheme_name = st.selectbox("Select a Scheme", list(scheme_code_to_name.values()))
selected_scheme_code = [code for code, name in scheme_code_to_name.items() if name == selected_scheme_name][0]
plot_nav_trend(selected_scheme_code)

st.markdown('<div class="subheader">SIP Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Calculate the future value of your investments through a Systematic Investment Plan (SIP) using this intuitive tool designed to help you plan your financial future.</div>', unsafe_allow_html=True)
st.markdown('<div class="calculator-box">', unsafe_allow_html=True)

sip_amount = st.number_input("Monthly SIP Amount (₹)", min_value=1000, step=1000)
sip_duration = st.number_input("Duration (Months)", min_value=12, step=1)
expected_return = st.number_input("Expected Annual Return (%)", min_value=1.0, step=0.5)

if st.button("Calculate Future Value"):
    future_value = sip_calculator(sip_amount, sip_duration, expected_return)
    st.markdown(f"<div class='calculator-header'>Future Value of SIP: ₹{future_value:,.2f}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Mutual funds are subject to market risks. Read all the scheme related information carefully before investing.</div>', unsafe_allow_html=True)