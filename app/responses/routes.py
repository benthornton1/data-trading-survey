from app.responses import bp
from app.admin.decorators import admin_required
from flask_login import current_user
from app.models import Card, Response, Study
from flask.templating import render_template
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE

from app.responses.parsing.average_response import average_response
from app.responses.parsing.position_count import get_card_x_responses, get_card_y_responses
from statistics import mean


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
    avg_response = average_response(study, responses)
    cards_y = avg_response.get('cards_y')
    cards_x = avg_response.get('cards_x')
    data_values = avg_response.get('data_values')
    card_set_x = study.card_sets[0]
    card_set_y = study.card_sets[1]
    data_values_labels = study.data_values_labels
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    
    return render_template(
        'responses/average_response.html',
        plot_script_x=script_x,
        plot_div_x=div_x,
        plot_script_y=script_y,
        plot_div_y=div_y,
        js_resources=js_resources,
        css_resources=css_resources,
        study=study,
        creator=current_user.id,
        cards_x = cards_x,
        cards_y = cards_y,
        data_values = data_values,
        data_values_labels = data_values_labels,
        card_set_x = card_set_x,
        card_set_y = card_set_y
    )



# {'cards_x': {'0': ['1'], '1': [], '2': [], '3': []}, 'cards_y': {'0': [], '1': [], '2': [], '3': ['2']}, 'data_values': {'col-0-row-3': ['12'], 'col-1-row-3': [''], 'col-2-row-3': [''], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}}