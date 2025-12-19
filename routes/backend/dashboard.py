from app import app, render_template
import requests

@app.route('/admin/dashboard')
def dashboard():
    module = 'dashboard'
    return render_template('backend/dashboard/index.html', module=module)