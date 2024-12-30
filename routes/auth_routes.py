from flask import Blueprint, redirect, request, session, url_for, flash, render_template, jsonify
import requests
from config import Config
from models import OAuthUser, User
from extensions import db

auth_blueprint = Blueprint('auth', __name__)
auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return render_template('change_password.html', message="All fields are required.", message_type="error")

        if new_password != confirm_password:
            return render_template('change_password.html', message="Passwords do not match.", message_type="error")

        user_id = session.get('user', {}).get('id')  
        if not user_id:
            return render_template('change_password.html', message="User not logged in.", message_type="error")

        user = User.query.get(user_id)
        if not user:
            return render_template('change_password.html', message="User not found.", message_type="error")

        if not user.check_password(old_password):
            return render_template('change_password.html', message="Old password is incorrect.", message_type="error")

        user.set_password(new_password)
        try:
            db.session.commit()
            return render_template('change_password.html', message="Password updated successfully!", message_type="success")
        except Exception as e:
            db.session.rollback()
            return render_template('change_password.html', message=f"An error occurred: {e}", message_type="error")


@auth_blueprint.route('/login')
def login():

    auth_url = (
        f"{Config.AUTH_URL}?response_type=code&client_id={Config.CLIENT_ID}"
        f"&redirect_uri={Config.REDIRECT_URI}&scope=email profile&access_type=offline"
    )
    return redirect(auth_url)


@auth_blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        flash("Authorization failed. Please try again.", "error")
        return redirect(url_for('auth.login'))

  
    token_response = requests.post(
        Config.TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Config.REDIRECT_URI,
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
        }
    ).json()

    access_token = token_response.get('access_token')
    if not access_token:
        flash("Failed to retrieve access token. Please try again.", "error")
        return redirect(url_for('auth.login'))

  
    user_info = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    if 'error' in user_info or 'email' not in user_info:
        flash("Failed to retrieve user information. Please try again.", "error")
        return redirect(url_for('auth.login'))


    session['user'] = {
        'id': user_info['id'],
        'email': user_info['email'],
        'name': user_info.get('name', ''),
        'picture': user_info.get('picture', '')
    }

    oauth_user = OAuthUser.query.filter_by(oauth_id=user_info['id']).first()
    if not oauth_user:
        new_oauth_user = OAuthUser(
            oauth_provider='google',
            oauth_id=user_info['id'],
            profile_picture=user_info.get('picture', ''),
            given_name=user_info.get('given_name', ''),
            family_name=user_info.get('family_name', ''),
        )
        try:
            db.session.add(new_oauth_user)
            db.session.commit()
            flash('OAuth user successfully registered!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while storing the OAuth user. Please try again.', 'error')

    flash('Login successful!', 'success')
    return redirect(url_for('dashboard'))
