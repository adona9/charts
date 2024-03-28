import pandas as pd
import plotly.graph_objects as go
import price_loader as pl

ticker_symbol = 'HYGW'
#benchmark_tickers = ['^VIX','^SPX','UUP','^TNX','GLD','USO']
benchmark_tickers = ['SVOL', 'HYGH', 'YMAX', 'YMAG', 'AMDY', 'OARK']

sec = pl.get_price(ticker_symbol)
sec = sec.rename(columns={'Adj Close': f'{ticker_symbol} Price'})

correlations = {'ticker': [], 'correlation': []}
for bt in benchmark_tickers:
    benchmark = pl.get_price(ticker_symbol)
    benchmark = benchmark.rename(columns={'Adj Close': f'{bt} Price'})
    merged = pd.merge(sec, benchmark, left_index=True, right_index=True, how='outer')
    correlations['ticker'].append(bt)
    correlations['correlation'].append(merged[f'{ticker_symbol} Price'].corr(merged[f'{bt} Price']))
print(correlations)


fig = go.Figure(data=[go.Bar(x=correlations['ticker'], y=correlations['correlation'])])

fig.update_layout(
    title=f'Correlation of {ticker_symbol}',
    yaxis_title=f'Index')

fig.show()