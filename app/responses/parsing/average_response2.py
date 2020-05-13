from statistics import mean


from munch import munchify

from app.models import Card
from app.models import DataValue, Response, CardPosition


def average_response(study):
    card_positions_x = average_card_positions_x(study)
    cards_positions_y = average_card_positions_y(study)
    data_values = average_response_data_values(study)

    average_response = Response(
        data_values=data_values, card_positions=card_positions_x + cards_positions_y
    )

    return average_response


def average_response_data_values(study):

    data_values_derived = {}
    for column in range(study.number_of_columns):
        for row in range(study.number_of_rows):
            for data_value_label in study.data_value_labels:
                data_value = DataValue(
                    column=column, row=row, value=0, data_value_label=data_value_label
                )
                data_values_derived.update({data_value: 0})

    for response in study.responses:
        for data_value in response.data_values:
            for data_value_derived in data_values_derived.keys():
                if (
                    data_value.column == data_value_derived.column
                    and data_value.row == data_value_derived.row
                ):
                    data_value_derived.value += data_value.value
                    data_values_derived[data_value_derived] += 1

    for data_value_derived, count in data_values_derived.items():
        data_value_derived.value = data_value_derived.value / count

    return list(data_values_derived.keys())


def average_card_positions_x(study):

    card_positions_derived = {}
    for card in study.card_set_x.cards:
        card_position_derived = CardPosition(card=card, position=0)
        card_positions_derived.update({card_position_derived: 0})

    for response in study.responses:
        for card_position in response.card_positions:
            for card_position_derived in card_positions_derived.keys():
                if card_position.card == card_position_derived.card:
                    card_position_derived.position += card_position.position
                    card_positions_derived[card_position_derived] += 1

    for card_position_derived, count in card_positions_derived.items():
        try:
            card_position_derived.position = int(card_position_derived.position / count)
        except ZeroDivisionError:
            card_position_derived.position = 0

    return list(card_positions_derived.keys())


def average_card_positions_y(study):
    card_positions_derived = {}
    for card in study.card_set_y.cards:
        card_position_derived = CardPosition(card=card, position=0)
        card_positions_derived.update({card_position_derived: 0})

    for response in study.responses:
        for card_position in response.card_positions:
            for card_position_derived in card_positions_derived.keys():
                if card_position.card == card_position_derived.card:
                    card_position_derived.position += card_position.position
                    card_positions_derived[card_position_derived] += 1

    for card_position_derived, count in card_positions_derived.items():
        try:
            card_position_derived.position = int(card_position_derived.position / count)
        except ZeroDivisionError:
            card_position_derived.position = 0
    return list(card_positions_derived.keys())
