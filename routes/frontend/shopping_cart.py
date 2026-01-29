from app import app, render_template, db
import requests
from model.product import getAllProduct, getProductbyId
from flask_wtf import FlaskForm
@app.route('/shopping_cart')
def shopping_cart():
    return render_template('frontend/shopping_cart.html')