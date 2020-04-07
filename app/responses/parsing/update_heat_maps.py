import itertools

from munch import munchify
from sqlalchemy.orm.attributes import flag_modified

from app import db
from app.models import HeatMap



def normalise_data_values(response):
    data_values = munchify(response.data_values)
    if response.study.data_values > 0:
        all_values = data_values.values()
        data_value_0 = []
        data_value_1 = []
        for values in all_values:
            for idx,value in enumerate(values):
                if idx==0 and value.value != None:
                    data_value_0.append(value.value)
                if idx==1 and value.value != None:
                    data_value_1.append(value.value)   
    
        max_data_value_0 = max(data_value_0)
        min_data_value_0 = min(data_value_0)
        max_data_value_1 = 0
        min_data_value_1 = 0

        if response.study.data_values >1:
            max_data_value_1 = max(data_value_1)
            min_data_value_1 = min(data_value_1)
        for col_row, values in data_values.items():
            for idx,value in enumerate(values):
                if value.value != '' and value.value != None:
                    new_val = 0
                    try:
                        if idx==0:
                            new_val = (value.value - min_data_value_0)/(max_data_value_0-min_data_value_0)
                        if idx==1:
                            new_val = (value.value - min_data_value_1)/(max_data_value_1-min_data_value_1)
                    except:
                        new_val = 1
                        
                    data_values[col_row][idx].value=new_val
                    
        return data_values
    
def update_heat_maps(response):
    # Update the collection of heatmaps with the normalised response
    normalised_data_values = normalise_data_values(response=response)

    response_cards_x = munchify(response.cards_x)
    response_cards_y = munchify(response.cards_y)
    heat_maps = HeatMap.query.filter(HeatMap.study==response.study, HeatMap.is_count==False).all()
    for label_idx,label in enumerate(response.study.data_value_labels):
        
        for col, cards_x in response_cards_x.items():
            for row, cards_y in response_cards_y.items():
                col2 = col.split('_')[1]
                row2 = row.split('_')[1]
                col_row = 'col_'+col2+'_row_'+row2
                for card_x in cards_x:
                    for card_y in cards_y:
                        for heat_map in heat_maps:
                            if card_x.id == heat_map.card_x_id and card_y.id == heat_map.card_y_id \
                                and heat_map.data_value_label == label:
                                    value = normalised_data_values[col_row] 
                                    if len(normalised_data_values[col_row])>0:
                                        heat_map.values[col_row] += value[label_idx].value 
                                    flag_modified(heat_map,"values")
                                    break
    ret_heat_maps = []
    for heat_map in heat_maps:
        ret_heat_maps.append(heat_map)
    
    # Update count heat maps 
    heat_maps_count = (db.session.query(HeatMap).filter(HeatMap.study_id==response.study_id).filter(HeatMap.is_count==True).all())
    for col,cards_x in response_cards_x.items():
        for row, cards_y in response_cards_y.items():
            col_row = 'col_'+col.split('_')[1]+'_row_'+row.split('_')[1]
            for card_x in cards_x:
                for card_y in cards_y:
                    for heat_map in heat_maps_count:
                        if card_x.id == heat_map.card_x_id and card_y.id == heat_map.card_y_id:
                            heat_map.values[col_row] += 1
                        flag_modified(heat_map,"values")
    
    
    for heat_map in heat_maps_count:
        ret_heat_maps.append(heat_map)
    
    return ret_heat_maps
                        