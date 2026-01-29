from fileinput import filename

from app import app, render_template, db
from model import MultiImage
import requests
from flask import request, redirect, abort, url_for, flash

from model.product import Product
from model.category import getCategoryList
from model.product import getAllProduct, getProductbyId
from flask_wtf import FlaskForm
from pathlib import Path

from werkzeug.utils import secure_filename
import uuid
import os

@app.route('/product_detail')
def product_detail():
    form = FlaskForm()
    pro_id = request.args.get('pro_id', 0, type=int)

    product = getProductbyId(pro_id)
    multi_images = MultiImage.query.filter_by(product_id=pro_id).all()

    if not product:
        return abort(404)

    return render_template(
        'frontend/product_detail.html',
        product=product,
        multi_images=multi_images,
        form=form
    )
