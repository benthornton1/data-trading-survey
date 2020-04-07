from app import db
from app.models import HeatMap

def find_combinations(study):
    # find all combinations of cards
    # and create heatmap for each.
    cards_set_x = study.card_set_x
    cards_set_y = study.card_set_y
    values = {}
    for col in range(int(study.number_of_columns)):
        for row in range(int(study.number_of_rows)):
            col_row = 'col_'+str(col)+'_row_'+str(row)
            values.update({col_row:0})
    for card_y in cards_set_y.cards:
        for card_x in cards_set_x.cards:
            heat_map1 = HeatMap(card_x=card_x, card_x_id=card_x.id, card_y=card_y, card_y_id=card_y.id, study_id=study.id, creator_id=study.creator_id, values=values, is_count=True)
            db.session.add(heat_map1)
            for data_value_label in study.data_value_labels: 
                heat_map2 = HeatMap(card_x=card_x, card_x_id=card_x.id, card_y=card_y, card_y_id=card_y.id, study_id=study.id, creator_id=study.creator_id, values=values, data_value_label=data_value_label, is_count=False)
                        
                db.session.add(heat_map2)

    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()