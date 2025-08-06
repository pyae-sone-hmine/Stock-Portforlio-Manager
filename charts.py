import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_stock_chart(ticker, stock_data, timeframe='1y'):
    """
    Create interactive stock chart with multiple timeframes
    """
    if not stock_data or 'historical_data' not in stock_data:
        return None
    
    hist = stock_data['historical_data']
    
    # Create subplots for price and volume
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,  # Reduced spacing
        subplot_titles=(f'{ticker} Stock Price', 'Volume', 'RSI'),
        row_width=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart with clean colors
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='Price',
            increasing_line_color='#10b981',  # Clean green
            decreasing_line_color='#ef4444',  # Clean red
            increasing_fillcolor='#10b981',
            decreasing_fillcolor='#ef4444'
        ),
        row=1, col=1
    )
    
    # Moving averages with clean colors
    if 'MA20' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['MA20'],
                mode='lines',
                name='MA20',
                line=dict(color='#f59e0b', width=1.5)  # Clean orange
            ),
            row=1, col=1
        )
    
    if 'MA50' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['MA50'],
                mode='lines',
                name='MA50',
                line=dict(color='#3b82f6', width=1.5)  # Clean blue
            ),
            row=1, col=1
        )
    
    if 'MA200' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['MA200'],
                mode='lines',
                name='MA200',
                line=dict(color='#8b5cf6', width=1.5)  # Clean purple
            ),
            row=1, col=1
        )
    
    # Volume bars with clean colors
    colors = ['#10b981' if close >= open else '#ef4444' 
              for close, open in zip(hist['Close'], hist['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # RSI with clean colors
    if 'RSI' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='#06b6d4', width=1.5)  # Clean cyan
            ),
            row=3, col=1
        )
        
        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#10b981", row=3, col=1)
    
    # Update layout with dark theme
    fig.update_layout(
        title=f'{ticker} Stock Analysis - {timeframe.upper()}',
        xaxis_rangeslider_visible=False,
        height=600,  # Reduced height
        showlegend=True,
        template='plotly_dark',
        margin=dict(l=50, r=50, t=50, b=50),  # Reduced margins
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')  # White text for dark theme
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=3, col=1, gridcolor='#333')
    fig.update_yaxes(title_text="Price ($)", row=1, col=1, gridcolor='#333')
    fig.update_yaxes(title_text="Volume", row=2, col=1, gridcolor='#333')
    fig.update_yaxes(title_text="RSI", row=3, col=1, gridcolor='#333')
    
    return fig

def create_price_performance_chart(stock_data, spy_data=None):
    """
    Create price performance comparison chart
    """
    if not stock_data:
        return None
    
    fig = go.Figure()
    
    # Define clean colors for stocks
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316', '#84cc16', '#ec4899', '#6366f1']
    
    # Add each stock's performance
    for i, (ticker, data) in enumerate(stock_data.items()):
        if 'historical_data' in data and data['historical_data'] is not None:
            hist = data['historical_data']
            
            # Calculate cumulative returns
            returns = hist['Close'].pct_change().fillna(0)
            cumulative_returns = (1 + returns).cumprod() - 1
            
            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=cumulative_returns * 100,
                    mode='lines',
                    name=ticker,
                    line=dict(width=2, color=colors[i % len(colors)])
                )
            )
    
    # Add SPY if available
    if spy_data and 'historical_data' in spy_data and spy_data['historical_data'] is not None:
        spy_hist = spy_data['historical_data']
        spy_returns = spy_hist['Close'].pct_change().fillna(0)
        spy_cumulative = (1 + spy_returns).cumprod() - 1
        
        fig.add_trace(
            go.Scatter(
                x=spy_hist.index,
                y=spy_cumulative * 100,
                mode='lines',
                name='SPY (Benchmark)',
                line=dict(color='white', width=2, dash='dash')
            )
        )
    
    fig.update_layout(
        title='Portfolio Performance vs Benchmark',
        xaxis_title='Date',
        yaxis_title='Cumulative Return (%)',
        template='plotly_dark',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def create_technical_indicators_chart(ticker, stock_data):
    """
    Create technical indicators chart
    """
    if not stock_data or 'historical_data' not in stock_data:
        return None
    
    hist = stock_data['historical_data']
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,  # Reduced spacing
        subplot_titles=(f'{ticker} Technical Indicators', 'Volume Analysis'),
        row_width=[0.7, 0.3]
    )
    
    # Price and moving averages with clean colors
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            name='Price',
            line=dict(color='#374151', width=2)  # Clean dark gray
        ),
        row=1, col=1
    )
    
    if 'MA20' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['MA20'],
                mode='lines',
                name='MA20',
                line=dict(color='#f59e0b', width=1.5)  # Clean orange
            ),
            row=1, col=1
        )
    
    if 'MA50' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['MA50'],
                mode='lines',
                name='MA50',
                line=dict(color='#3b82f6', width=1.5)  # Clean blue
            ),
            row=1, col=1
        )
    
    # RSI with clean colors
    if 'RSI' in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='#06b6d4', width=1.5),  # Clean cyan
                yaxis='y2'
            ),
            row=1, col=1
        )
        
        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#10b981", row=1, col=1)
    
    # Volume with clean colors
    colors = ['#10b981' if close >= open else '#ef4444' 
              for close, open in zip(hist['Close'], hist['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Update layout with clean theme
    fig.update_layout(
        title=f'{ticker} Technical Analysis',
        xaxis_rangeslider_visible=False,
        height=500,  # Reduced height
        showlegend=True,
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50),  # Reduced margins
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#374151'),  # Clean dark gray text
        yaxis2=dict(
            title="RSI",
            overlaying="y",
            side="right",
            range=[0, 100]
        )
    )
    
    return fig

def create_portfolio_summary_chart(analysis_results):
    """
    Create portfolio summary charts
    """
    if not analysis_results:
        return None
    
    # Prepare data for charts
    tickers = list(analysis_results.keys())
    prices = [data['current_price'] for data in analysis_results.values()]
    price_changes_1d = [data['price_changes']['price_change_1d'] for data in analysis_results.values()]
    price_changes_1m = [data['price_changes']['price_change_1m'] for data in analysis_results.values()]
    rsi_values = [data['rsi'] for data in analysis_results.values()]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Current Prices', '1-Day Change (%)', '1-Month Change (%)', 'RSI Values'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Current prices with clean colors
    fig.add_trace(
        go.Bar(x=tickers, y=prices, name='Current Price', marker_color='#3b82f6'),
        row=1, col=1
    )
    
    # 1-day change with clean colors
    colors_1d = ['#10b981' if x > 0 else '#ef4444' for x in price_changes_1d]
    fig.add_trace(
        go.Bar(x=tickers, y=price_changes_1d, name='1-Day Change', marker_color=colors_1d),
        row=1, col=2
    )
    
    # 1-month change with clean colors
    colors_1m = ['#10b981' if x > 0 else '#ef4444' for x in price_changes_1m]
    fig.add_trace(
        go.Bar(x=tickers, y=price_changes_1m, name='1-Month Change', marker_color=colors_1m),
        row=2, col=1
    )
    
    # RSI values with clean colors
    colors_rsi = ['#ef4444' if x > 70 else ('#10b981' if x < 30 else '#f59e0b') for x in rsi_values]
    fig.add_trace(
        go.Bar(x=tickers, y=rsi_values, name='RSI', marker_color=colors_rsi),
        row=2, col=2
    )
    
    fig.update_layout(
        title='Portfolio Summary',
        height=600,
        showlegend=False,
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def create_sentiment_analysis_chart(analysis_results):
    """
    Create sentiment analysis visualization
    """
    if not analysis_results:
        return None
    
    # Prepare sentiment data
    tickers = list(analysis_results.keys())
    sentiment_scores = [data['sentiment_score'] for data in analysis_results.values()]
    sentiments = [data['sentiment'] for data in analysis_results.values()]
    
    # Create color mapping with clean colors
    color_map = {
        'Very Positive': '#10b981',
        'Positive': '#34d399',
        'Neutral': '#6b7280',
        'Negative': '#f87171',
        'Very Negative': '#ef4444'
    }
    
    colors = [color_map.get(sentiment, '#6b7280') for sentiment in sentiments]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=tickers,
            y=sentiment_scores,
            marker_color=colors,
            text=sentiments,
            textposition='auto'
        )
    )
    
    fig.update_layout(
        title='Sentiment Analysis by Stock',
        xaxis_title='Stock Ticker',
        yaxis_title='Sentiment Score',
        template='plotly_dark',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def create_recommendation_chart(analysis_results):
    """
    Create recommendation distribution chart
    """
    if not analysis_results:
        return None
    
    # Count recommendations
    recommendations = [data['recommendation']['action'] for data in analysis_results.values()]
    rec_counts = pd.Series(recommendations).value_counts()
    
    # Color mapping with clean colors
    color_map = {
        'Strong Buy': '#10b981',
        'Buy': '#34d399',
        'Hold': '#3b82f6',
        'Consider Selling': '#f59e0b',
        'Strong Sell': '#ef4444'
    }
    
    colors = [color_map.get(rec, '#6b7280') for rec in rec_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=rec_counts.index,
            values=rec_counts.values,
            marker_colors=colors
        )
    ])
    
    fig.update_layout(
        title='Recommendation Distribution',
        template='plotly_dark',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig 