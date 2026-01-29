
from app import app, render_template, db
import requests
from flask import request, redirect, abort, url_for, flash

from model.category import Category
from model.category import getCategoryList, getCategoryById
from flask_wtf import FlaskForm

@app.route('/admin/category')
def category():
    module = "category"
    form = FlaskForm()
    categories = getCategoryList()

    return render_template(
        'backend/category/index.html',
        form=form,
        categories=categories,
        module=module,
    )


@app.route('/admin/category/form')
def form_category():
    module = 'category'
    form = FlaskForm()
    action = request.args.get('action','add')
    if action not in ['add','edit']:
        return abort(404)

    category_id = request.args.get('category_id',0)
    status = 'add' if action == 'add' else 'edit'
    category = None
    if status == 'edit':
        category = getCategoryById(category_id)

    return render_template(
        'backend/category/form.html',
        module=module,
        form=form,
        status=status,
        category=category if status == 'edit' else None,
        category_id=category_id
    )

@app.route('/admin/category/save', methods=['POST'])
def save_category():
    status = request.form.get('status')   # add | edit
    category_id = request.form.get('category_id')

    categoryname = request.form.get('categoryname')
    description = request.form.get('description')

    if not categoryname:
        flash("Category name are required", "error")
        return redirect(url_for('form_category', action=status, category_id=category_id))

    try:
        if status == 'add':
            category = Category(
                categoryname = categoryname,
                # status = category_status,
                description = description
            )
            db.session.add(category)

        if status == 'edit':
            category = getCategoryById(category_id)
            category.categoryname = categoryname
            category.description = description

        db.session.commit()
        flash("category saved successfully!", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        flash("Error saving category", "error")
        return redirect(url_for('form_category', action=status, category_id=category_id))

    return redirect(url_for('category'))


@app.route('/admin/category/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category= Category.query.get_or_404(category_id)

    try:
        db.session.delete(category)
        db.session.commit()

        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting Category.', 'error')
        app.logger.error(f'Error deleting Category {category_id}: {str(e)}')

    return redirect(url_for('category'))
