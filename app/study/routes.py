from app import db
from flask import render_template,flash, redirect, url_for, request
from app.study.forms import UserInfoForm
from flask_login import current_user, login_required
from app.models import CardSet, Response, Study
from datetime import date
from app.study import bp


@bp.route('/<study_id>', methods=['GET', 'POST'])
@login_required
def study(study_id):
    study = Study.query.filter_by(id=study_id).first_or_404()
    user_group = current_user.user_group
    
    if study.user_group_id != user_group.id or current_user.completed_study == True:
        flash('You cannot access this User Study')
        return redirect(url_for('study.index'))
    
    card_set_x = CardSet.query.filter_by(id=study.card_sets[0].id).first_or_404()
    card_set_y = CardSet.query.filter_by(id=study.card_sets[1].id).first_or_404()
    
    if request.method=='POST':
        
        
        data = request.get_json()
        print(data)
        response = Response(user=current_user.id, study=study.id, cards_x = data.get('cards_x'), cards_y = data.get('cards_y'), data_values=data.get('data_values'))
        current_user.completed_study = True
        db.session.add(response)
        db.session.commit()
        return dict(url=url_for('study.index'))
    
    
    return render_template('study/study.html', study=study, card_set_x=card_set_x, card_set_y=card_set_y, creator=user_group.creator_id)
    

@bp.route('/index')
@bp.route('/')
@login_required
def index():
    if current_user.completed_study == False:
        current_studies = (Study.query
                        .filter(Study.user_group_id == current_user.user_group_id)
                        .filter(Study.start_date <= date.today() )
                        .filter(Study.end_date >= date.today() ).all())
        return render_template('study/index.html', current_studies=current_studies)
    else:
        study = Study.query.filter(Study.user_group_id == current_user.user_group_id).first()
        return render_template('study/index.html', study = study)
        
@bp.route('/user_info', methods=['POST', 'GET'])
@login_required
def user_info():
    form = UserInfoForm()
    
    if current_user.completed_form is False and current_user.is_admin is False:
        if form.validate_on_submit():
            current_user.gender = form.gender.data
            current_user.age_group = form.age_group.data
            current_user.country_of_birth = form.nationality.data
            current_user.education_level = form.education_level.data
            current_user.occupation = form.occupation.data
            current_user.latest_country = form.latest_country.data
            current_user.income = form.income.data
            current_user.completed_form = True
            try:
                db.session.commit()
                redirect(url_for('study.index'))
            except:
                flash("There was a problem submitting your information. Please try again.")
                db.session.rollback()
                    
        if request.method=='GET':
            form.gender.data = current_user.gender
            form.age_group.data = current_user.age_group
            form.nationality.data = current_user.country_of_birth
            form.education_level.data = current_user.education_level
            form.occupation.data = current_user.occupation
            form.latest_country.data = current_user.latest_country
            form.income.data = current_user.income
            form.income.data
        else:
            return render_template('study/user_info.html', form=form)

    
    return redirect(url_for('study.index'))