from statistics import mean


from munch import munchify

from app.models import Card
from app.models import DataValue, Response2, CardPosition

def average_response(study):
    card_positions_x = average_card_positions_x(study)
    cards_positions_y = average_card_positions_y(study)
    data_values = average_response_data_values(study)
    
    average_response = Response2(data_values=data_values, card_positions=card_positions_x+cards_positions_y)
    
    return average_response


def average_response_data_values(study):
    # average_data_values = {}
    # data_values = {}
    # all_data_values = {}
    
    data_values_derived = {}
    for column in range(study.number_of_columns):
        for row in range(study.number_of_rows):
            for data_value_label in study.data_value_labels:
                data_value = DataValue(column=column, row=row, value=0, data_value_label=data_value_label)
                data_values_derived.update({data_value: 0})
    
    for response in study.responses_2:
        for data_value in response.data_values:
            for data_value_derived in data_values_derived.keys():
                if data_value.column == data_value_derived.column and data_value.row == data_value_derived.row:
                    data_value_derived.value += data_value.value
                    data_values_derived[data_value_derived] += 1
    
    for data_value_derived, count in data_values_derived.items():
        data_value_derived.value = data_value_derived.value/count

    return list(data_values_derived.keys())

    # for response in study.responses:
    #     response_data_values = munchify(response.data_values)
    #     for col_row, values in response_data_values.items():
    #         if col_row not in data_values:
    #             data_values[col_row] = []
    #         if col_row not in all_data_values:
    #             all_data_values[col_row] = values
    #         vals = []
    #         for value in values:
    #             if value.value is not None:
    #                 vals.append(int(value.value))
    #         data_values[col_row].append(vals)

    # for col_row, data_value in data_values.items():
    #     if col_row not in average_data_values:
    #         average_data_values[col_row] = []
    #     average_data_values[col_row] = list(map(mean, zip(*data_value)))

    # for col_row, data_values in average_data_values.items():
    #     for idx, data_value in enumerate(data_values):
    #         all_data_values[col_row][idx].value = data_value

    # return all_data_values


def average_card_positions_x(study):
    # average_cards_x = {}
    # cards_x = {}
    # all_cards_x = {}
    card_positions_derived = {}
    for card in study.card_set_x.cards:
        card_position_derived = CardPosition(card=card, position=0)
        card_positions_derived.update({card_position_derived: 0})

    for response in study.responses_2:
        for card_position in response.card_positions:
            for card_position_derived in card_positions_derived.keys():
                if card_position.card == card_position_derived.card:
                    card_position_derived.position += card_position.position
                    card_positions_derived[card_position_derived] += 1

    for card_position_derived, count in card_positions_derived.items():
        card_position_derived.position = int(card_position_derived.position/count)

    return list(card_positions_derived.keys()) 
    
    # for col in range(study.number_of_columns):
    #     col_key = "col_" + str(col)
    #     average_cards_x[col_key] = []
    # for response in study.responses:
    #     response_cards_x = munchify(response.cards_x)
    #     for col, cards in response_cards_x.items():
    #         for card in cards:
    #             if card.id not in cards_x:
    #                 cards_x[card.id] = []
    #             col_num = col.split("_")[1]
    #             all_cards_x[card.id] = card
    #             cards_x[card.id].append(int(col_num))

    # for card_id, cols in cards_x.items():
    #     card = all_cards_x[card_id]
    #     col = mean(cols)
    #     col_key = "col_" + str(round(col))
    #     average_cards_x[col_key].append(card)

    # return average_cards_x


def average_card_positions_y(study):
    card_positions_derived = {}
    for card in study.card_set_y.cards:
        card_position_derived = CardPosition(card=card, position=0)
        card_positions_derived.update({card_position_derived:0})

    for response in study.responses_2:
        for card_position in response.card_positions:
            for card_position_derived in card_positions_derived.keys():
                if card_position.card == card_position_derived.card:
                    card_position_derived.position += card_position.position
                    card_positions_derived[card_position_derived] += 1
    
    for card_position_derived, count in card_positions_derived.items():
        card_position_derived.position = int(card_position_derived.position/count)

    return list(card_positions_derived.keys()) 

    # average_cards_y = {}
    # cards_y = {}
    # all_cards_y = {}
    # for row in range(study.number_of_rows):
    #     row_key = "row_" + str(row)
    #     average_cards_y[row_key] = []

    # for response in study.responses:
    #     response_cards_y = munchify(response.cards_y)
    #     for row, cards in response_cards_y.items():
    #         for card in cards:
    #             if card.id not in cards_y:
    #                 cards_y[card.id] = []
    #             row_num = row.split("_")[1]
    #             all_cards_y[card.id] = card
    #             cards_y[card.id].append(int(row_num))

    # for card_id, rows in cards_y.items():
    #     card = all_cards_y[card_id]
    #     row = mean(rows)
    #     row_key = "row_" + str(round(row))
    #     average_cards_y[row_key].append(card)
    # return average_cards_y
