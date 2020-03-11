from app import db
from flask import render_template,flash, redirect, url_for, request, current_app
from app.admin.forms import  StudyForm, CardSetForm, UserGroupForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Card, CardSet, DataValuesLabels, Study, User, UserGroup
from werkzeug.utils import secure_filename
from functools import wraps
# from app.scheduler import start_study_job
import os
import mimetypes
from werkzeug.datastructures import FileStorage, Headers
from app.admin import bp
from app.admin.decorators import admin_required

from datetime import date
import random
import string
from sqlalchemy import or_, and_


@bp.route('')
@admin_required
@login_required
def admin():
    studies = Study.query.filter_by(creator=current_user.id).all()
    for study in studies:
        if study.name == None:
            studies.remove(study)
            db.session.delete(study)
            db.session.commit()

    card_sets = CardSet.query.filter_by(creator=current_user.id).all()
    for card_set in card_sets:
        if card_set.name == None:
            card_sets.remove(card_set)
            db.session.delete(card_set)
            db.session.commit()

    user_groups = UserGroup.query.filter_by(creator_id=current_user.id).all()
    for user_group in user_groups:
        if user_group.name == None:
            user_groups.remove(user_group)
            db.session.delete(user_group)
            db.session.commit()
    
    return render_template('admin/admin_index.html', studies=studies, card_sets=card_sets, user_groups=user_groups, creator=current_user.id)

@bp.route('/edit_study/<int:study_id>', methods=['GET','POST'])
@admin_required
@login_required
def edit_study(study_id):
    study = Study.query.filter_by(id=study_id).first_or_404()
    form = StudyForm(data_values=study.data_values, number_of_columns=study.number_of_columns, number_of_rows=study.number_of_rows)
    form.user_group.query = UserGroup.query.filter(UserGroup.creator_id == current_user.id).filter( or_(UserGroup.study==study, UserGroup.study==None))
    
    
    if study.start_date:
        if study.start_date <= date.today():
            flash('You cannot edit this study as it is ongoing.')
            return redirect(url_for('admin.admin'))
        
    if form.validate_on_submit():
        study.name = form.name.data
        study.desc = form.desc.data
        
        
        if form.image.data is not None:
            file = form.image.data
            file_name = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],'img','study_images', str(current_user.id), file_name)
            
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)
            study.image = file_name
                
        study.card_sets = [form.cards_set_1.data, form.cards_set_2.data]
        
        study.data_values = form.data_values.data
        for label in study.data_values_labels:
            db.session.delete(label)
        db.session.commit()
        
        labels = []
        for label in form.data_values_labels.data:
            if label is not '':
                labels.append(DataValuesLabels(label=label, study_id=study.id))
        study.data_values_labels = labels    
        study.number_of_columns = form.number_of_columns.data
        study.number_of_rows = form.number_of_rows.data
        study.user_group_id = form.user_group.data.id
        study.start_date = form.start_date.data
        study.end_date = form.end_date.data
        try:
            db.session.commit()
            flash('Study Created/ Updated Succesfully')
            return redirect(url_for('admin.admin'))
        except Exception as error:
            db.session.rollback()
            flash('There was a problem creating your study')
        
        
    elif request.method=='GET' and study.card_sets != []:
        
        form.name.data = study.name
        form.desc.data = study.desc
        form.cards_set_1.data = study.card_sets[0]
        form.cards_set_2.data = study.card_sets[1]
        for idx, label in enumerate(study.data_values_labels):
            form_label = form.data_values_labels[idx]
            form_label.data = label.label
        form.start_date.data = study.start_date
        form.end_date.data = study.end_date
        
        if form.name.data is not None:
            form.submit.label.text = 'Update'
        
    return render_template('admin/edit_study.html', form=form, study=study)


@bp.route('/card_set/<card_set_id>', methods=['GET','POST'])
@login_required
@admin_required
def card_set(card_set_id):
    form = CardSetForm()
    card_set = CardSet.query.filter_by(id=card_set_id).first_or_404()
    if form.validate_on_submit():
        old_cards = Card.query.filter(Card.card_sets.contains(card_set)).all()

        # db.session.commit()
        
        card_set.cards = []
        
        card_set.name = form.card_set_name.data
        card_set.measure = form.measure.data
        
        card_list = []
        
        for card in form.cards.data:
            
            
            f = card.get('image')
            if f is not None:
                file_name = secure_filename(f.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],'img','card_images', str(current_user.id), file_name)
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                f.save(file_path)
                card_list.append(Card(name=card.get("card_name"), desc= card.get('desc'), image=file_name, creator=current_user.id))
            else:
                card_list.append(Card(name=card.get("card_name"), desc= card.get('desc'), creator=current_user.id))
        
        card_set.cards = card_list
        
        db.session.commit()

        for card in old_cards:
            db.session.delete(card)
        db.session.commit()
        
        flash('Card Set Created/ Updated Succesfully.')
        return redirect(url_for('admin.admin'))
    elif request.method=='GET':
        form.card_set_name.data = card_set.name
        form.measure.data = card_set.measure
    
        for idx,card in enumerate(card_set.cards):
            image = None
            if card.image is not None:
                image = card.image
            if card.desc is not None:
                form.cards.append_entry(dict(card_name=card.name, desc=card.desc, image=image))
            else:
                form.cards.append_entry(dict(card_name=card.name, desc='', image=image))

    
        if form.card_set_name.data is not None:
                form.submit.label.text = 'Update'
        
        
    return render_template('admin/card_set.html', form=form)


@bp.route('/user_group/<int:user_group_id>', methods=['GET','POST'])
@login_required
@admin_required
def user_group(user_group_id):
    form = UserGroupForm()
    user_group = UserGroup.query.filter_by(id=user_group_id).first_or_404()
    
    study = Study.query.filter_by(user_group_id=user_group.id).first()
    
    if study is not None and study.start_date <= date.today():
        flash('You cannot edit this user group as the Study is in progress.')
        return redirect(url_for('admin.admin'))
    
    if form.validate_on_submit():
        # replace attributes upon re-sumbission of form with updates, preventing duplicate users.
        
        user_group.name = form.name.data
        
        # Find participants who have been deleted from the user group form and delete them.
        if user_group.users is not None:
            for user in user_group.users:                
                emails = [val['email'] for val in form.users.data]
                if user.email not in emails:
                    db.session.delete(user)
        
        db.session.commit()
            
        for user in form.users.data:
            # Create new User object for new emails in the form.
            
            participant = User.query.filter_by(user_group_id=user_group_id, email=user.get('email')).first()
            if participant is None:
                username = ''.join(random.choice(string.ascii_letters) for i in range(5))
                new_participant = User(email=user.get('email'), username=username)
                user_group.users.append(new_participant)
                
        try:   
            db.session.commit()
            flash('User Group Created/ Updated Succesfully.')
            return redirect(url_for('admin.admin'))
        except Exception as error:
            flash('There was a problem updating your User Group')
            db.session.rollback()
    elif request.method == 'GET':
        form.name.data = user_group.name
        for user in user_group.users:
            form.users.append_entry(dict(email=user.email))

        if form.name.data is not None:
            form.submit.label.text = 'Update'
        
    return render_template('admin/user_group.html', form=form)


@bp.route('/new_study')
@login_required
def new_study():
    try:
        study = Study()
        study.creator = current_user.id
        db.session.add(study)
        db.session.commit()
        return redirect(url_for('admin.edit_study', study_id=study.id))
    except:
        flash('There was a problem creating a new Study.')
        return redirect(url_for('admin.admin'))
    
    
@bp.route('/new_user_group')
@login_required
@admin_required
def new_user_group():
    try:
        user_group = UserGroup()
        user_group.creator_id = current_user.id
        db.session.add(user_group)
        db.session.commit()
        return redirect(url_for('admin.user_group', user_group_id=user_group.id))
    except Exception as error:
        flash('There was a problem creating a new User Group.')
        return redirect(url_for('admin.admin'))

@bp.route('/new_card_set')
@login_required
@admin_required
def new_card_set():
    try:
        card_set = CardSet()
        card_set.creator = current_user.id
        db.session.add(card_set)
        db.session.commit()
        
        return redirect(url_for('admin.card_set', card_set_id=card_set.id))
    except Exception as error:
        db.session.rollback()
        flash('There was a problem creating a new Card Set.')
        return redirect(url_for('admin.admin'))

@bp.route('/delete/study/<int:study_id>', methods=['POST', 'GET'])
@login_required
def delete_study(study_id):
    try:
        obj = Study.query.filter_by(id=study_id).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        flash('Study {} succesfully deleted.'.format(obj.name))
        return redirect(url_for('admin.admin'))
    except:
        flash('There was a problem deleting this Study.')
        return redirect(url_for('admin.admin'))
    
@bp.route('/delete/user_group/<int:user_group_id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_user_group(user_group_id):
    try:
        obj = UserGroup.query.filter_by(id=user_group_id).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        flash('User Group {} succesfully deleted.'.format(obj.name))
        return redirect(url_for('admin.admin'))
    except:
        db.session.rollback()
        flash('There was a problem deleting this User Group.')
        return redirect(url_for('admin.admin'))
    
@bp.route('/delete/card_set/<int:card_set_id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_card_set(card_set_id):
    try:
        obj = CardSet.query.filter_by(id=card_set_id).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        flash('Card Set {} succesfully deleted.'.format(obj.name))
        return redirect(url_for('admin.admin'))
    except:
        db.session.rollback()
        flash('There was a problem deleting this Card Set.')
        return redirect(url_for('admin.admin'))