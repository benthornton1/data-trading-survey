from statistics import mean

from bokeh.models.formatters import FuncTickFormatter
from bokeh.models.tickers import FixedTicker
from flask import redirect
from flask import request
from flask.helpers import flash, send_file, url_for
from flask_login import current_user, login_required
from flask.templating import render_template
from munch import munchify
from sqlalchemy import desc
from werkzeug.exceptions import HTTPException

from app import db
from app.admin.decorators import valid_admin_required, admin_required
from app.models import Card, DataValueLabel, HeatMap, Response, Study
from app.responses import bp
from app.responses.parsing.add_heat_maps import CreateAllHeatMaps, CreateOneHeatMap
from app.responses.parsing.average_response2 import average_response as avg
from app.responses.parsing.create_pdf import create_pdf as gen_pdf
from app.responses.parsing.position_count import get_card_x_responses, get_card_y_responses


@bp.route('/<int:id>')
@login_required
@admin_required
@valid_admin_required(model="study")
def general(id, study):
    script_x, div_x = get_card_x_responses(study, study.responses)
    script_y, div_y = get_card_y_responses(study, study.responses)
        
    return render_template(
        'responses/general.html',
        plot_script_x=script_x,
        plot_div_x=div_x,
        plot_script_y=script_y,
        plot_div_y=div_y,
        responses=study.responses,
        study=study,
    )


@bp.route('/heat_maps/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
@valid_admin_required(model="study")
def heat_maps(id, study):

    if request.method =='POST':
        data = request.get_json()
        if data.get('type') == 'one':
            hm = CreateOneHeatMap()
            
            if data.get('label_id'):
                label = DataValueLabel.query.filter_by(id=data.get('label_id')).first()
                hm.add(card_x_id=data.get('card_x_id'), card_y_id=data.get('card_y_id'), label=label, study=study, is_count=data.get('is_count'))
            else:
                hm.add(card_x_id=data.get('card_x_id'), card_y_id=data.get('card_y_id'), study=study, is_count=data.get('is_count'))
            plots = hm.plots
        else:
            hm = CreateAllHeatMaps()
            hm.add(study=study, is_count=data.get('is_count'))
            plots = hm.plots
        return dict(plots=dict(plots))

        
    return render_template('responses/heat_maps.html', study=study, card_set_x=study.card_set_x, card_set_y=study.card_set_y)

@bp.route('/compare/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
@valid_admin_required(model="study")
def compare_responses(id, study):    
    if request.method == 'POST':
        data = request.get_json()
        try:
            if data.get('response_id_1') == 'average':
                response_1 = munchify(avg(study))
            else:
                response_1 = Response.query.filter(Response.study_id==study.id, Response.id==int(data.get('response_id_1'))).first()
            
            if data.get('response_id_2') == 'average':
                response_2 = munchify(avg(study))
            else:
                response_2 = Response.query.filter(Response.study_id==study.id, Response.id==int(data.get('response_id_2'))).first()
            return dict(data=render_template('responses/response.html', data_value_labels=study.data_value_labels, card_set_x=study.card_set_x, card_set_y=study.card_set_y, study=study, responses=[response_1, response_2]))
        except:
            flash('Invalid choice.')
            
    return render_template('responses/compare_responses.html', study=study, responses=study.responses)


@bp.route('/average/<int:id>')
@login_required
@admin_required
@valid_admin_required(model="study")
def average_response(id, study):

    avg_response = avg(study)
    return render_template('responses/average_response.html',data_value_labels=study.data_value_labels, study=study, card_set_x = study.card_set_x, card_set_y=study.card_set_y, average_response=avg_response)

@bp.route('/create_pdf/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
@valid_admin_required(model="study")
def create_pdf(id, study):
    
    if request.method=='POST':
        try:
            data = request.get_json()
            file_path = gen_pdf(study, all_responses=data.get('all_responses'), average_response2=data.get('average_response'), response_ids=data.get('response_ids'))
            return dict(file_path=file_path)
        except:
            flash('Could not create pdf.')
        
    return render_template('/responses/create_pdf.html', study=study, responses=study.responses)
