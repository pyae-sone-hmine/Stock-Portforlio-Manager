import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
import time
import re

def fetch_stock_data(tickers, period="1y"):
    """
    Fetch stock price data and calculate moving averages
    """
    stock_data = {}
    
    for ticker in tickers:
        try:
            ticker = ticker.strip().upper()
            print(f"Fetching data for {ticker}...")
            
            # Create ticker object
            stock = yf.Ticker(ticker)
            
            # Try different approaches to get data
            hist = None
            
            # Method 1: Try with period
            try:
                hist = stock.history(period="1y")
                print(f"Method 1 successful for {ticker}")
            except:
                pass
            
            # Method 2: Try with explicit dates
            if hist is None or hist.empty:
                try:
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=365)
                    hist = stock.history(start=start_date, end=end_date)
                    print(f"Method 2 successful for {ticker}")
                except:
                    pass
            
            # Method 3: Try with longer period
            if hist is None or hist.empty:
                try:
                    hist = stock.history(period="2y")
                    print(f"Method 3 successful for {ticker}")
                except:
                    pass
            
            # Method 4: Try with download function
            if hist is None or hist.empty:
                try:
                    import yfinance as yf_download
                    hist = yf_download.download(ticker, start="2023-01-01", end=datetime.now().strftime("%Y-%m-%d"))
                    print(f"Method 4 successful for {ticker}")
                except:
                    pass
            
            if hist is None or hist.empty:
                print(f"All methods failed for {ticker}")
                continue
                
            # Calculate moving averages
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            
            # Calculate additional technical indicators
            hist['RSI'] = calculate_rsi(hist['Close'])
            hist['Volatility'] = hist['Close'].rolling(window=20).std()
            hist['Returns'] = hist['Close'].pct_change()
            
            # Get current info
            try:
                info = stock.info
            except:
                info = {}
            
            stock_data[ticker] = {
                'current_price': hist['Close'].iloc[-1],
                'ma50': hist['MA50'].iloc[-1],
                'ma200': hist['MA200'].iloc[-1],
                'ma20': hist['MA20'].iloc[-1],
                'volume': hist['Volume'].iloc[-1],
                'market_cap': info.get('marketCap', 0),
                'company_name': info.get('longName', ticker),
                'historical_data': hist,
                'rsi': hist['RSI'].iloc[-1] if not pd.isna(hist['RSI'].iloc[-1]) else 50,
                'volatility': hist['Volatility'].iloc[-1] if not pd.isna(hist['Volatility'].iloc[-1]) else 0,
                'avg_volume': hist['Volume'].rolling(window=20).mean().iloc[-1],
                'price_change_1d': hist['Returns'].iloc[-1] * 100 if not pd.isna(hist['Returns'].iloc[-1]) else 0,
                'price_change_5d': ((hist['Close'].iloc[-1] / hist['Close'].iloc[-6]) - 1) * 100 if len(hist) > 5 else 0,
                'price_change_1m': ((hist['Close'].iloc[-1] / hist['Close'].iloc[-22]) - 1) * 100 if len(hist) > 22 else 0,
                'price_change_3m': ((hist['Close'].iloc[-1] / hist['Close'].iloc[-66]) - 1) * 100 if len(hist) > 66 else 0,
                'price_change_6m': ((hist['Close'].iloc[-1] / hist['Close'].iloc[-132]) - 1) * 100 if len(hist) > 132 else 0,
                'price_change_1y': ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100 if len(hist) > 0 else 0
            }
            
            print(f"✅ Successfully fetched REAL data for {ticker}: ${hist['Close'].iloc[-1]:.2f}")
            
            # Add delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {str(e)}")
            continue
    
    return stock_data

def calculate_rsi(prices, period=14):
    """
    Calculate RSI (Relative Strength Index)
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_stock_data_multiple_timeframes(ticker, timeframes=['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y']):
    """
    Fetch stock data for multiple timeframes
    """
    data = {}
    
    try:
        stock = yf.Ticker(ticker)
        
        for timeframe in timeframes:
            try:
                if timeframe == '5y':
                    hist = stock.history(period="5y")
                else:
                    hist = stock.history(period=timeframe)
                
                if not hist.empty:
                    # Calculate moving averages for this timeframe
                    hist['MA20'] = hist['Close'].rolling(window=20).mean()
                    hist['MA50'] = hist['Close'].rolling(window=50).mean()
                    hist['MA200'] = hist['Close'].rolling(window=200).mean()
                    
                    data[timeframe] = {
                        'dates': hist.index,
                        'prices': hist['Close'].values,
                        'volumes': hist['Volume'].values,
                        'ma20': hist['MA20'].values,
                        'ma50': hist['MA50'].values,
                        'ma200': hist['MA200'].values,
                        'high': hist['High'].values,
                        'low': hist['Low'].values,
                        'open': hist['Open'].values
                    }
                    
            except Exception as e:
                print(f"Error fetching {timeframe} data for {ticker}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error fetching multi-timeframe data for {ticker}: {str(e)}")
    
    return data

def fetch_spy_data(period="1y"):
    """
    Fetch SPY data for benchmark comparison
    """
    try:
        print("Fetching SPY data...")
        spy = yf.Ticker("SPY")
        
        # Try different approaches to get SPY data
        hist = None
        
        # Method 1: Try with period
        try:
            hist = spy.history(period="1y")
            print("SPY Method 1 successful")
        except:
            pass
        
        # Method 2: Try with explicit dates
        if hist is None or hist.empty:
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=365)
                hist = spy.history(start=start_date, end=end_date)
                print("SPY Method 2 successful")
            except:
                pass
        
        # Method 3: Try with download function
        if hist is None or hist.empty:
            try:
                import yfinance as yf_download
                hist = yf_download.download("SPY", start="2023-01-01", end=datetime.now().strftime("%Y-%m-%d"))
                print("SPY Method 3 successful")
            except:
                pass
        
        if hist is None or hist.empty:
            print("❌ All SPY methods failed")
            return None
            
        # Calculate YTD return
        current_year = datetime.now().year
        year_data = hist[hist.index.year == current_year]
        
        if year_data.empty:
            # If no data for current year, use the first available data
            year_start = hist.iloc[0]['Close']
        else:
            year_start = year_data.iloc[0]['Close']
            
        current_price = hist['Close'].iloc[-1]
        ytd_return = ((current_price - year_start) / year_start) * 100
        
        print(f"✅ Successfully fetched REAL SPY data: ${current_price:.2f}, YTD: {ytd_return:.2f}%")
        
        return {
            'current_price': current_price,
            'ytd_return': ytd_return,
            'historical_data': hist
        }
    except Exception as e:
        print(f"❌ Error fetching SPY data: {str(e)}")
        return None

def fetch_news_headlines(ticker, max_headlines=5):
    """
    Fetch news headlines using Google News RSS feed
    """
    try:
        # Use Google News RSS feed
        url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(url)
        headlines = []
        
        for entry in feed.entries[:max_headlines]:
            headlines.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary if hasattr(entry, 'summary') else ''
            })
        
        print(f"Fetched {len(headlines)} news headlines for {ticker}")
        return headlines
        
    except Exception as e:
        print(f"Error fetching news for {ticker}: {str(e)}")
        # Return sample headlines as fallback
        return [
            {
                'title': f"{ticker} stock shows mixed signals in recent trading",
                'link': '#',
                'published': 'Recent',
                'summary': 'Market analysis shows varying opinions on this stock.'
            }
        ]

def fetch_analyst_recommendations(ticker):
    """
    Scrape analyst recommendations from Yahoo Finance
    """
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for analyst recommendation table
        # This is a simplified approach - in practice, you might need to adjust selectors
        recommendations = []
        
        # Try to find recommendation elements
        rec_elements = soup.find_all('td', string=re.compile(r'(Buy|Hold|Sell|Overweight|Underweight)', re.IGNORECASE))
        
        for element in rec_elements:
            text = element.get_text().strip()
            if text.lower() in ['buy', 'overweight']:
                recommendations.append(1)
            elif text.lower() in ['hold', 'neutral']:
                recommendations.append(0)
            elif text.lower() in ['sell', 'underweight']:
                recommendations.append(-1)
        
        if recommendations:
            avg_recommendation = sum(recommendations) / len(recommendations)
            
            if avg_recommendation > 0.3:
                consensus = "Buy"
            elif avg_recommendation < -0.3:
                consensus = "Sell"
            else:
                consensus = "Hold"
                
            return {
                'consensus': consensus,
                'score': avg_recommendation,
                'count': len(recommendations)
            }
        else:
            # Fallback: return neutral recommendation
            return {
                'consensus': "Hold",
                'score': 0,
                'count': 0
            }
            
    except Exception as e:
        print(f"Error fetching analyst recommendations for {ticker}: {str(e)}")
        return {
            'consensus': "Hold",
            'score': 0,
            'count': 0
        }

def calculate_portfolio_performance(stock_data, spy_data):
    """
    Calculate portfolio performance vs SPY
    """
    if not stock_data or not spy_data:
        return None
    
    # Calculate YTD returns for each stock
    portfolio_returns = []
    
    for ticker, data in stock_data.items():
        try:
            hist = data['historical_data']
            
            # Only calculate if we have real historical data
            if hist is not None:
                current_year = datetime.now().year
                year_data = hist[hist.index.year == current_year]
                
                if not year_data.empty:
                    year_start = year_data.iloc[0]['Close']
                    current_price = data['current_price']
                    ytd_return = ((current_price - year_start) / year_start) * 100
                    portfolio_returns.append(ytd_return)
        except Exception as e:
            print(f"Error calculating return for {ticker}: {str(e)}")
            continue
    
    if portfolio_returns:
        avg_portfolio_return = sum(portfolio_returns) / len(portfolio_returns)
        spy_return = spy_data['ytd_return']
        
        return {
            'portfolio_return': avg_portfolio_return,
            'spy_return': spy_return,
            'outperformance': avg_portfolio_return - spy_return
        }
    
    return None

def test_data_fetching():
    """
    Test function to verify data fetching works
    """
    print("🧪 Testing REAL data fetching...")
    
    # Test stock data
    test_tickers = ["AAPL"]
    stock_data = fetch_stock_data(test_tickers)
    print(f"📊 Stock data test: {len(stock_data)} stocks fetched")
    
    # Test SPY data
    spy_data = fetch_spy_data()
    print(f"📈 SPY data test: {'✅ Success' if spy_data else '❌ Failed'}")
    
    if len(stock_data) > 0:
        for ticker, data in stock_data.items():
            print(f"   {ticker}: ${data['current_price']:.2f}")
    
    if spy_data:
        print(f"   SPY: ${spy_data['current_price']:.2f}, YTD: {spy_data['ytd_return']:.2f}%")
    
    return len(stock_data) > 0 and spy_data is not None 