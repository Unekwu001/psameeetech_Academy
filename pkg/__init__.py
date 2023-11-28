from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'unekwutheophilus@gmail.com'
app.config['MAIL_PASSWORD'] = 'nhichanaffghfdko'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db=SQLAlchemy(app)

mail=Mail(app)

from pkg import routes

