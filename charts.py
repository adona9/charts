import plotly.graph_objects as go
import pandas as pd
import os

ticker = 'OARK'

df = pd.read_csv(f'/home/alessandro/Downloads/{ticker}.csv')

dividends_file = f'./data/{ticker}_dividends.csv'
dividends = pd.read_csv(dividends_file) if os.path.exists(dividends_file) else pd.DataFrame(columns=['Date', 'Amount'])

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'])])

fig.update_layout(
    title=ticker,
    yaxis_title=f'{ticker} Price',
    xaxis_rangeslider_visible=False,
    shapes=[dict(
        x0=dividend_date, x1=dividend_date, y0=0, y1=1, xref='x', yref='paper',
        line_width=.5) for dividend_date in dividends['Date']],
    annotations=[dict(
        x=row['Date'], y=0.95, xref='x', yref='paper',
        showarrow=False, xanchor='left', text=row['Date'] + ' ' + str(row['Amount']))
        for index, row in dividends.iterrows()]
)
fig.show()
