This program creates an interactive dashboard that:

Scrapes product data from any e-commerce website (you'll need to adjust the CSS selectors based on the specific site)
Analyzes the data to show:

Average price and rating
Total review count
Price range
Price distribution
Price vs. Rating scatter plot


Displays the raw data in a table format

To run this program, you'll need to install the required packages:

# packages
# bash

# pip install streamlit selenium webdriver-manager pandas plotly

Then run it with:

# bash
# streamlit run your_script.py

Key features:

Uses headless Chrome browser for scraping
Interactive sidebar controls for URL and sample size
Error handling for failed scraping attempts
Session state management to persist data between reruns
Interactive Plotly visualizations
Responsive layout with metrics and charts



