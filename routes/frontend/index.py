from app import app, render_template
import requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('frontend/index.html')