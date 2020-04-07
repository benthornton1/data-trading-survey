from statistics import mean


from munch import munchify

from app.models import Card

def average_response(study):
    cards_x = average_response_cards_x(study)
    cards_y = average_response_cards_y(study)
    data_values = average_response_data_values(study)
    average_response = {'cards_x':cards_x, 'cards_y':cards_y, 'data_values':data_values}
    return average_response 

def average_response_data_values(study):
    average_data_values = {}
    data_values = {}
    all_data_values = {}
    for response in study.responses:
        response_data_values = munchify(response.data_values)
        for col_row, values in response_data_values.items():
            if col_row not in data_values:
                data_values[col_row] = []
            if col_row not in all_data_values:
                all_data_values[col_row] = values
            vals = []
            for value in values:
                if value.value != None:
                    vals.append(int(value.value))
            data_values[col_row].append(vals)
    
    for col_row, data_value in data_values.items():
        if col_row not in average_data_values:
            average_data_values[col_row] = []
        average_data_values[col_row] = list(map(mean, zip(*data_value)))

    for col_row, data_values in average_data_values.items():
        for idx, data_value in enumerate(data_values):
            all_data_values[col_row][idx].value = data_value
            
    
    return all_data_values    
                
def average_response_cards_x(study):
    average_cards_x = {}
    cards_x = {}
    all_cards_x = {}

    for col in range(study.number_of_columns):
        col_key = 'col_'+str(col)
        average_cards_x[col_key] = []
    for response in study.responses:
        response_cards_x = munchify(response.cards_x)
        for col, cards in response_cards_x.items(): 
            for card in cards:
                if card.id not in cards_x:
                    cards_x[card.id] = []
                col_num = col.split('_')[1]
                all_cards_x[card.id] = card
                cards_x[card.id].append(int(col_num))
    
    for card_id, cols in cards_x.items():
        card = all_cards_x[card_id]
        col = mean(cols)
        col_key = 'col_'+str(round(col))
        average_cards_x[col_key].append(card)
    
    return average_cards_x

def average_response_cards_y(study):
    average_cards_y = {}
    cards_y = {}
    all_cards_y = {}
    for row in range(study.number_of_rows):
        row_key = 'row_'+str(row)
        average_cards_y[row_key] = []

    for response in study.responses:
        response_cards_y = munchify(response.cards_y)
        for row, cards in response_cards_y.items():
            for card in cards:
                if card.id not in cards_y:
                    cards_y[card.id] = []
                row_num = row.split('_')[1]
                all_cards_y[card.id] = card
                cards_y[card.id].append(int(row_num))

    for card_id, rows in cards_y.items():
        card = all_cards_y[card_id]
        row = mean(rows)
        row_key = 'row_'+str(round(row))
        average_cards_y[row_key].append(card)
    return average_cards_y