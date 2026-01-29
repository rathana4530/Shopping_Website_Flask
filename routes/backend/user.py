from fileinput import filename

from app import app, render_template, db
import requests
from flask import request, redirect, abort, url_for, flash

from model.role import getAllRole
from model.user import getAllUser, getUserbyId
from model.user import User

from flask_wtf import FlaskForm
from pathlib import Path

from werkzeug.utils import secure_filename
import uuid
import os

import config
from upload_service import save_image

@app.route('/admin/user')
def user():
    module = 'user'
    form = FlaskForm()
    users = getAllUser()
    return render_template('backend/user/index.html', module=module, form=form, users=users)


@app.route('/admin/user/detail/<int:user_id>')
def user_details(user_id):
    user = getUserbyId(user_id)
    form = FlaskForm()
    module = 'user'

    return render_template(
        'backend/user/view.html',
        module=module,
        user=user,
        form=form  # Your CSRF form
    )

@app.route('/admin/user/form')
def form_user():
    module = 'user'
    form = FlaskForm()
    action = request.args.get('action','add')
    if action not in ['add','edit']:
        return abort(404)

    user_id = request.args.get('user_id',0)
    status = 'add' if action == 'add' else 'edit'
    roles = getAllRole()

    user = None
    if status == 'edit':
        user = getUserbyId(user_id)

    return render_template('backend/user/form.html', module=module, status=status,form=form, user=user, user_id=user_id, roles=roles)

@app.route('/admin/user/save', methods=['POST'])
def save_user():
    user_id = request.form.get('user_id')
    status = request.form.get('status')
    old_image = request.form.get('old_image')

    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    address = request.form.get('address')
    role_id = request.form.get('role_id')
    user_status = request.form.get('user_status')

    # Determine if add or edit based on user_id presence
    action = 'edit' if user_id else 'add'

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

    # Validate required fields
    if not username or not email or not phone or not role_id:
        flash("Username, email, phone and role are required", "error")
        return redirect(url_for('form_user', action=action, user_id=user_id))

    # Password is required for new users
    if action == 'add' and not password:
        flash("Password is required for new users", "error")
        return redirect(url_for('form_user', action=action, user_id=user_id))

    try:
        if action == 'add':
            # Create new user
            user = User(
                username=username,
                email=email,
                phone=phone,
                address=address,
                role_id=role_id,
                status=int(user_status) if status else 1,
                image=filename
            )

            # Hash password before saving
            if password:
                user.set_password(password)  # Assuming you have this method in your User model
                # OR use: user.password = generate_password_hash(password)

            db.session.add(user)
            db.session.flush()

        elif action == 'edit':
            user = getUserbyId(user_id)
            if not user:
                flash("User not found", "error")
                return redirect(url_for('user'))

            # Update user fields
            user.username = username
            user.email = email
            user.phone = phone
            user.address = address
            user.role_id = role_id
            user.status = int(user_status) if status else 1

            # Update password only if provided
            if password:
                user.set_password(password)
                # OR use: user.password = generate_password_hash(password)

            # Update image if new one uploaded
            if file and file.filename:
                user.image = filename
                # Delete old image files
                if old_image:
                    delete_image_files(old_image)

        db.session.commit()
        flash("User saved successfully!", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving user: {str(e)}")
        flash(f"Error saving user: {str(e)}", "error")
        return redirect(url_for('form_user', action=action, user_id=user_id))

    return redirect(url_for('user'))

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = getUserbyId(user_id)
    old_image = user.images

    try:
        # Delete main user image
        if old_image:
            delete_image_files(old_image)

        db.session.delete(user)

        db.session.commit()

        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user.', 'error')
        app.logger.error(f'Error deleting user {user_id}: {str(e)}')

    return redirect(url_for('user'))

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