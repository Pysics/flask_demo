from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
# app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
db = SQLAlchemy(app)

from app import views, models
