from app import app, render_template
import requests

@app.route('/admin')
def admin():
    return render_template('backend/dashboard/index.html')