from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
  user = {
    'nickname': 'QinFen'
  }
  return render_template('index.pug', title = 'Home', user=user)
