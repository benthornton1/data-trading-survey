from app.models import HeatMap
from app.responses.parsing.find_combinations import find_combinations
from tests.helpers import create_study

def test_get_find_combinations(client, init_database):
    """
    GIVEN a Flask application, study
    WHEN find_combinations is called 
    THEN check no error and db
    """
    
    study = create_study(client)
    
    find_combinations(study)
    
    heat_maps_db = HeatMap.query.all()
    
    assert heat_maps_db is not None
    assert len(heat_maps_db) == len(study.card_set_x.cards)*len(study.card_set_y.cards)*len(study.data_value_labels)*2
