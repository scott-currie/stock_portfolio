import requests
import pandas as pd
import bokeh.plotting as bk
from bokeh.models import HoverTool, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool, Label
import numpy as np
from bokeh.embed import components


API_URL = 'https://api.iextrading.com/1.0/stock/{}/chart/5y'


def make_plot(data):
    # Make the API request and load json data into DataFrame
    symbol = 'amzn'
    res = requests.get(API_URL.format(symbol))
    data = res.json()
    df = pd.DataFrame(data)
    # Add a new column in the shape of the original data
    seqs = np.arange(df.shape[0])
    df['seqs'] = pd.Series(seqs)
    # Add a mid column that is midpoint between open and close
    df['mid'] = df.apply(lambda x: (x['open'] + x['close']) / 2, axis=1)
    # Add height column after checking if close is greater than open
    df['height'] = df.apply(lambda x: x['close'] - x['open']
                            if x['close'] != x['open'] else 0.01, axis=1)
    # some stuff to format plot
    inc = df.close > df.open  # Series where stocks closed higher than they opened
    dec = df.close < df.open  # Series in which stocks closed lower than they opened
    w = .3  # line width for plot
    # some stuff to format plot
    inc = df.close > df.open  # Series where stocks closed higher than they opened
    dec = df.close < df.open  # Series in which stocks closed lower than they opened
    w = .3  # line width for plot
    # Define sources for increasing and decreasing stocks
    sourceInc = bk.ColumnDataSource(df.loc[inc])
    sourceDec = bk.ColumnDataSource(df.loc[dec])
    # Define the Bokeh tools to include in the figure
    hover = HoverTool(
        tooltips=[
            ('Date', '@date'),
            ('Low', '@low'),
            ('High', '@high'),
            ('Open', '@open'),
            ('Close', '@close'),
            ('Percent', '@changePercent')
        ]
    )
    TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(),
             ZoomOutTool(), ResetTool()]
    # Define size and layout of figure
    p = bk.figure(plot_width=1200, plot_height=800, title='Amazon',
                  tools=TOOLS, toolbar_location='above')
    p.xaxis.major_label_orientation = np.pi/4
    p.grid.grid_line_alpha = w
    descriptor = Label(x=70,  y=70, text='Amazon Stock Price Over Time')
    p.add_layout(descriptor)
    # Create segments for price increases
    p.segment(df.seqs[inc], df.high[inc],
              df.seqs[inc], df.low[inc], color='green')
    # Create segments for price decreases
    p.segment(df.seqs[dec], df.high[dec],
              df.seqs[dec], df.low[dec], color='red')
    # Create rects for price increases
    p.rect(x='seqs', y='mid', width=w, height='height',
           fill_color='green', line_color='green', source=sourceInc)
    # Create rects for price decreases
    p.rect(x='seqs', y='mid', width=w, height='height',
           fill_color='red', line_color='red', source=sourceDec)
    script, div = components(p)
    return script, div
