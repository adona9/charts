import plotly.graph_objects as go
from plotly.subplots import make_subplots
import price_loader as pl

ticker = 'AMDY'
u_ticker = 'AMD'

price = pl.get_price(ticker)
u_price = pl.get_price(u_ticker)

fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[70, 10, 10, 10])

fig.add_trace(
    go.Candlestick(x=price.index, open=price['Open'], high=price['High'], low=price['Low'], close=price['Close'], name='Price', yaxis='y1'),
    row=1, col=1)

sma_20 = price['Close'].rolling(window=20).mean()
fig.add_trace(
    go.Scatter(x=price.index, y=sma_20, mode='lines', name='20-day SMA', line=dict(color='orange'), opacity=.2),
    row=1, col=1)

fig.add_trace(
    go.Scatter(x=u_price.index, y=price['Close'].rolling(window=20).corr(u_price['Close']), mode='lines', name=f'20-day corr {u_ticker}', line=dict(color='lightgrey'), opacity=.75, yaxis='y2'),
    row=4, col=1)

fig.add_trace(
    go.Scatter(name='Open+Dividend $',
               x=price.index, y=price['Open'] + price['Dividend'],
               mode='markers+text',
               textposition='top center',
               text=price['Dividend'],
               marker=dict(size=8, color='white', line=dict(width=.5, color='black'))),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=price.index, y=price['Volume'], name='Volume', yaxis='y2', opacity=.5),
    row=2, col=1)

price['Yield'] = 100 * price['Dividend'] / (price['Open'] + price['Dividend'])
dividends =  price.dropna(subset=['Dividend'])
fig.add_trace(
    go.Bar(name='Yield %',
           x=dividends.index, y=dividends["Yield"],
           opacity=.5,
           text=round(dividends["Yield"], 3),
           textposition='inside',
           textfont=dict(size=18)
           ),
    row=3, col=1)

fig.update_xaxes(row=1, col=1, dtick='M1')
fig.update_xaxes(row=2, col=1, dtick='M1')
fig.update_xaxes(row=3, col=1, dtick='M1')
fig.update_xaxes(row=4, col=1, dtick='D1',  ticklabelstep=7, ticks='outside')

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
