from app.models import Response, DataValue, CardPosition, Card, DataValueLabel
from werkzeug.exceptions import NotFound
from munch import munchify



def convert_response(cards_x, cards_y, data_values):
    dv = []
    cp = []
    cards_x_munch = munchify(cards_x)
    cards_y_munch = munchify(cards_y)
    data_values_munch = munchify(data_values)

    for col, cards in cards_x_munch.items():

        col_num = int(col.split("_")[1])
        for card in cards:

            card_db = Card.query.filter_by(id=card.id).first_or_404()

            card_position = CardPosition(position=col_num, card=card_db)
            cp.append(card_position)

    for row, cards in cards_y_munch.items():

        row_num = int(row.split("_")[1])
        for card in cards:

            card_db = Card.query.filter_by(id=card.id).first_or_404()

            card_position = CardPosition(position=row_num, card=card_db)
            cp.append(card_position)

    for col_row, data_values in data_values_munch.items():
        col_num = int(col_row.split("_")[1])
        row_num = int(col_row.split("_")[3])

        for data_value in data_values:
            data_value_label = DataValueLabel.query.filter_by(
                id=data_value.id
            ).first_or_404()

            if data_value.value is not None:
                data_value = DataValue(
                    column=col_num,
                    row=row_num,
                    value=data_value.value,
                    data_value_label=data_value_label,
                )
                dv.append(data_value)

    return Response(data_values=dv, card_positions=cp)
