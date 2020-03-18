# response = {'cards_x': {'0': ['1'], '1': [], '2': [], '3': []}, 'cards_y': {'0': [], '1': [], '2': [], '3': ['2']}, 'data_values': {'col-0-row-3': ['12'], 'col-1-row-3': ['4'], 'col-2-row-3': ['8'], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}}
from app import db
from app.models import HeatMap
import pdb

def find_combinations(study):
    # find all combinations of cards
    # and create heatmap for each.
    cards_set_x = study.card_sets[0]
    cards_set_y = study.card_sets[1]
    values = {}
    for col in range(study.number_of_columns):
        for row in range(study.number_of_rows):
            col_row = 'col-'+str(col)+'-row-'+str(row)
            values.update({col_row:0})
    for card_y in cards_set_y.cards:
        for card_x in cards_set_x.cards:
            for data_value_label in study.data_values_labels:
                heat_map = HeatMap(card_x=card_x, card_x_id=card_x.id, card_y=card_y, card_y_id=card_y.id, study=study.id, creator=study.creator, values=values, data_value_label=data_value_label.id)        
                db.session.add(heat_map)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return error