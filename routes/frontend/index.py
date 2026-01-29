from app import app, render_template, db
import requests
from model.product import getAllProduct, getProductbyId
from model.multi_image import MultiImage
from flask_wtf import FlaskForm
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    module = 'home'
    form = FlaskForm()
    products = getAllProduct()
    return render_template('frontend/index.html', products=products, module=module, form=form)


@app.route('/get-product/<int:product_id>')
def get_product(product_id):
    try:
        product = getProductbyId(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Fetch multiple images
        multi_images = MultiImage.query.filter_by(product_id=product_id).all()

        # Build response data
        response_data = {
            'id': product.id,
            'productname': product.productname,
            'price': float(product.price),
            'description': getattr(product, 'description', 'No description available.'),
            'image': product.image if product.image else None,
            'multi_images': [{'image': img.image} for img in multi_images]
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error fetching product {product_id}: {str(e)}")  # For debugging
        return jsonify({'error': 'Failed to load product details'}), 500
