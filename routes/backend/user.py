from app import app, render_template
import requests

@app.route('/customer')
def customer():
    return render_template('backend/customer/index.html')
