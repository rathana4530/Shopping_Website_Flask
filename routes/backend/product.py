from fileinput import filename

from app import app, render_template, db
import requests
from flask import request, redirect, abort, url_for, flash

from model import getProductImages
from model.product import Product, getAllProduct, getProductbyId
from model.multi_image import MultiImage
from model.category import Category, getCategoryList, getCategoryById

from flask_wtf import FlaskForm
from pathlib import Path

from werkzeug.utils import secure_filename
import uuid
import os

import config
from upload_service import save_image


@app.route('/admin/product')
def product():
    module = 'product'
    form = FlaskForm()
    products = getAllProduct()
    return render_template('backend/product/index.html', module=module, products=products, form=form)


@app.route('/admin/product/detail/<int:pro_id>')
def product_details(pro_id):
    product = getProductbyId(pro_id)
    category = getCategoryById(product.category_id)
    form = FlaskForm()
    module = 'product'
    # Fetch multiple images for this product
    multi_images = MultiImage.query.filter_by(product_id=pro_id).all()

    return render_template(
        'backend/product/view.html',
        module=module,
        product=product,
        category=category,
        multi_images=multi_images,
        form=form  # Your CSRF form
    )


@app.route('/admin/product/form')
def form_product():
    module = 'product'
    form = FlaskForm()
    action = request.args.get('action', 'add')

    if action not in ['add', 'edit']:
        return abort(404)

    pro_id = request.args.get('pro_id', 0)
    status = 'add' if action == 'add' else 'edit'
    product = None
    existing_images = []

    if status == 'edit':
        product = getProductbyId(pro_id)
        if not product:
            flash('Product not found', 'error')
            return redirect(url_for('product'))
        existing_images = getProductImages(pro_id)

    category = getCategoryList()

    return render_template(
        'backend/product/form.html',
        module=module,
        status=status,
        pro_id=pro_id,
        product=product,
        category=category,
        existing_images=existing_images,
        form=form
    )


@app.route('/admin/product/delete/<int:pro_id>', methods=['POST'])
def delete_product(pro_id):
    product = getProductbyId(pro_id)
    old_image = product.image

    try:
        # Get all multi_images before deleting product
        multi_images = MultiImage.query.filter_by(product_id=pro_id).all()

        # Delete all multi_image files
        for multi_img in multi_images:
            delete_image_files(multi_img.image)
            db.session.delete(multi_img)

        # Delete main product image
        if old_image:
            delete_image_files(old_image)

        # Delete product (cascade will delete multi_images from DB)
        db.session.delete(product)

        db.session.commit()

        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting product.', 'error')
        app.logger.error(f'Error deleting product {pro_id}: {str(e)}')

    return redirect(url_for('product'))


@app.route('/admin/product/save', methods=['POST'])
def save_product():
    status = request.form.get('status')  # add | edit
    pro_id = request.form.get('pro_id')
    old_image = request.form.get('old_image')

    product_name = request.form.get('product_name')
    barcode = request.form.get('barcode')
    category = request.form.get('category')
    cost = request.form.get('cost')
    price = request.form.get('price')
    description = request.form.get('description')

    if not product_name or not price:
        flash("Product name and price are required", "error")
        return redirect(url_for('form_product', action=status, pro_id=pro_id))

    try:
        # Handle main product image
        images = None
        filename = old_image  # Keep old image by default
        file = request.files.get('image_path')

        if file and file.filename:
            filename = secure_filename(file.filename)
            images = save_image(
                file,
                app.config['UPLOAD_FOLDER'],
                app.config['ALLOWED_EXTENSIONS']
            )


        if status == 'add':
            if not file or not file.filename:
                flash('Main image is required', 'error')
                return redirect(url_for('form_product', action=status))

            # Create new product
            product = Product(
                productname=product_name,
                barcode=barcode,
                category_id=category,
                cost=cost,
                price=price,
                description=description,
                image=filename
            )
            db.session.add(product)
            db.session.flush()  # Get the product ID before committing

            # Handle multiple images for new product
            multi_images = request.files.getlist('multi_images[]')
            for img_file in multi_images:
                if img_file and img_file.filename:
                    img_filename = secure_filename(img_file.filename)
                    saved_image = save_image(
                        img_file,
                        app.config['UPLOAD_FOLDER'],
                        app.config['ALLOWED_EXTENSIONS']
                    )

                    # Create multi_image record
                    multi_img = MultiImage(
                        product_id=product.product_id,
                        image=img_filename
                    )

                    db.session.add(multi_img)

        elif status == 'edit':
            product = getProductbyId(pro_id)
            product.productname = product_name
            product.barcode = barcode
            product.category_id = category
            product.cost = cost
            product.price = price
            product.description = description

            # Update main image if new one uploaded
            if file and file.filename:
                product.image = filename
                # Delete old main image files
                if old_image:
                    delete_image_files(old_image)

            # Get all multi_images before deleting product
            del_multi_images = MultiImage.query.filter_by(product_id=pro_id).all()

            # Handle new multiple images
            multi_images = request.files.getlist('multi_images[]')

            # Only delete old images if new ones are uploaded
            if multi_images and multi_images[0].filename:
                for multi_img in del_multi_images:
                    delete_image_files(multi_img.image)
                    db.session.delete(multi_img)

            for img_file in multi_images:
                if img_file and img_file.filename:
                    img_filename = secure_filename(img_file.filename)
                    saved_image = save_image(
                        img_file,
                        app.config['UPLOAD_FOLDER'],
                        app.config['ALLOWED_EXTENSIONS']
                    )

                    # Create multi_image record
                    multi_img = MultiImage(
                        product_id=int(pro_id),
                        image=img_filename
                    )
                    db.session.add(multi_img)

        db.session.commit()
        flash("Product saved successfully!", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving product: {str(e)}")
        flash("Error saving product", "error")
        return redirect(url_for('form_product', action=status, pro_id=pro_id))

    return redirect(url_for('product'))


def delete_image_files(image_filename):
    """Helper function to delete image files (original, resized, and thumbnail)"""
    if not image_filename:
        return

    try:
        # Delete original image
        original_path = Path('./static/uploads/' + image_filename)
        if original_path.is_file():
            original_path.unlink()

        # Delete resized image
        resized_path = Path('./static/uploads/resized_' + image_filename)
        if resized_path.is_file():
            resized_path.unlink()

        # Delete thumbnail
        thumb_path = Path('./static/uploads/thumb_' + image_filename)
        if thumb_path.is_file():
            thumb_path.unlink()
    except Exception as e:
        app.logger.error(f"Error deleting image files for {image_filename}: {str(e)}")
