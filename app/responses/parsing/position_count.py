from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models.tickers import SingleIntervalTicker
from app.models import Card

def get_card_x_responses(study, responses):
    
    columns = [str(i) for i in range(study.number_of_columns)]
    cards = []
    cards_x_data = {}
    for card in study.card_sets[0].cards:
        cards.append(card.name)
        cards_x_data[card.name] = [0 for x in range(study.number_of_columns)]

    for response in responses:
        for column, card_ids in response.cards_x.items():
            for card_id in card_ids:
                card = Card.query.filter_by(id=card_id).first()
                card_name = cards_x_data[card.name]
                card_name[int(column)] += 1

    x = [(column, card) for column in columns for card in cards]
    lists = list(cards_x_data.values())
    counts = sum(zip(*lists),()) # like an hstack                  
    
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), plot_height=250, title="Card", toolbar_location=None, tools="")         
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
    for card in study.card_sets[1].cards:
        cards.append(card.name)
        cards_y_data[card.name] = [0 for x in range(study.number_of_rows)]

    for response in responses:
        for row, card_ids in response.cards_y.items():
            for card_id in card_ids:
                card = Card.query.filter_by(id=card_id).first()
                card_name = cards_y_data[card.name]
                card_name[int(row)] += 1
    test  =[2,4,5,2]
    x = [(row, card) for row in rows for card in cards]
    lists = list(cards_y_data.values())
    counts = sum(zip(*lists),()) # like an hstack                  
    
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), plot_height=250, title="Card", toolbar_location=None, tools="")         
    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.yaxis.ticker = SingleIntervalTicker(interval=1) 
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    
    
    script, div = components(p)
    
    return script, div