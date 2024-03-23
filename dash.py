from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd


app = dash.Dash(__name__)

app.layout = html.Div([
    dash.html.H4('OARK candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dash.dcc.Graph(id="graph"),
])


@app.callback(
    dash.Output("graph", "figure"),
    dash.Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    df = pd.read_csv('/home/alessandro/Downloads/OARK.csv')
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)