from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import UserLoginForm
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets  # For token generation if needed

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            hashed_password = generate_password_hash(password)
            user_token = secrets.token_hex(16)  # Generate a token if your system uses it
            user = User(email=email, password=hashed_password, token=user_token)  # Save the token
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('auth.signin'))
        else:
            flash('Email already exists. Please log in.', 'danger')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('site.profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
