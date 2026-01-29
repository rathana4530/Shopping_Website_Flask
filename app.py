from datetime import timedelta

from flask import Flask,render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from datetime import datetime
import os
import config

app = Flask(__name__)

app.config.from_object(config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SECRET_KEY'] = 'super-secret-key'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)

csrf = CSRFProtect()
csrf.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import model

@app.before_request
def before_request():
    path = request.path   # use path, not url

    # Protect all /admin routes except login
    if path.startswith('/admin') and path not in ['/login', '/do_login']:
        if not session.get('user_id'):
            flash('You need to login first!', 'error')
            return redirect(url_for('login', next=path))

import routes

if __name__ == '__main__':
    app.run()
