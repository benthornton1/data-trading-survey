import json

from flask import url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

# f_age_groups = open(url_for('static', filename='json/age_groups.json'))
f_age_groups = open('app/static/json/age_groups.json')
data = json.load(f_age_groups)
data_age_groups = [(k,v) for k, v in data.items()]
f_age_groups.close()

# f_countries = open(url_for('static', filename='json/countries.json'))
f_countries = open('app/static/json/countries.json')
data = json.load(f_countries)
data_countries = [(k,v) for k, v in data.items()]
f_countries.close()

# f_educations = open(url_for('static', filename='json/educations.json'))
f_educations = open('app/static/json/educations.json')
data = json.load(f_educations)
data_educations = [(k,v) for k, v in data.items()]
f_educations.close()

# f_genders = open(url_for('static', filename='json/genders.json'))
f_genders = open('app/static/json/genders.json')
data = json.load(f_genders)
data_genders = [(k,v) for k, v in data.items()]
f_genders.close()

# f_incomes = open(url_for('static', filename='json/incomes.json'))
f_incomes = open('app/static/json/incomes.json')
data = json.load(f_incomes)
data_incomes = [(k,v) for k, v in data.items()]
f_incomes.close()

# f_occupations = open(url_for('static', filename='json/occupations.json'))
f_occupations = open('app/static/json/occupations.json')
data = json.load(f_occupations)
data_occupations = [(k,v) for k, v in data.items()]
f_occupations.close()
    
class UserInfoForm(FlaskForm):
    gender = SelectField('Gender',choices=data_genders, validators=[DataRequired()])
    age_group = SelectField('Age Group',choices=data_age_groups, validators=[DataRequired()])
    nationality = SelectField('Country of Birth',choices=data_countries, validators=[DataRequired()])
    latest_country = SelectField('Latest Country',choices=data_countries, validators=[DataRequired()])
    education_level = SelectField('Education Level',choices=data_educations, validators=[DataRequired()])
    occupation = SelectField('Occupation',choices=data_occupations, validators=[DataRequired()])
    income = SelectField('Income',choices=data_incomes, validators=[DataRequired()])
    submit = SubmitField('Submit')