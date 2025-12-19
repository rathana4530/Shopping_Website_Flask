from app import app, render_template
import requests

@app.route('/shop')
def shop():
    return render_template('frontend/shop.html')