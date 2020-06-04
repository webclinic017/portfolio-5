import logging
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from service.technical_analysis import get_analysis



def update_graph(ticker):

    logging.info(f"{ticker}")

    # Get Technical analysis data in df
    df, low_period, high_period, mean_period = get_analysis(ticker)

    logging.info("end date is %s", df.iloc[-1].at['datetime'])
    logging.info("start date is %s", df.iloc[-21].at['datetime'])

    fig = make_subplots(
        rows=4,
        cols=1,
        row_heights=[0.5, 0.1, 0.2, 0.2],
        shared_xaxes=True,
        vertical_spacing=0.05,
    )

    # Stock price Candelstick -  Chart 1
    fig.add_trace(
        go.Candlestick(
            x=df["datetime"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Candle",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["short_mavg"],
            name="10 day simple average",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["long_mavg_1"],
            name="20 day exp average",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["long_mavg_2"],
            name="30 day exp average",
        ),
        row=1,
        col=1,
    )


     # shape defined programatically
    fig.add_shape(line_color='blue',
            type="line",
            xref='x1',
            yref="y1",
            x0=df.iloc[-21].at['datetime'],
            y0=low_period,
            x1=df.iloc[-1].at['datetime'],
            y1=low_period,
           

        )
    
    fig.add_shape(line_color='blue',
            type="line",
            xref='x1',
            yref="y1",
            x0=df.iloc[-21].at['datetime'],
            y0=high_period,
            x1=df.iloc[-1].at['datetime'],
            y1=high_period,
        )

    fig.add_annotation(
            y=high_period + 2,
            x=df.iloc[-21].at['datetime'],
            text="30 Day High : " + str(high_period),
            showarrow=False,
            xref='x1',
            yref="y1",
        )

    fig.add_annotation(
            y=low_period + 2,
            x=df.iloc[-21].at['datetime'],
            text="30 Day Low : " + str(low_period),
            showarrow=False,
            xref='x1',
            yref="y1",
        )

    fig.add_trace(
        go.Bar(
            x=df["datetime"],
            y=df["volume"],
            name="Volume",
        ),
        row=2,
        col=1,
    )

    # RSI scatter - Chart 2
    fig.add_trace(go.Scatter(x=df["datetime"], y=df["rsi"], name="rsi"), row=3, col=1)
    
    # shape defined programatically
    fig.add_shape(line_color='green',
            type="line",
            xref='paper',
            x0=0,
            y0=30.0,
            x1=1,
            y1=30.0,
            yref="y3",

        )
    
    fig.add_shape(line_color='red',
            type="line",
            xref='paper',
            x0=0,
            y0=70.0,
            x1=1,
            y1=70.0,
            yref="y3",

        )

    fig.add_annotation(
            y=35,
            text="OverSold",
            showarrow=False,
            xref='paper',
            yref="y3",
        )

    fig.add_annotation(
            y=75,
            text="OverBought",
            showarrow=False,
            xref='paper',
            yref="y3",
    )
    
    # MACD  - Chart 3
    fig.add_trace(go.Scatter(x=df["datetime"], y=df["macd"], name="macd", line=dict(color='royalblue'),), row=4, col=1)
    fig.add_trace(go.Scatter(x=df["datetime"], y=df["macdsignal"], name="signal", line=dict(color='red')), row=4, col=1)
    fig.add_trace(go.Bar(x=df["datetime"], y=df["macdhist"], name="macdhistogram"), row=4, col=1)


    fig.add_shape(line_color='blue',
            type="line",
            xref='paper',
            x0=0,
            y0=0,
            x1=1,
            y1=0,
            yref="y4",

        )

    # Update yaxis properties to show chart titles
    fig.update_yaxes(title_text="STOCK PRICE", showgrid=False, row=1, col=1)
    fig.update_yaxes(title_text="VOLUME", showgrid=False, row=2, col=1)
    fig.update_yaxes(title_text="RSI", showgrid=False, row=3, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=4, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(
        height=800, title=ticker, template="plotly_white", showlegend=False,
    )

    info_text = f" Average Close Price for 30 Day Period : {mean_period} "

    return fig, info_text
