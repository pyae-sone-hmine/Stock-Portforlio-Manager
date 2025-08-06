import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

# Import our custom modules
from data_fetch import (
    fetch_stock_data, 
    fetch_spy_data, 
    fetch_news_headlines, 
    fetch_analyst_recommendations,
    calculate_portfolio_performance,
    fetch_stock_data_multiple_timeframes
)
from analysis import (
    analyze_portfolio, 
    calculate_portfolio_metrics,
    format_currency,
    format_percentage,
    get_sentiment_color,
    get_momentum_color,
    get_recommendation_color
)
from charts import (
    create_stock_chart,
    create_price_performance_chart,
    create_portfolio_summary_chart,
    create_sentiment_analysis_chart,
    create_recommendation_chart
)

# Page configuration
st.set_page_config(
    page_title="Stock Portfolio Manager",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .positive { color: #28a745; }
    .negative { color: #dc3545; }
    .neutral { color: #6c757d; }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    .stock-input-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Reduce spacing between sections */
    .stExpander {
        margin-bottom: 0.5rem !important;
        border: 1px solid #e9ecef !important;
        border-radius: 0.5rem !important;
    }
    .stExpander > div > div {
        padding: 0.5rem !important;
    }
    /* Reduce spacing between chart and analysis */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    /* Compact layout for analysis summary */
    .analysis-summary {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
    }
    /* Clean sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    /* Better button styling */
    .stButton > button {
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Clean table styling */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    /* Remove footer */
    .footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Advanced Stock Portfolio Manager</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Investment Analysis & Interactive Charts")
    
    # Sidebar for input
    with st.sidebar:
        st.header("Portfolio Input")
        
        # Initialize session state for stocks if not exists
        if 'stocks' not in st.session_state:
            st.session_state.stocks = []
        
        # Stock input section
        st.markdown('<div class="stock-input-container">', unsafe_allow_html=True)
        st.subheader("Add Stocks")
        
        # Popular stocks suggestions
        popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "JPM", "JNJ"]
        
        # Show popular stocks as quick add buttons
        st.write("**Quick Add Popular Stocks:**")
        popular_cols = st.columns(5)
        for i, stock in enumerate(popular_stocks):
            with popular_cols[i % 5]:
                if st.button(stock, key=f"quick_{stock}", use_container_width=True):
                    if stock not in st.session_state.stocks:
                        st.session_state.stocks.append(stock)
                        st.success(f"✅ Added {stock}")
                        st.rerun()
                    else:
                        st.error(f"❌ {stock} is already in your portfolio")
        
        st.markdown("---")
        
        # Text input for new stock
        new_stock = st.text_input(
            "Enter Stock Ticker",
            placeholder="e.g., AAPL",
            help="Enter a stock ticker symbol and click 'Add Stock'"
        ).strip().upper()
        
        # Add stock button
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ Add Stock", type="primary", use_container_width=True):
                if new_stock:
                    if new_stock not in st.session_state.stocks:
                        # Basic validation - check if it's a valid ticker format
                        if len(new_stock) <= 5 and new_stock.isalpha():
                            st.session_state.stocks.append(new_stock)
                            st.success(f"✅ Added {new_stock}")
                            st.rerun()
                        else:
                            st.error("❌ Please enter a valid stock ticker (1-5 letters)")
                    else:
                        st.error(f"❌ {new_stock} is already in your portfolio")
                else:
                    st.error("❌ Please enter a stock ticker")
        
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.stocks = []
                st.success("✅ Portfolio cleared")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display current stocks
        if st.session_state.stocks:
            st.subheader("Current Portfolio")
            for i, stock in enumerate(st.session_state.stocks):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {stock}")
                with col2:
                    if st.button(f"❌", key=f"remove_{i}"):
                        st.session_state.stocks.pop(i)
                        st.success(f"✅ Removed {stock}")
                        st.rerun()
        else:
            st.info("👈 Add stocks to your portfolio to get started")
        
        # Analysis button
        if st.session_state.stocks:
            st.markdown("---")
            analyze_button = st.button("🚀 Analyze Portfolio", type="primary", use_container_width=True)
        else:
            analyze_button = False
    
    # Main content area
    if analyze_button and st.session_state.stocks:
        with st.spinner("Fetching market data and analyzing portfolio..."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Fetch stock data
            status_text.text("Fetching stock price data...")
            stock_data = fetch_stock_data(st.session_state.stocks)
            progress_bar.progress(25)
            
            # Step 2: Fetch SPY data
            status_text.text("Fetching SPY benchmark data...")
            spy_data = fetch_spy_data()
            progress_bar.progress(40)
            
            # Step 3: Fetch news headlines
            status_text.text("Fetching news headlines...")
            news_data = {}
            for i, ticker in enumerate(st.session_state.stocks):
                if ticker in stock_data:
                    news_data[ticker] = fetch_news_headlines(ticker)
                progress_bar.progress(40 + (i + 1) * 20 // len(st.session_state.stocks))
            
            # Step 4: Fetch analyst recommendations
            status_text.text("Fetching analyst recommendations...")
            analyst_data = {}
            for ticker in st.session_state.stocks:
                if ticker in stock_data:
                    analyst_data[ticker] = fetch_analyst_recommendations(ticker)
            
            progress_bar.progress(80)
            
            # Step 5: Analyze portfolio
            status_text.text("Analyzing portfolio and generating recommendations...")
            analysis_results = analyze_portfolio(stock_data, news_data, analyst_data)
            portfolio_metrics = calculate_portfolio_metrics(analysis_results)
            performance_data = calculate_portfolio_performance(stock_data, spy_data)
            
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
        
        # Display results
        if analysis_results:
            display_enhanced_results(analysis_results, portfolio_metrics, performance_data, spy_data, stock_data)
        else:
            st.error("No data could be fetched for the provided tickers. Please check the ticker symbols and try again.")
    
    elif not st.session_state.stocks:
        st.info("👈 Please add stocks to your portfolio in the sidebar to get started.")
    
    # Footer removed for cleaner UI

def display_enhanced_results(analysis_results, portfolio_metrics, performance_data, spy_data, stock_data):
    """Display the enhanced analysis results with charts and interactive features"""
    
    # Portfolio Performance Overview
    st.header("📊 Portfolio Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if performance_data:
            st.metric(
                "Portfolio YTD Return",
                format_percentage(performance_data['portfolio_return']),
                delta=format_percentage(performance_data['outperformance'])
            )
        else:
            st.metric("Portfolio YTD Return", "N/A")
    
    with col2:
        if spy_data:
            st.metric("SPY YTD Return", format_percentage(spy_data['ytd_return']))
        else:
            st.metric("SPY YTD Return", "N/A")
    
    with col3:
        st.metric("Total Stocks", portfolio_metrics['total_stocks'])
    
    with col4:
        st.metric(
            "Avg Sentiment Score", 
            f"{portfolio_metrics['avg_sentiment']:.3f}",
            delta="Positive" if portfolio_metrics['avg_sentiment'] > 0.05 else "Negative" if portfolio_metrics['avg_sentiment'] < -0.05 else "Neutral"
        )
    
    # Portfolio Performance Chart
    st.subheader("📈 Portfolio Performance vs Benchmark")
    performance_chart = create_price_performance_chart(stock_data, spy_data)
    if performance_chart:
        st.plotly_chart(performance_chart, use_container_width=True)
    
    # Portfolio Summary Charts
    st.subheader("📊 Portfolio Summary")
    summary_chart = create_portfolio_summary_chart(analysis_results)
    if summary_chart:
        st.plotly_chart(summary_chart, use_container_width=True)
    
    # Sentiment Analysis Chart
    st.subheader("🧠 Sentiment Analysis")
    sentiment_chart = create_sentiment_analysis_chart(analysis_results)
    if sentiment_chart:
        st.plotly_chart(sentiment_chart, use_container_width=True)
    
    # Recommendation Distribution
    st.subheader("🎯 Recommendation Distribution")
    recommendation_chart = create_recommendation_chart(analysis_results)
    if recommendation_chart:
        st.plotly_chart(recommendation_chart, use_container_width=True)
    
    # Enhanced Portfolio Metrics
    st.header("📈 Enhanced Portfolio Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Recommendations")
        st.write(f"🟢 Strong Buy: {portfolio_metrics['strong_buy_recommendations']}")
        st.write(f"🟢 Buy: {portfolio_metrics['buy_recommendations']}")
        st.write(f"🟡 Hold: {portfolio_metrics['hold_recommendations']}")
        st.write(f"🔴 Consider Selling: {portfolio_metrics['sell_recommendations']}")
        st.write(f"🔴 Strong Sell: {portfolio_metrics['strong_sell_recommendations']}")
    
    with col2:
        st.subheader("Momentum Signals")
        st.write(f"🟢 Strong Bullish: {portfolio_metrics['strong_bullish_momentum']}")
        st.write(f"🟢 Bullish: {portfolio_metrics['bullish_momentum']}")
        st.write(f"🟡 Neutral: {portfolio_metrics['neutral_momentum']}")
        st.write(f"🔴 Bearish: {portfolio_metrics['bearish_momentum']}")
        st.write(f"🔴 Strong Bearish: {portfolio_metrics['strong_bearish_momentum']}")
    
    with col3:
        st.subheader("Technical Trends")
        st.write(f"🟢 Uptrend: {portfolio_metrics['uptrend_count']}")
        st.write(f"🔴 Downtrend: {portfolio_metrics['downtrend_count']}")
        st.write(f"🟡 Sideways: {portfolio_metrics['sideways_count']}")
    
    # Enhanced Stock Analysis Table
    st.header("📋 Enhanced Stock Analysis")
    
    # Create DataFrame for display
    table_data = []
    for ticker, data in analysis_results.items():
        table_data.append({
            'Ticker': ticker,
            'Company': data['company_name'],
            'Current Price': format_currency(data['current_price']),
            '1D Change': format_percentage(data['price_changes']['price_change_1d']),
            '1M Change': format_percentage(data['price_changes']['price_change_1m']),
            'RSI': f"{data['rsi']:.1f}",
            'Momentum': data['momentum'],
            'Sentiment': data['sentiment'],
            'Technical Trend': data['technical_analysis']['trend'],
            'Recommendation': data['recommendation']['action'],
            'Confidence': data['recommendation']['confidence']
        })
    
    df = pd.DataFrame(table_data)
    
    # Display table with custom formatting
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Individual Stock Details with Charts
    st.header("📰 Individual Stock Analysis & Charts")
    
    for ticker, data in analysis_results.items():
        with st.expander(f"📊 {ticker} - {data['company_name']} - {data['recommendation']['action']}"):
            
            # Stock chart
            st.subheader(f"📈 {ticker} Stock Chart")
            stock_chart = create_stock_chart(ticker, stock_data[ticker])
            if stock_chart:
                st.plotly_chart(stock_chart, use_container_width=True)
            
            # Analysis Summary
            st.subheader("📊 Analysis Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Momentum", data['momentum'], delta=None)
            
            with col2:
                st.metric("Sentiment", data['sentiment'], delta=None)
            
            with col3:
                st.metric("Recommendation", data['recommendation']['action'], delta=None)
            
            with col4:
                confidence_value = data['recommendation']['confidence']
                if isinstance(confidence_value, (int, float)):
                    st.metric("Confidence", f"{confidence_value:.1f}%", delta=None)
                else:
                    st.metric("Confidence", confidence_value, delta=None)
            
            # Recommendation Reasoning
            st.subheader("💡 Recommendation Reasoning")
            st.write(data['recommendation']['reasoning'])
            
            # News headlines
            if data['headlines']:
                st.subheader("📰 Latest News")
                for i, headline in enumerate(data['headlines'][:3]):
                    st.write(f"**{i+1}.** {headline['title']}")
                    st.caption(f"Published: {headline['published']}")
                    if i < 2:  # Don't add separator after last item
                        st.write("---")
            else:
                st.info("No recent news headlines available for this stock.")

if __name__ == "__main__":
    main() 