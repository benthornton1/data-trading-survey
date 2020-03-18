# response = {'cards_x': {'0': ['1'], '1': [], '2': [], '3': []}, 'cards_y': {'0': [], '1': [], '2': [], '3': ['2']}, 'data_values': {'col-0-row-3': ['12'], 'col-1-row-3': ['4'], 'col-2-row-3': ['8'], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}}
import itertools
from app import db
from app.models import HeatMap
import pdb
from sqlalchemy.orm.attributes import flag_modified

def normalise_data_values(study, response):
    data_values = response.data_values
    if study.data_values > 0:
        all_values = data_values.values()
        data_value_0 = []
        data_value_1 = []
        for values in all_values:
            for idx,value in enumerate(values):
                if value == '':
                    value = 0
                if idx==0:
                    data_value_0.append(int(value))
                if idx==1:
                    data_value_1.append(int(value))   
    
        max_data_value_0 = max(data_value_0)
        min_data_value_0 = min(data_value_0)
        max_data_value_1 = 0
        min_data_value_1 = 0
        
        if study.data_values >1:
            max_data_value_1 = max(data_value_1)
            min_data_value_1 = min(data_value_1)

        for col_row, values in data_values.items():
            new_values = []
            for idx,value in enumerate(values):
                if value != '':
                    new_val = 0
                    if idx==0:
                        new_val = (int(value) - min_data_value_0)/(max_data_value_0-min_data_value_0)
                    if idx==1:
                        new_val = (int(value) - min_data_value_1)/(max_data_value_1-min_data_value_1)
                    new_values.append(new_val)
            data_values[col_row]=new_values
            
        return data_values
    
def update_heatmaps(cards_x, cards_y, response,study):
    # Update the collection of heatmaps with the normalised response
    normalised_data_values = normalise_data_values(study=study, response=response)
    combinations = []
    for col,card_x in cards_x.items():
        for row,card_y in cards_y.items():
            tuples = list(itertools.product(card_x,card_y))
            for combination in tuples:
                if all(combination):
                    combinations.append(combination)
    
    for data_value in range(study.data_values):
        pdb.set_trace()
        for combination in combinations:
            heat_map = (db.session.query(HeatMap).filter(HeatMap.card_x_id==int(combination[0]))
                    .filter(HeatMap.card_y_id==int(combination[1]))
                    .filter(HeatMap.study==study.id)
                    .filter(HeatMap.data_value_label==study.data_values_labels[data_value].id).first())
            if heat_map is not None:
                for col, cards_x in response.cards_x.items():
                    for row, cards_y in response.cards_y.items():
                        for card_x in cards_x:
                            for card_y in cards_y:
                                if int(card_x) == heat_map.card_x_id and int(card_y) == heat_map.card_y_id:
                                    col_row = 'col-'+col+'-row-'+row
                                    value = normalised_data_values[col_row] 
                                    if len(normalised_data_values[col_row])>0:
                                        heat_map.values[col_row] += value[data_value]
                flag_modified(heat_map,"values")