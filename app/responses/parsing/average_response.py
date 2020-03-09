from statistics import mean
from app.models import Card


def average_response(study, responses):
    cards_x = average_response_cards_x(study, responses)
    cards_y = average_response_cards_y(study, responses)
    data_values = average_response_data_values(study, responses)
    average_response = {'cards_x':cards_x, 'cards_y':cards_y, 'data_values':data_values}
    return average_response 

def average_response_data_values(study, responses):
    average_data_values = {}
    data_values = {}
    for response in responses:
        for col_row, values in response.data_values.items():
            if col_row not in data_values:
                data_values[col_row] = []
            vals = []
            for value in values:
                if value != '':
                    vals.append(int(value))
                else:
                    vals.append(0)
            data_values[col_row].append(vals)
    
    for col_row, data_value in data_values.items():
        if col_row not in average_data_values:
            average_data_values[col_row] = []
        average_data_values[col_row] = list(map(mean, zip(*data_value)))
        # print(*map(mean, zip(*data_value)))
    
    
    return average_data_values    
                
def average_response_cards_x(study,responses):
    average_cards_x = {}
    cards_x = {}
    for col in range(study.number_of_columns):
        average_cards_x[str(col)] = []
    
    for response in responses:
        for col, card_ids in response.cards_x.items():
            for card_id in card_ids:
                card = Card.query.filter_by(id=card_id).first()
                if card is not None:
                    if card not in cards_x:
                        cards_x[card] = []
                    
                    cards_x[card].append(int(col))
    
    for card, cols in cards_x.items():
        col = mean(cols)
        average_cards_x[str(int(col))].append(card)
    
    return average_cards_x

def average_response_cards_y(study, responses):
    average_cards_y = {}
    cards_y = {}
    
    for row in range(study.number_of_rows):
        average_cards_y[str(row)] = []
    
    for response in responses:
        for row, card_ids in response.cards_y.items():
            for card_id in card_ids:
                card = Card.query.filter_by(id=card_id).first()
                if card is not None:
                    if card not in cards_y:
                        cards_y[card] = []
                    cards_y[card].append(int(row))
    
    for card, rows in cards_y.items():
        row = mean(rows)
        average_cards_y[str(int(row))].append(card)
    
    return average_cards_y