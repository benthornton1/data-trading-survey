from app import db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, SubmitField, TextAreaField, SelectField, FormField, FieldList
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from app.models import User, CardSet, UserGroup
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import or_, and_
from _datetime import date





class UserForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])

class CardForm(Form):
    card_name = StringField('Card Name', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg','png','.gif'], 'Images only')])
    desc = TextAreaField('desc', validators = [Optional(), Length(max=200)])

class CardSetForm(FlaskForm):
    card_set_name = StringField('Card Set Name', validators=[DataRequired()])
    cards = FieldList(FormField(CardForm), min_entries=1)
    measure = StringField('Measure', validators=[DataRequired()])
    submit = SubmitField('Create')

def card_set_choices():
    return CardSet.query.filter_by(creator=current_user.id)

def user_group_choices():
    return UserGroup.query.filter(creator_id=current_user.id).filter( or_(id=study_id, study=None))

class StudyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[Optional(), Length(max=400)])
    image = FileField('Image', validators=[FileAllowed(['jpg','png','.gif'], 'Images only')])
    cards_set_1 = QuerySelectField('Card Set for x-axis', validators=[DataRequired()], query_factory=card_set_choices)
    cards_set_2 = QuerySelectField('Card Set for y-axis', validators=[DataRequired()], query_factory=card_set_choices)
    data_values = SelectField('Data Values', choices=[('0',0),('1',1),('2',2)], validators=[DataRequired()], default=2)
    data_values_labels = FieldList(StringField('Data Value Label'), min_entries=2)
    number_of_columns = SelectField('Number of Columns', choices=[('2',2),('3',3),('4',4),('5',5)], validators=[DataRequired()], default=2)
    number_of_rows = SelectField('Number of Rows', choices=[('2',2),('3',3),('4',4),('5',5)], validators=[DataRequired()])
    user_group = QuerySelectField('User Study Participant Group', validators=[DataRequired()])
    start_date = DateField('Study Start Date', id='datepick',format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Study End Date',id='datepick', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create')
    
    def validate(self):
        if not super(StudyForm, self).validate():
            return False
        if self.end_date.data < self.start_date.data:
            msg = "The end date cannot be before the start date."
            self.end_date.errors.append(msg)
            return False
        if self.start_date.data < date.today():
            msg = "The start date cannot be in the past"
            self.start_date.errors.append(msg)
        if self.end_date.data < date.today():
            msg = 'The end date cannot be in the past'
            self.end_date.errors.append(msg)

        return True
            
class UserGroupForm(FlaskForm):
    name = StringField('User Group Name', validators=[DataRequired()])
    users = FieldList(FormField(UserForm), min_entries=1)
    submit = SubmitField('Create')
    
    