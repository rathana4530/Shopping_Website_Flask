from app import app, render_template
import requests

@app.route('/contact')
def contact():
    return render_template('frontend/contact.html')