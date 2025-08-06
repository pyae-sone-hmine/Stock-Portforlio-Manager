from data_fetch import fetch_stock_data

# Test multiple stocks
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
data = fetch_stock_data(tickers)

print(f"\n📊 Fetched {len(data)} stocks:")
for ticker in data.keys():
    price = data[ticker]['current_price']
    ma50 = data[ticker]['ma50']
    ma200 = data[ticker]['ma200']
    print(f"  {ticker}: ${price:.2f} | MA50: ${ma50:.2f} | MA200: ${ma200:.2f}") 