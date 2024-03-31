import plotly.graph_objects as go
from plotly.subplots import make_subplots
import price_loader as pl

ticker = 'FBY'

prices = pl.get_price(ticker)
df = prices.reset_index()

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[70, 15, 15])

fig.add_trace(
    go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'),
    row=1, col=1)

sma_20 = df['Close'].rolling(window=20).mean()
fig.add_trace(
    go.Scatter(x=df['Date'], y=sma_20, mode='lines', name='20-day SMA', line=dict(color='orange'), opacity=.2),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(name='Open+Dividend $',
               x=df['Date'], y=df['Open'] + df['Dividend'],
               mode='markers+text',
               textposition='top center',
               text=df['Dividend'],
               marker=dict(size=8, color='white', line=dict(width=.5, color='black'))),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=df['Date'], y=df['Volume'], name='Volume', yaxis='y2', opacity=.5),
    row=2, col=1)

df['Yield'] = 100 * df['Dividend'] / (df["Open"] + df["Dividend"])
dividends =  df.dropna(subset=['Dividend'])
fig.add_trace(
    go.Bar(name='Yield %',
           x=dividends['Date'], y=dividends["Yield"],
           opacity=.5,
           text=round(dividends["Yield"], 3),
           textposition='inside',
           textfont=dict(size=18)
           ),
    row=3, col=1)


fig.update_xaxes(row=3, col=1, dtick='D1',  ticklabelstep=7, ticks='outside')

fig.update_layout(
    title=ticker,
    xaxis_rangeslider_visible=False,
    yaxis_title=f'{ticker} Price',
    # shapes=[dict(
    #     x0=dividend_date, x1=dividend_date, y0=0.33, y1=.66, xref='x', yref='paper',
    #     line_width=.2) for dividend_date in dividends['Date']],
    # annotations=[dict(
    #     x=row['Date'], y=0.02, xref='x', yref='paper',
    #     showarrow=False, xanchor='center', text=row['Date'])
    #     for index, row in dividends.iterrows()]
)
fig.show()
