from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models import User, OAuthUser, Project, Task
from routes.auth_routes import auth_blueprint, auth_routes
from routes.project_routes import project_blueprint
from routes.user_routes import user_blueprint
import os


app = Flask(__name__)


app.secret_key = 'your_secret_key'


app.register_blueprint(auth_routes)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)


def register_blueprints(app):

    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # This is where 'auth' blueprint is registered.
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(user_blueprint, url_prefix='/user')


register_blueprints(app)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            print(f"Fetched User: {user.username}, Password: {user.password}")
        else:
            print("User not found.")

        if user and user.password == password:  
            session['user'] = {
                'id': user.uid,
                'username': user.username,
                'email': user.email,
            }
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            new_user = User(username=username, email=email, user_type='manual', password=password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')
                print(e)
    return render_template('login.html', show_register=True)

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    app.logger.info(f"User ID from session: {user['id']}, Type: {type(user['id'])}")

    user_id = int(user['id'])


    projects = Project.query.filter_by(uid=user_id).all()
    for project in projects:
        project.tasks = Task.query.filter_by(project_id=project.pid).all()

    return render_template('dashboard.html', user=user, projects=projects)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = session.get('user')
    if not user:
        flash('Please login to change your password', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
 
        user_in_db = User.query.filter_by(uid=user['id']).first()
        

        if user_in_db and user_in_db.password == old_password:
            if new_password == confirm_password:
                user_in_db.password = new_password
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('New passwords do not match', 'error')
        else:
            flash('Incorrect old password', 'error')
    
    return render_template('change_password.html')


@app.route('/create_task', methods=['POST'])
def create_task():
    project_id = request.form['project']
    title = request.form['title']
    assignee = request.form['assignee']
    due_date = request.form['due_date']
    user = session.get('user')

    if user:
        user_id = user['id']
        
        new_task = Task(
            project_id=project_id,
            user_id=user_id,
            task_description=title,
            due_date=due_date
        )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the task. Please try again.', 'error')
            app.logger.error(f"Error creating task: {e}")
        return redirect(url_for('dashboard'))
    else:
        flash('You must be logged in to create a task', 'error')
        return redirect(url_for('login'))



@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = session.get('user')
    if not user:
        flash('Please login to update your profile', 'error')
        return redirect(url_for('login'))

    username = request.form['username']
    bio = request.form['bio']
    
    user_in_db = User.query.filter_by(uid=user['id']).first()
    user_in_db.username = username
    user_in_db.bio = bio
    db.session.commit()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/chat')
def chat():
    user = session.get('user')
    if not user:
        flash('Please login to access the chat', 'error')
        return redirect(url_for('login'))
    
    return render_template('chat.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
