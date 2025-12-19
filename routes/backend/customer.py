from app import app, render_template
import requests

@app.route('/category')
def category():
    return render_template('backend/category/index.html')
