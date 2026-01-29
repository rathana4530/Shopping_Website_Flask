from app import app, render_template, db, request, flash, redirect, url_for, session
from model import User, getUserByName, Role
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash


@app.route('/login')
def login():
    form = FlaskForm()
    return render_template('backend/auth/login.html', form=form)


@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate input
    if not username or not password:
        flash('Username and password required', 'error')
        return redirect(url_for('login'))

    # Get user
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    # Check password
    if not user.check_password(password):
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    # Get admin role to prevent regular users from accessing backend
    admin_role = Role.query.filter_by(role_name='admin').first()

    # Check if user has admin privileges (adjust based on your role system)
    if not admin_role or user.role_id != admin_role.role_id:
        flash('You do not have permission to access this area.', 'error')
        return redirect(url_for('login'))

    # Check if user account is active
    if not user.status:
        flash('Your account has been disabled. Please contact administrator.', 'error')
        return redirect(url_for('login'))

    if user:
        if user.check_password(password):
            # Login success
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['image'] = user.image
            session['role_id'] = user.role_id

            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))

# Add logout function
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))