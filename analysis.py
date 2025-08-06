from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def analyze_sentiment(headlines):
    """
    Analyze sentiment of news headlines using VADER
    """
    analyzer = SentimentIntensityAnalyzer()
    
    if not headlines:
        return {
            'compound_score': 0,
            'sentiment': 'Neutral',
            'positive_score': 0,
            'negative_score': 0,
            'neutral_score': 0
        }
    
    compound_scores = []
    positive_scores = []
    negative_scores = []
    neutral_scores = []
    
    for headline in headlines:
        scores = analyzer.polarity_scores(headline['title'])
        compound_scores.append(scores['compound'])
        positive_scores.append(scores['pos'])
        negative_scores.append(scores['neg'])
        neutral_scores.append(scores['neu'])
    
    avg_compound = np.mean(compound_scores)
    avg_positive = np.mean(positive_scores)
    avg_negative = np.mean(negative_scores)
    avg_neutral = np.mean(neutral_scores)
    
    # Determine sentiment category with more granularity
    if avg_compound > 0.2:
        sentiment = 'Very Positive'
    elif avg_compound > 0.05:
        sentiment = 'Positive'
    elif avg_compound < -0.2:
        sentiment = 'Very Negative'
    elif avg_compound < -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return {
        'compound_score': avg_compound,
        'sentiment': sentiment,
        'positive_score': avg_positive,
        'negative_score': avg_negative,
        'neutral_score': avg_neutral
    }

def calculate_momentum_signal(ma50, ma200, current_price, rsi, volatility):
    """
    Calculate comprehensive momentum signal
    """
    if pd.isna(ma50) or pd.isna(ma200):
        return 'Neutral'
    
    # Multiple momentum indicators
    ma_signal = 'Bullish' if ma50 > ma200 else 'Bearish'
    price_vs_ma50 = 'Above' if current_price > ma50 else 'Below'
    rsi_signal = 'Overbought' if rsi > 70 else ('Oversold' if rsi < 30 else 'Neutral')
    
    # Combined momentum score
    momentum_score = 0
    
    # MA signal (40% weight)
    if ma_signal == 'Bullish':
        momentum_score += 0.4
    elif ma_signal == 'Bearish':
        momentum_score -= 0.4
    
    # Price vs MA50 (30% weight)
    if price_vs_ma50 == 'Above':
        momentum_score += 0.3
    else:
        momentum_score -= 0.3
    
    # RSI signal (30% weight)
    if rsi_signal == 'Oversold':
        momentum_score += 0.3
    elif rsi_signal == 'Overbought':
        momentum_score -= 0.3
    
    # Determine final momentum
    if momentum_score > 0.3:
        return 'Strong Bullish'
    elif momentum_score > 0.1:
        return 'Bullish'
    elif momentum_score < -0.3:
        return 'Strong Bearish'
    elif momentum_score < -0.1:
        return 'Bearish'
    else:
        return 'Neutral'

def calculate_technical_score(stock_data):
    """
    Calculate comprehensive technical analysis score
    """
    score = 0
    signals = []
    
    # RSI Analysis
    rsi = stock_data.get('rsi', 50)
    if rsi < 30:
        score += 1
        signals.append('RSI Oversold')
    elif rsi > 70:
        score -= 1
        signals.append('RSI Overbought')
    else:
        score += 0.5
        signals.append('RSI Neutral')
    
    # Moving Average Analysis
    current_price = stock_data['current_price']
    ma20 = stock_data.get('ma20', current_price)
    ma50 = stock_data.get('ma50', current_price)
    ma200 = stock_data.get('ma200', current_price)
    
    if current_price > ma20 > ma50 > ma200:
        score += 2
        signals.append('Strong Uptrend')
    elif current_price > ma20 and ma20 > ma50:
        score += 1
        signals.append('Uptrend')
    elif current_price < ma20 < ma50 < ma200:
        score -= 2
        signals.append('Strong Downtrend')
    elif current_price < ma20 and ma20 < ma50:
        score -= 1
        signals.append('Downtrend')
    else:
        signals.append('Mixed Signals')
    
    # Volume Analysis
    avg_volume = stock_data.get('avg_volume', 0)
    current_volume = stock_data.get('volume', 0)
    if current_volume > avg_volume * 1.5:
        score += 0.5
        signals.append('High Volume')
    elif current_volume < avg_volume * 0.5:
        score -= 0.5
        signals.append('Low Volume')
    
    # Volatility Analysis
    volatility = stock_data.get('volatility', 0)
    if volatility > 0.05:  # High volatility
        score += 0.3
        signals.append('High Volatility')
    
    return {
        'score': score,
        'signals': signals,
        'rsi': rsi,
        'trend': 'Uptrend' if score > 0 else ('Downtrend' if score < 0 else 'Sideways')
    }

def generate_recommendation(momentum, sentiment, analyst_score, technical_score, price_changes):
    """
    Generate comprehensive investment recommendation
    """
    # Convert signals to numerical scores
    momentum_scores = {
        'Strong Bullish': 2, 'Bullish': 1, 'Neutral': 0, 
        'Bearish': -1, 'Strong Bearish': -2
    }
    momentum_score = momentum_scores.get(momentum, 0)
    
    sentiment_scores = {
        'Very Positive': 2, 'Positive': 1, 'Neutral': 0,
        'Negative': -1, 'Very Negative': -2
    }
    sentiment_score = sentiment_scores.get(sentiment, 0)
    
    # Technical score is already numerical
    technical_score_val = technical_score.get('score', 0)
    
    # Price change analysis
    price_score = 0
    if price_changes.get('price_change_1d', 0) > 2:
        price_score += 0.5
    elif price_changes.get('price_change_1d', 0) < -2:
        price_score -= 0.5
    
    if price_changes.get('price_change_5d', 0) > 5:
        price_score += 0.3
    elif price_changes.get('price_change_5d', 0) < -5:
        price_score -= 0.3
    
    # Calculate weighted average
    total_score = (
        momentum_score * 0.25 + 
        sentiment_score * 0.2 + 
        analyst_score * 0.2 + 
        technical_score_val * 0.25 + 
        price_score * 0.1
    )
    
    # Generate detailed recommendation
    if total_score > 1.5:
        return {
            'action': 'Strong Buy',
            'confidence': 'High',
            'reasoning': 'Multiple positive signals across all indicators',
            'score': total_score
        }
    elif total_score > 0.5:
        return {
            'action': 'Buy',
            'confidence': 'Medium',
            'reasoning': 'Generally positive signals with some mixed indicators',
            'score': total_score
        }
    elif total_score > -0.5:
        return {
            'action': 'Hold',
            'confidence': 'Medium',
            'reasoning': 'Mixed signals, wait for clearer direction',
            'score': total_score
        }
    elif total_score > -1.5:
        return {
            'action': 'Consider Selling',
            'confidence': 'Medium',
            'reasoning': 'Generally negative signals with some mixed indicators',
            'score': total_score
        }
    else:
        return {
            'action': 'Strong Sell',
            'confidence': 'High',
            'reasoning': 'Multiple negative signals across all indicators',
            'score': total_score
        }

def analyze_portfolio(stock_data, news_data, analyst_data):
    """
    Comprehensive portfolio analysis
    """
    analysis_results = {}
    
    for ticker in stock_data.keys():
        # Get data for this ticker
        stock_info = stock_data[ticker]
        headlines = news_data.get(ticker, [])
        analyst_info = analyst_data.get(ticker, {'consensus': 'Hold', 'score': 0})
        
        # Calculate comprehensive momentum
        momentum = calculate_momentum_signal(
            stock_info['ma50'], 
            stock_info['ma200'], 
            stock_info['current_price'],
            stock_info.get('rsi', 50),
            stock_info.get('volatility', 0)
        )
        
        # Analyze sentiment
        sentiment_analysis = analyze_sentiment(headlines)
        
        # Calculate technical score
        technical_analysis = calculate_technical_score(stock_info)
        
        # Get price changes
        price_changes = {
            'price_change_1d': stock_info.get('price_change_1d', 0),
            'price_change_5d': stock_info.get('price_change_5d', 0),
            'price_change_1m': stock_info.get('price_change_1m', 0),
            'price_change_3m': stock_info.get('price_change_3m', 0),
            'price_change_6m': stock_info.get('price_change_6m', 0),
            'price_change_1y': stock_info.get('price_change_1y', 0)
        }
        
        # Generate comprehensive recommendation
        recommendation = generate_recommendation(
            momentum, 
            sentiment_analysis['sentiment'], 
            analyst_info['score'],
            technical_analysis,
            price_changes
        )
        
        analysis_results[ticker] = {
            'current_price': stock_info['current_price'],
            'ma50': stock_info['ma50'],
            'ma200': stock_info['ma200'],
            'ma20': stock_info.get('ma20', stock_info['current_price']),
            'momentum': momentum,
            'sentiment_score': sentiment_analysis['compound_score'],
            'sentiment': sentiment_analysis['sentiment'],
            'analyst_consensus': analyst_info['consensus'],
            'analyst_score': analyst_info['score'],
            'recommendation': recommendation,
            'technical_analysis': technical_analysis,
            'price_changes': price_changes,
            'headlines': headlines,
            'company_name': stock_info['company_name'],
            'rsi': stock_info.get('rsi', 50),
            'volatility': stock_info.get('volatility', 0),
            'volume': stock_info.get('volume', 0),
            'avg_volume': stock_info.get('avg_volume', 0)
        }
    
    return analysis_results

def calculate_portfolio_metrics(analysis_results):
    """
    Calculate portfolio-level metrics
    """
    if not analysis_results:
        return {}
    
    # Count recommendations
    recommendations = [result['recommendation']['action'] for result in analysis_results.values()]
    strong_buy_count = recommendations.count('Strong Buy')
    buy_count = recommendations.count('Buy')
    hold_count = recommendations.count('Hold')
    sell_count = recommendations.count('Consider Selling')
    strong_sell_count = recommendations.count('Strong Sell')
    
    # Average sentiment score
    sentiment_scores = [result['sentiment_score'] for result in analysis_results.values()]
    avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
    
    # Momentum distribution
    momentum_signals = [result['momentum'] for result in analysis_results.values()]
    strong_bullish_count = momentum_signals.count('Strong Bullish')
    bullish_count = momentum_signals.count('Bullish')
    neutral_count = momentum_signals.count('Neutral')
    bearish_count = momentum_signals.count('Bearish')
    strong_bearish_count = momentum_signals.count('Strong Bearish')
    
    # Technical analysis distribution
    technical_trends = [result['technical_analysis']['trend'] for result in analysis_results.values()]
    uptrend_count = technical_trends.count('Uptrend')
    downtrend_count = technical_trends.count('Downtrend')
    sideways_count = technical_trends.count('Sideways')
    
    return {
        'total_stocks': len(analysis_results),
        'strong_buy_recommendations': strong_buy_count,
        'buy_recommendations': buy_count,
        'hold_recommendations': hold_count,
        'sell_recommendations': sell_count,
        'strong_sell_recommendations': strong_sell_count,
        'avg_sentiment': avg_sentiment,
        'strong_bullish_momentum': strong_bullish_count,
        'bullish_momentum': bullish_count,
        'neutral_momentum': neutral_count,
        'bearish_momentum': bearish_count,
        'strong_bearish_momentum': strong_bearish_count,
        'uptrend_count': uptrend_count,
        'downtrend_count': downtrend_count,
        'sideways_count': sideways_count
    }

def format_currency(value):
    """
    Format currency values
    """
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"

def format_percentage(value):
    """
    Format percentage values
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}%"

def get_sentiment_color(sentiment):
    """
    Get color for sentiment display
    """
    if sentiment in ['Very Positive', 'Positive']:
        return 'green'
    elif sentiment in ['Very Negative', 'Negative']:
        return 'red'
    else:
        return 'orange'

def get_momentum_color(momentum):
    """
    Get color for momentum display
    """
    if momentum in ['Strong Bullish', 'Bullish']:
        return 'green'
    elif momentum in ['Strong Bearish', 'Bearish']:
        return 'red'
    else:
        return 'orange'

def get_recommendation_color(recommendation):
    """
    Get color for recommendation display
    """
    if recommendation in ['Strong Buy', 'Buy']:
        return 'green'
    elif recommendation in ['Strong Sell', 'Consider Selling']:
        return 'red'
    else:
        return 'blue' 