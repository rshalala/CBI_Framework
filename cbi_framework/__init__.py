from enum import Enum
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

class Topic(Enum):
    HYPOTHESIS = 1
    TVD = 2
    CLASSIFICATION = 3

class Feedback_type(Enum):
    EXPLICIT = 1
    IMPLICIT = 2

app = Flask(__name__)
app.config['SECRET_KEY'] = '33c3b2532dc636687beeafb32333177b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['UPLOAD_FOLDER'] = 'cbi_framework/uploads/'
app.config['MODULES_FOLDER'] = 'cbi_framework/modules/'
app.config['NOTEBOOKS_FOLDER'] = 'cbi_framework/notebooks_to_analyze/'

db = SQLAlchemy(app)

# extract authorized emails from CSV files
from cbi_framework import tools
users_dict = tools.create_users_dictionary('cbi_framework/data/participants.csv')
authorized_emails = [*users_dict]

# create folder for temporary modules
try:
    os.mkdir(app.config['MODULES_FOLDER'])
except OSError as error:
    pass

# create folder for uploads in each topic
for topic in Topic:
    try:
        os.mkdir(app.config['UPLOAD_FOLDER'] + str.lower(topic.name))
    except OSError as error:
        pass

topic = Topic.CLASSIFICATION
from cbi_framework import views