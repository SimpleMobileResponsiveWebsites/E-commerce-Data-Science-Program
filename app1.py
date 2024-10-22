import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import plotly.express as px
import time

def setup_selenium():
    """Configure and return a headless Chrome browser instance"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_product_data(url, num_products=20):
    """Scrape product data from the e-commerce website"""
    driver = setup_selenium()
    driver.get(url)
    time.sleep(2)  # Wait for page to load
    
    products = []
    try:
        # Example selectors - adjust based on actual website structure
        product_elements = driver.find_elements(By.CLASS_NAME, "product-card")[:num_products]
        
        for element in product_elements:
            product = {
                'name': element.find_element(By.CLASS_NAME, "product-name").text,
                'price': float(element.find_element(By.CLASS_NAME, "product-price").text.replace("$", "")),
                'rating': float(element.find_element(By.CLASS_NAME, "product-rating").text),
                'reviews': int(element.find_element(By.CLASS_NAME, "review-count").text.split()[0])
            }
            products.append(product)
    
    finally:
        driver.quit()
    
    return pd.DataFrame(products)

def analyze_data(df):
    """Perform basic analysis on the scraped data"""
    analysis = {
        'avg_price': df['price'].mean(),
        'avg_rating': df['rating'].mean(),
        'total_reviews': df['reviews'].sum(),
        'price_range': (df['price'].min(), df['price'].max())
    }
    return analysis

def main():
    st.title("E-commerce Product Analysis Dashboard")
    
    # Sidebar inputs
    st.sidebar.header("Data Collection Settings")
    url = st.sidebar.text_input("Enter E-commerce URL")
    num_products = st.sidebar.slider("Number of products to analyze", 5, 50, 20)
    
    if st.sidebar.button("Collect Data") and url:
        with st.spinner("Collecting data..."):
            try:
                # Collect and analyze data
                df = scrape_product_data(url, num_products)
                analysis = analyze_data(df)
                
                # Store in session state
                st.session_state['data'] = df
                st.session_state['analysis'] = analysis
                st.success("Data collected successfully!")
            except Exception as e:
                st.error(f"Error collecting data: {str(e)}")
    
    # Display analysis if data is available
    if 'data' in st.session_state:
        df = st.session_state['data']
        analysis = st.session_state['analysis']
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Price", f"${analysis['avg_price']:.2f}")
        col2.metric("Average Rating", f"{analysis['avg_rating']:.1f}/5.0")
        col3.metric("Total Reviews", analysis['total_reviews'])
        col4.metric("Price Range", f"${analysis['price_range'][0]:.2f} - ${analysis['price_range'][1]:.2f}")
        
        # Create visualizations
        st.subheader("Price Distribution")
        fig_price = px.histogram(df, x="price", nbins=20)
        st.plotly_chart(fig_price)
        
        st.subheader("Price vs Rating")
        fig_scatter = px.scatter(df, x="price", y="rating", size="reviews",
                               hover_data=["name"])
        st.plotly_chart(fig_scatter)
        
        # Display raw data
        st.subheader("Raw Data")
        st.dataframe(df)

if __name__ == "__main__":
    main()
