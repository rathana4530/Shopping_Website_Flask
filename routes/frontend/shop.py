from app import app, render_template, db
import requests
from model.product import getAllProduct, getProductbyId
from flask_wtf import FlaskForm
@app.route('/shop')
def shop():
    form = FlaskForm()
    products = getAllProduct()
    return render_template('frontend/shop.html', products=products, form=form)