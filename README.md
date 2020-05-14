# Data Trading Survey Platform

This project is a Flask survey application which allows the creation and participation of an interactive study ranking items in one category against items in another category and allowing the participant to give numerical values to their ranking. The application also supports some data analysis of responses and an API.

It is intended to help identify the trends in different types of data a person may be willing to trade to different organisations and at what cost under the [Sensing as a Service (S2aaS) model](https://arxiv.org/abs/1702.02380). But has uses beyond the one identified here.
## Installation
I recommend to install Python dependencies within a virtual environment:

```bash
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```
Then install the Python dependencies inside the ```requirements.txt``` file
```bash
pip install -r requirements.txt
```
To install the non-Python dependencies, using Homebrew, run the following:
```bash
brew install wkhtmltopdf
```
## Usage
Set up environment variables and migrate changes to database. The development environment uses an SQLite database by default.
```bash
export FLASK_PROJECT_SECRET_KEY=areallysecretkey 
export FLASK_MAIL_PORT=<your-smtp-mail-port>
export FLASK_PROJECT_MAIL_USE_TLS=1
export FLASK_PROJECT_MAIL_USERNAME=<your-mail-username>
export FLASK_PROJECT_MAIL_PASSWORD=<your-mail-password>
export FLASK_ENV=development
flask db migrate
flask db upgrade
flask run
```
to create and administrator account.
```bash
flask shell
```
```python
>> admin = Admin(username='admin')
>> admin.set_password('your_password')
>> db.session.add(admin)
>> db.session.commit()
```
You will now be able to log in with those details.

to run the tests
```bash
pytest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)