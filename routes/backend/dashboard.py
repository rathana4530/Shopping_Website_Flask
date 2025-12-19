from app import app, render_template
import requests

@app.route('/admin')
def admin():
    module = 'index'
    return render_template('backend/dashboard/index.html', module=module)