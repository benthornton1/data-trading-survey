from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_required

from app import jwt, csrf
from app.api import bp
from app.api.helpers import (create_response_json, create_participant_json, create_card_json, create_card_set_json,
                create_data_value_label_json, create_study_json, create_heat_map_json, create_user_group_json) 
from app.models import Admin, Card, CardSet, DataValueLabel, HeatMap, Participant, Response, Study, User, UserGroup

error_not_found = {'error':'resource not found'}

@bp.route('/login', methods=['POST'])
@csrf.exempt
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"error": "Missing username parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400
    
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Incorrect username or password"}), 401
    if not user.type == 'admin':
        return jsonify({"error":"Unauthorised"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@bp.route('/get/response/<int:id>')
@jwt_required
def get_response(id):
    response = (Response.query.filter(Response.id==id)
                    .filter(Response.creator_id==get_jwt_identity())
                    .first())
    if response is None:
        return jsonify(error_not_found)
    else:
        return jsonify({'id':response.id, 
                    'participant_id':response.participant_id,
                    'cards_x':response.cards_x,
                    'cards_y':response.cards_y,
                    'data_values':response.data_values
                    })

@bp.route('get/response/all')
@jwt_required
def get_all_responses():
    responses = (Response.query.filter_by(creator_id=get_jwt_identity()).all())
    if not responses:
        return jsonify(error_not_found)
    else:
        return jsonify([create_response_json(response) for response in responses])

@bp.route('/get/participant/<int:id>')
@jwt_required
def get_participant(id):
    participant = Participant.query.filter_by(id=id).first()
    if participant is None:
        return jsonify(error_not_found)
    else:
        if participant.user_group.creator_id == get_jwt_identity():
            return jsonify(create_participant_json(participant))
        else:
            return jsonify(error_not_found)

@bp.route('/get/participant/all')
@jwt_required
def get_all_participants():
    user_groups = UserGroup.query.filter_by(creator_id=get_jwt_identity()).all()
    if not user_groups:
        return jsonify(error_not_found)
    else:
        participants = []
        for user_group in user_groups:
            for user in user_group.users:
                participants.append(create_participant_json(user))
        return jsonify(participants)

@bp.route('/get/user_group/<int:id>')
@jwt_required
def get_user_group(id):
    user_group = (UserGroup.query.filter(UserGroup.id==id)
                    .filter(UserGroup.creator_id==get_jwt_identity())
                    .first())
    if user_group is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_user_group_json(user_group))
        
@bp.route('/get/user_group/all')
@jwt_required
def get_all_user_groups():
    user_groups = UserGroup.query.filter_by(creator_id=get_jwt_identity()).all()
    if not user_groups:
        return jsonify(error_not_found)
    else:
        return jsonify([create_user_group_json(user_group) for user_group in user_groups])

@bp.route('/get/data_value_label/<int:id>')
@jwt_required
def get_data_value_label(id):
    data_value_label = (DataValueLabel.query.filter(DataValueLabel.id==id)
                    .filter(DataValueLabel.creator_id==get_jwt_identity())
                    .first())
    
    if data_value_label is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_data_value_label_json(data_value_label))

@bp.route('/get/data_value_label/all')
@jwt_required
def get_all_data_value_labels():
    data_value_labels = DataValueLabel.query.filter_by(creator_id=get_jwt_identity()).all()
    if not data_value_labels:
        return jsonify(error_not_found)
    else:
        return jsonify([create_data_value_label_json(data_value_label) for data_value_label in data_value_labels])


@bp.route('/get/study/<int:id>')
@jwt_required
def get_study(id):
    study = (Study.query.filter(Study.id==id)
                    .filter(Study.creator_id==get_jwt_identity())
                    .first())
    if study is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_study_json(study))

@bp.route('/get/study/all')
@jwt_required
def get_all_studies():
    studies = Study.query.filter_by(creator_id=get_jwt_identity()).all()
    if not studies:
        return jsonify(error_not_found)
    else:
        return jsonify([create_study_json(study) for study in studies ])
    

@bp.route('/get/heat_map/<int:id>')
@jwt_required
def get_heat_map(id):
    heat_map = (HeatMap.query.filter(HeatMap.id==id)
                    .filter(CardSet.creator_id==get_jwt_identity())
                    .first())
    if heat_map is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_heat_map_json(heat_map))
        
@bp.route('/get/heat_map/all')
@jwt_required
def get_all_heat_maps():
    heat_maps = HeatMap.query.filter_by(creator_id=get_jwt_identity()).all()
    if not heat_maps:
        return jsonify(error_not_found)
    else:
        return jsonify([create_heat_map_json(heat_map) for heat_map in heat_maps])

@bp.route('/get/card_set/<int:id>')
@jwt_required
def get_card_set(id):
    card_set = (CardSet.query.filter(CardSet.id==id)
                    .filter(CardSet.creator_id==get_jwt_identity())
                    .first())
    if card_set is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_card_set_json(card_set))

@bp.route('/get/card_set/all')
@jwt_required
def get_all_card_sets():
    card_sets = CardSet.query.filter_by(creator_id=get_jwt_identity()).all()
    if not card_sets:
        return jsonify(error_not_found)
    else:
        return jsonify([create_card_set_json(card_set) for card_set in card_sets])

@bp.route('/get/card/<int:id>')
@jwt_required
def get_card(id):
    card = (Card.query.filter(Card.id==id)
                    .filter(Card.creator_id==get_jwt_identity())
                    .first())
    if card is None:
        return jsonify(error_not_found)
    else:
        return jsonify(create_card_json(card))
    
@bp.route('/get/card/all')
@jwt_required
def get_all_cards():
    cards = Card.query.filter_by(creator_id=get_jwt_identity()).all()
    if not cards:
        return jsonify(error_not_found)
    else:
        return jsonify([create_card_json(card) for card in cards])