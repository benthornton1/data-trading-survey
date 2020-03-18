from app.responses import bp
from app import db
from flask import request
from app.admin.decorators import admin_required
from flask_login import current_user
from app.models import Card, Response, Study, HeatMap
from flask.templating import render_template
from sqlalchemy import desc
from app.responses.parsing.average_response import average_response as avg
from app.responses.parsing.position_count import get_card_x_responses, get_card_y_responses
from app.responses.parsing.add_heatmaps import CreateAllHeatMaps, CreateOneHeatMap
from statistics import mean
import pdb
from bokeh.models.formatters import FuncTickFormatter
from bokeh.models.tickers import FixedTicker


@bp.route('/')
@admin_required
def index():
    studies = Study.query.filter_by(creator=current_user.id).all()
    
    return render_template('responses/index.html', studies=studies)

@bp.route('/<int:study_id>')
def response(study_id):
    responses = Response.query.filter_by(study=study_id).all()
    study = Study.query.filter_by(id=study_id).first_or_404()

    script_x, div_x = get_card_x_responses(study, responses)
    script_y, div_y = get_card_y_responses(study, responses)
    avg_response = avg(study, responses)
    cards_y = avg_response.get('cards_y')
    cards_x = avg_response.get('cards_x')
    data_values = avg_response.get('data_values')
    card_set_x = study.card_sets[0]
    card_set_y = study.card_sets[1]
    data_values_labels = study.data_values_labels
    
   
    return render_template(
        'responses/average_response.html',
        plot_script_x=script_x,
        plot_div_x=div_x,
        plot_script_y=script_y,
        plot_div_y=div_y,
        study=study,
        creator=current_user.id,
        cards_x = cards_x,
        cards_y = cards_y,
        data_values = data_values,
        data_values_labels = data_values_labels,
        card_set_x = card_set_x,
        card_set_y = card_set_y
    )

@bp.route('/<int:study_id>')
def general(study_id):
    return "General"

@bp.route('/heat_maps/<int:study_id>', methods=['GET','POST'])
def heat_maps(study_id):
    study = Study.query.filter_by(id=study_id).first_or_404()
    if request.method =='POST':
        data = request.get_json()
        type = data.get('type')
        plots = []
        if type == 'one':
            card_x_id = data.get('card_x_id')
            card_y_id = data.get('card_y_id')
            hm = CreateOneHeatMap()
            plots = hm.add(card_x_id=card_x_id, card_y_id=card_y_id, study=study)
        else:
            hm = CreateAllHeatMaps()
            plots = hm.add(study=study)
            
        plots_dict = dict(plots)
        
        return dict(plots=plots_dict)

    return render_template('responses/heat_maps.html', study=study, card_set_x=study.card_sets[0], card_set_y=study.card_sets[1])

@bp.route('/compare/<int:study_id>')
def compare_responses(study_id):
    return "Compare"  
    
@bp.route('/average/<int:study_id>')
def average_response(study_id):
    return "Average"