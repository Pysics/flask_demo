import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# login and signup
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')
# app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models

if not app.debug:
  import logging
  from logging.handlers import SMTPHandler, RotatingFileHandler
  credentials = None
  if MAIL_USERNAME or MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, '出现错误', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

  # 日志
  file_handler = RotatingFileHandler('tmp/flask_app.log', 'a', 1 * 1024 * 1024, 10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  file_handler.setLevel(logging.INFO)
  app.logger.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('Flask App')
