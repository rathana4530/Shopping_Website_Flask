from app import app, render_template
from flask import session, flash, redirect, url_for, request
import requests

@app.route('/admin')
@app.route('/admin/')
def dashboard():

    module = 'dashboard'
    return render_template('backend/dashboard/index.html', module=module)