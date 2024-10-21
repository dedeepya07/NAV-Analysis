Mutual Fund NAV Analysis Dashboard

This repository hosts the Mutual Fund NAV Analysis Dashboard, a sophisticated and intuitive analytical tool built using Streamlit. Designed to provide actionable insights into mutual fund performance, the dashboard enables users to make informed investment decisions through comprehensive financial metrics, interactive visualizations, and precise forecasting tools.

Core Functionalities

	•	Top 5 Mutual Funds by Returns: Offers a ranked list of mutual funds exhibiting the highest cumulative returns over a predefined period, allowing users to identify funds with superior growth trajectories.
	•	Top 5 Mutual Funds by Sharpe Ratio: Provides a risk-adjusted performance ranking by calculating the Sharpe Ratio for mutual funds, highlighting those that deliver optimal returns for a given level of risk.
	•	Historical NAV Trend Visualization: Displays the historical evolution of the Net Asset Value (NAV) for selected mutual funds, offering a granular view of fund performance across timeframes.
	•	SIP (Systematic Investment Plan) Calculator: Empowers users to project the future value of their investments based on customizable parameters such as monthly contribution, investment horizon, and expected annual returns.

System Requirements

	•	Python 3.12 or higher
	•	Streamlit for application development and deployment
	•	Pandas for data manipulation and analysis
	•	Matplotlib for rendering sophisticated visualizations
	•	JSON data files containing the mutual fund NAV data (scheme_code_to_name.json and date_to_nav_mapping.json)

Features in Detail

	1.	Real-Time Data Analysis: The dashboard computes critical financial metrics, such as cumulative returns and Sharpe ratios, using historical NAV data, ensuring users can assess both short- and long-term fund performance with precision.
	2.	Intuitive User Interface: The platform is designed with a clean, professional aesthetic, allowing for effortless navigation and interaction. Visual elements, such as tables and graphs, are seamlessly integrated to enrich the user experience.
	3.	SIP Forecasting: The SIP calculator offers advanced financial modeling, providing users with an accurate projection of the future value of their investments. This allows investors to simulate potential outcomes based on varying input parameters.
	4.	Data-Driven Decision-Making: By presenting both returns and risk-adjusted returns (via the Sharpe ratio), the dashboard equips users with the necessary data to make informed, risk-sensitive investment choices.

Deployment Instructions

	1.	Clone the repository and install the required dependencies listed in the requirements.txt file.
	2.	Launch the application using Streamlit.
	3.	Analyze mutual fund performance by selecting a scheme, visualizing its historical NAV trend, and utilizing the SIP calculator for forward-looking financial projections.

Conclusion

This Mutual Fund NAV Analysis Dashboard serves as a comprehensive platform for investors and financial analysts alike. With its ability to combine historical performance data, risk-adjusted metrics, and future value projections, it empowers users to make strategic and data-driven investment decisions.
