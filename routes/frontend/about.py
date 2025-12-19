from app import app, render_template
import requests

@app.route('/about')
def about():
    return render_template('frontend/about.html')