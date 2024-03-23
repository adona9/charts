import numpy as np
import plotly.graph_objects as go
import pandas as pd
import os
from plotly.subplots import make_subplots


ticker = 'SVOL'

prices = pd.read_csv(f'/home/alessandro/Downloads/{ticker}.csv')
prices.set_index('Date', inplace=True)


dividends_file = f'./data/{ticker}_dividends.csv'
dividends = pd.read_csv(dividends_file) if os.path.exists(dividends_file) else pd.DataFrame(columns=['Date', 'Dividend'])
dividends.set_index('Date', inplace=True)

merged = pd.merge(prices, dividends, left_index=True, right_index=True, how='outer')

df = merged.reset_index()
dividends = dividends.reset_index()


fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03)


fig.add_trace(
    go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name=ticker),
    row=1, col=1)

sma_20 = df['Close'].rolling(window=20).mean()
fig.add_trace(
    go.Scatter(x=df['Date'], y=sma_20, mode='lines', name='20-day SMA', line=dict(color='orange'), opacity=.2),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=df['Date'], y=df['Open'] + df['Dividend'], name='Open+Dividend', mode='markers', marker=dict(color='black')),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=dividends['Date'], y=dividends['Dividend'], name='Dividend', opacity=.5, text=dividends['Dividend'], textposition='inside'),
    row=3, col=1)

fig.add_trace(
    go.Bar(x=df['Date'], y=df['Volume'], name='Volume', yaxis='y2',opacity=.5),
    row=2, col=1)

fig.update_xaxes(showticklabels=False, row=3, col=1)

fig.update_layout(
    title=ticker,
    xaxis_rangeslider_visible=False,
    yaxis_title=f'{ticker} Price',
    shapes=[dict(
        x0=dividend_date, x1=dividend_date, y0=0.33, y1=.66, xref='x', yref='paper',
        line_width=.2) for dividend_date in dividends['Date']],
    annotations=[dict(
        x=row['Date'], y=0.02, xref='x', yref='paper',
        showarrow=False, xanchor='center', text=row['Date'])
        for index, row in dividends.iterrows()]
)
fig.show()