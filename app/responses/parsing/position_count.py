from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.plotting import figure
from munch import munchify

from app.models import Card

def get_card_x_responses(study, responses):
    
    columns = [str(i) for i in range(study.number_of_columns)]
    cards = []
    cards_x_data = {}
    for card in study.card_set_x.cards:
        cards.append(card.name)
        cards_x_data[card.name] = [0 for x in range(study.number_of_columns)]

    for response in responses:
        cards_x = munchify(response.cards_x)
        for col, cards2 in cards_x.items():
            for card in cards2:
                col2 = col.split('_')[1]
                cards_x_data[card.name][int(col2)] += 1
    x = [(column, card) for column in columns for card in cards]
    lists = list(cards_x_data.values())
    counts = sum(zip(*lists),()) # like an hstack                  
    
    title = "Count of each card in card set {} in each column".format(study.card_set_x.name)
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), height=400, sizing_mode="stretch_width", title=title, toolbar_location=None, tools="")         
    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.yaxis.ticker = SingleIntervalTicker(interval=1)
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    
    script, div = components(p)
    return script, div

def get_card_y_responses(study, responses):
    
    rows = [str(i) for i in range(study.number_of_rows)]
    cards = []
    cards_y_data = {}
    
    for card in study.card_set_y.cards:
        cards.append(card.name)
        cards_y_data[card.name] = [0 for x in range(study.number_of_rows)]
    
    for response in responses:
        cards_y = munchify(response.cards_y)
        for row, cards2 in cards_y.items():
            for card in cards2:
                row2 = row.split('_')[1]
                cards_y_data[card.name][int(row2)] += 1

    x = [(row, card) for row in rows for card in cards]
    lists = list(cards_y_data.values())
    counts = sum(zip(*lists),()) # like an hstack                  
    title = "Count of each card in card set {} in each row".format(study.card_set_y.name)
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), height=400, sizing_mode="stretch_width", title=title,
                toolbar_location=None, tools="")         
    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.yaxis.ticker = SingleIntervalTicker(interval=1) 
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    
    script, div = components(p)
    
    return script, div