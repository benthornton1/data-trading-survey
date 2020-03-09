import json
f_age_groups = open("age_groups.json")
data = json.load(f_age_groups)
data_age_groups = tuple(data.items())
f_age_groups.close()

f_countries = open("countries.json")
data = json.load(f_countries)
data_countries = tuple(data.items())
f_countries.close()

f_educations = open("educations.json")
data = json.load(f_educations)
data_educations = tuple(data.items())
f_educations.close()

f_genders = open("genders.json")
data = json.load(f_genders)
data_genders = tuple(data.items())
f_genders.close()

f_incomes = open("incomes.json")
data = json.load(f_incomes)
data_incomes = tuple(data.items())
f_incomes.close()

f_occupations = open("occupations.json")
data = json.load(f_occupations)
data_occupations = tuple(data.items())
f_occupations.close()


