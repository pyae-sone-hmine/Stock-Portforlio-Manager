# 📈 Stock Portfolio Manager

A comprehensive **MVP web application** built with Python and Streamlit that helps long-term investors manage their stock portfolio through data-driven analysis and recommendations.

## 🎯 Features

### Core Functionality
- **Stock Data Analysis**: Fetch real-time stock prices and calculate 50-day & 200-day moving averages
- **News Sentiment Analysis**: Analyze news headlines using VADER sentiment analysis
- **Analyst Recommendations**: Scrape analyst consensus from Yahoo Finance
- **Portfolio Performance**: Compare portfolio returns vs SPY (S&P 500 ETF)
- **Smart Recommendations**: Rule-based decision engine combining momentum, sentiment, and analyst signals

### Dashboard Features
- **Portfolio Overview**: YTD returns, performance vs benchmark
- **Stock Analysis Table**: Comprehensive view of all stocks with key metrics
- **Individual Stock Details**: Expandable sections with detailed analysis and news
- **Visual Indicators**: Color-coded signals for momentum, sentiment, and recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd stock_analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## 📊 How to Use

### 1. Input Your Portfolio
- In the sidebar, enter your stock tickers separated by commas
- Example: `AAPL, MSFT, GOOGL, AMZN, TSLA`
- Click "🚀 Analyze Portfolio" to start the analysis

### 2. Review Results
The app will display:

#### Portfolio Performance Overview
- Portfolio YTD Return vs SPY benchmark
- Total number of stocks analyzed
- Average sentiment score across portfolio

#### Portfolio Metrics
- **Recommendations**: Buy More, Hold, Consider Selling counts
- **Momentum Signals**: Bullish, Bearish, Neutral distribution
- **Analyst Consensus**: Buy, Hold, Sell distribution

#### Stock Analysis Table
- Current price and moving averages
- Momentum signal (Bullish/Bearish)
- Sentiment analysis results
- Analyst consensus
- Final recommendation

#### Individual Stock Details
- Expandable sections for each stock
- Detailed metrics and analysis
- Latest news headlines with sentiment

## 🔧 Technical Architecture

### File Structure
```
stock_analysis/
├── app.py              # Main Streamlit application
├── data_fetch.py       # Data fetching and API calls
├── analysis.py         # Analysis and decision logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Key Components

#### `data_fetch.py`
- **Stock Data**: Uses `yfinance` for price history and moving averages
- **News Headlines**: Google News RSS feed via `feedparser`
- **Analyst Ratings**: Web scraping Yahoo Finance with `BeautifulSoup`
- **SPY Benchmark**: S&P 500 ETF data for comparison

#### `analysis.py`
- **Sentiment Analysis**: VADER sentiment analysis on news headlines
- **Momentum Calculation**: 50-day vs 200-day moving average comparison
- **Decision Engine**: Weighted scoring system for recommendations
- **Portfolio Metrics**: Aggregated portfolio-level statistics

#### `app.py`
- **Streamlit UI**: Clean, responsive web interface
- **Progress Tracking**: Real-time progress bars during analysis
- **Data Display**: Interactive tables and expandable sections
- **Error Handling**: Graceful handling of API failures

## 📈 Analysis Methodology

### Momentum Signal
- **Bullish**: 50-day MA > 200-day MA
- **Bearish**: 50-day MA < 200-day MA
- **Neutral**: Insufficient data

### Sentiment Analysis
- **Positive**: Compound score > 0.05
- **Negative**: Compound score < -0.05
- **Neutral**: Between -0.05 and 0.05

### Recommendation Logic
Weighted scoring system:
- **Momentum**: 40% weight
- **Sentiment**: 30% weight
- **Analyst Consensus**: 30% weight

**Recommendations:**
- **Buy More**: Score > 0.5
- **Hold**: Score between -0.2 and 0.5
- **Consider Selling**: Score < -0.2

## ⚠️ Important Notes

### Data Sources
- **Stock Data**: Yahoo Finance (via yfinance)
- **News**: Google News RSS feed
- **Analyst Ratings**: Yahoo Finance (web scraping)

### Limitations
- **Rate Limiting**: Some data sources may have rate limits
- **Data Accuracy**: Web scraping may be affected by website changes
- **Educational Use**: This tool is for educational purposes only
- **No Financial Advice**: Always do your own research before investing

### Troubleshooting

#### Common Issues
1. **"No data found" errors**
   - Check ticker symbols are correct
   - Ensure internet connection is stable
   - Some international stocks may not be available

2. **Slow loading times**
   - Reduce number of stocks analyzed
   - Check internet connection speed
   - Some data sources may be temporarily unavailable

3. **Missing news or analyst data**
   - Web scraping may fail due to website changes
   - Some stocks may have limited news coverage
   - Analyst data may not be available for all stocks

## 🔮 Future Enhancements

### Potential Improvements
- **Database Integration**: Store historical analysis data
- **Email Alerts**: Notifications for significant changes
- **Portfolio Tracking**: Track actual portfolio performance over time
- **Advanced Charts**: Interactive price charts with technical indicators
- **Risk Analysis**: Volatility and risk metrics
- **Sector Analysis**: Group stocks by sector for analysis
- **Export Features**: Download analysis reports as PDF/Excel

### Technical Improvements
- **Caching**: Cache frequently accessed data
- **Async Processing**: Parallel data fetching for faster analysis
- **Error Recovery**: Better handling of API failures
- **Mobile Optimization**: Better mobile device support

## 📝 License

This project is for educational purposes. Please ensure compliance with data source terms of service.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Disclaimer**: This application is for educational purposes only. It does not constitute financial advice. Always conduct your own research and consult with financial professionals before making investment decisions. 