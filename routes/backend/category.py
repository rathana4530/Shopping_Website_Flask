from app import app, render_template
import requests

@app.route('/product')
def product():
    return render_template('backend/product/index.html')