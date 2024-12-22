from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models import User, OAuthUser, Project, Task, Comment, ConnectionRequest, Chat, Post
from routes.auth_routes import auth_blueprint, auth_routes
from routes.project_routes import project_blueprint
from routes.user_routes import user_blueprint
import os
from datetime import datetime

# from routes.google_routes import google_blueprint


app = Flask(__name__)


app.secret_key = 'your_secret_key'


# app.register_blueprint(google_blueprint, url_prefix="/google")

app.register_blueprint(auth_routes)



# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toti10102024@localhost:5432/colonydb'
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user', {}).get('id')
    if not user_id:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('login'))

    # Fetch projects and tasks
    projects = Project.query.filter_by(uid=user_id).all()
    for project in projects:
        project.tasks = Task.query.filter_by(project_id=project.pid).all()
        for task in project.tasks:
            task.comments = Comment.query.filter_by(task_id=task.task_id).all()  # Fetch comments for each task

    return render_template('dashboard.html', user=session['user'], projects=projects)



@app.route('/news_feed', methods=['GET', 'POST'])
def news_feed():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_post = Post(user_id=user['id'], content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added successfully!', 'success')
        else:
            flash('Post content cannot be empty.', 'error')

    # Fetch all posts, ordered by creation time
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('news_feed.html', user=user, posts=posts)



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

@app.route('/search_users', methods=['GET'])
def search_users():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    users = User.query.filter(User.username.ilike(f'%{query}%')).all()
    return jsonify([{'id': user.uid, 'username': user.username} for user in users])



@app.route('/search_members', methods=['GET', 'POST'])
def search_members():
    query = ''
    members = []

    if request.method == 'POST':
        query = request.form.get('query', '').strip()  # Get the search query from the form
        if query:
            # Perform a case-insensitive search using ilike
            members = User.query.filter(User.username.ilike(f"%{query}%")).all()
        else:
            # Return all members if no query is provided
            members = User.query.all()

    return render_template('search_members.html', query=query, members=members)


@app.route('/send_connection_request', methods=['POST'])
def send_connection_request():
    sender_id = session['user']['id']
    receiver_username = request.form.get('member_username')
    receiver = User.query.filter_by(username=receiver_username).first()

    if receiver:
        # Check if a request already exists
        existing_request = ConnectionRequest.query.filter_by(sender_id=sender_id, receiver_id=receiver.uid).first()
        if existing_request:
            flash('You have already sent a connection request to this user.', 'info')
        else:
            # Create a new connection request
            new_request = ConnectionRequest(sender_id=sender_id, receiver_id=receiver.uid)
            db.session.add(new_request)
            db.session.commit()
            flash(f'Connection request sent to {receiver.username}!', 'success')

    return redirect(url_for('search_members'))

# View Connection Requests
@app.route('/view_requests', methods=['GET', 'POST'])
def view_requests():
    user_id = session.get('user', {}).get('id')  # Get the logged-in user's ID

    if not user_id:
        flash('You need to log in to view connection requests.', 'error')
        return redirect(url_for('login'))

    # Fetch pending connection requests
    requests = ConnectionRequest.query.filter_by(receiver_id=user_id, status='pending').all()

    if request.method == 'POST':
        request_id = request.form.get('request_id')
        action = request.form.get('action')  # 'accept' or 'reject'

        if not request_id or not action:
            flash('Invalid request. Missing information.', 'error')
            return redirect(url_for('view_requests'))

        connection_request = ConnectionRequest.query.filter_by(id=request_id, receiver_id=user_id).first()
        if connection_request:
            if action == 'accept':
                # Mark the request as accepted
                connection_request.status = 'accepted'

                # Create a reverse connection request to establish two-way connection
                reverse_request = ConnectionRequest.query.filter_by(
                    sender_id=user_id, receiver_id=connection_request.sender_id
                ).first()
                if not reverse_request:
                    reverse_request = ConnectionRequest(
                        sender_id=user_id,
                        receiver_id=connection_request.sender_id,
                        status='accepted'
                    )
                    db.session.add(reverse_request)

                flash(f"You have accepted the connection request from {connection_request.sender.username}.", 'success')
            elif action == 'reject':
                connection_request.status = 'rejected'
                flash(f"You have rejected the connection request from {connection_request.sender.username}.", 'info')
            else:
                flash('Invalid action.', 'error')
                return redirect(url_for('view_requests'))
            
            db.session.commit()
        else:
            flash('Connection request not found or already handled.', 'error')

        return redirect(url_for('view_requests'))

    return render_template('view_requests.html', requests=requests)



@app.route('/accept_request', methods=['POST'])
def accept_request():
    user_id = session.get('user', {}).get('id')  # Ensure the user is logged in
    if not user_id:
        flash("You need to log in to perform this action.", "error")
        return redirect(url_for('login'))

    request_id = request.form.get('request_id')
    connection_request = ConnectionRequest.query.filter_by(id=request_id, receiver_id=user_id).first()

    if connection_request:
        connection_request.status = 'accepted'
        db.session.commit()
        flash("Connection request accepted.", "success")
    else:
        flash("Invalid connection request.", "error")

    return redirect(url_for('view_requests'))


@app.route('/reject_request', methods=['POST'])
def reject_request():
    user_id = session.get('user', {}).get('id')  # Ensure the user is logged in
    if not user_id:
        flash("You need to log in to perform this action.", "error")
        return redirect(url_for('login'))

    request_id = request.form.get('request_id')
    connection_request = ConnectionRequest.query.filter_by(id=request_id, receiver_id=user_id).first()

    if connection_request:
        connection_request.status = 'rejected'
        db.session.commit()
        flash("Connection request rejected.", "info")
    else:
        flash("Invalid connection request.", "error")

    return redirect(url_for('view_requests'))




@app.route('/create_task', methods=['POST'])
def create_task():
    if request.method == 'POST':
        project_id = request.form.get('project')
        task_description = request.form.get('title')
        due_date = request.form.get('due_date')
        assignee_username = request.form.get('assignee')  # Username from input

        if not project_id or not task_description or not assignee_username:
            flash("All fields are required!", "error")
            return redirect(url_for('dashboard'))

        # Find the user by username
        assignee = User.query.filter_by(username=assignee_username).first()
        if not assignee:
            flash("Assignee not found!", "error")
            return redirect(url_for('dashboard'))

        try:
            # Create and save the task
            new_task = Task(
                project_id=project_id,
                task_description=task_description,
                due_date=due_date,
                user_id=assignee.uid  # Assign task to user ID
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Task created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating task: {e}", "error")

        return redirect(url_for('dashboard'))




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





@app.route('/chat/<username>', methods=['GET', 'POST'])
def chat(username):
    user_id = session.get('user', {}).get('id')  # Safely get the logged-in user ID

    if not user_id:
        flash("You need to log in to access the chat.", "error")
        return redirect(url_for('login'))

    # Fetch all connected users (users with an accepted connection request)
    connected_users = User.query.join(
        ConnectionRequest,
        (ConnectionRequest.sender_id == User.uid) | (ConnectionRequest.receiver_id == User.uid)
    ).filter(
        ((ConnectionRequest.receiver_id == user_id) | (ConnectionRequest.sender_id == user_id)),
        ConnectionRequest.status == 'accepted'
    ).distinct().all()

    # Handle 'default' username or invalid username
    if username == 'default' and connected_users:
        return redirect(url_for('chat', username=connected_users[0].username))
    elif username == 'default':
        flash("No connected users found.", "error")
        return redirect(url_for('dashboard'))

    # Ensure a valid user is selected
    receiver = User.query.filter_by(username=username).first()
    if not receiver:
        flash("User not found.", "error")
        return redirect(url_for('dashboard'))

    # Ensure the receiver is in the connected users list
    if receiver.uid not in [user.uid for user in connected_users]:
        flash("You are not connected with this user.", "error")
        return redirect(url_for('dashboard'))

    # Fetch chat messages between the logged-in user and the selected receiver
    chats = Chat.query.filter(
        ((Chat.sender_id == user_id) & (Chat.receiver_id == receiver.uid)) |
        ((Chat.sender_id == receiver.uid) & (Chat.receiver_id == user_id))
    ).order_by(Chat.timestamp).all()

    # Handle sending messages
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if message:
            new_chat = Chat(
                sender_id=user_id,
                receiver_id=receiver.uid,
                message=message,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_chat)
            db.session.commit()
        return redirect(url_for('chat', username=username))

    return render_template(
        'chat.html',
        connected_users=connected_users,
        receiver=receiver.username,
        chats=chats
    )




@app.route('/faqs', methods=['GET'])
def faqs():
    faqs_list = [
        {"question": "How do I create a project?", "answer": "Go to the Dashboard and click on 'Create Project'."},
        {"question": "How do I reset my password?", "answer": "Go to 'Change Password' under your profile settings."},
        {"question": "Can I delete a task?", "answer": "Currently, deleting tasks is not supported, but you can update or archive them."},
        {"question": "How do I update the priority of a task?", "answer": "Open the task details and select a new priority from the dropdown menu, then click 'Update Priority'."},
        {"question": "How do I assign a task to a user?", "answer": "While creating a task, use the 'Search Assignee' field to assign the task to a user."},
        {"question": "What happens if I don't assign a task?", "answer": "Tasks without an assignee are not linked to any user and remain in the project unassigned."},
        {"question": "How do I upload a file?", "answer": "Go to the 'File Upload' section in the sidebar, choose your file, and click 'Upload'."},
        {"question": "Can I change my profile picture?", "answer": "Yes, go to your profile page and use the 'Update Profile Picture' option."},
        {"question": "How do I view all tasks assigned to me?", "answer": "Go to your profile page, where all tasks assigned to you are listed under 'Assigned Tasks'."},
        {"question": "How do I create a task within a project?", "answer": "Go to the Dashboard, select a project, and click on 'Create Task'."},
        {"question": "Can I create subtasks?", "answer": "Currently, subtasks are not supported, but you can create separate tasks for different components."},
        {"question": "What is the News Feed?", "answer": "The News Feed displays posts shared by all users on the platform."},
        {"question": "How do I post something in the News Feed?", "answer": "Navigate to the News Feed and use the 'Write a post' section to share your message."},
        {"question": "How do I log out?", "answer": "Click on the 'Logout' button in the sidebar to securely log out of your account."},
        {"question": "What do I do if I encounter a bug?", "answer": "Please contact support with a description of the bug and any screenshots if possible."},
        {"question": "Can I change the due date of a task?", "answer": "Yes, open the task details and update the due date field."},
        {"question": "How do I edit a project description?", "answer": "Currently, project descriptions cannot be edited once created."},
        {"question": "How do I see who created a task?", "answer": "The creator of a task is not explicitly displayed at this time."},
        {"question": "How do I contact support?", "answer": "You can email support at support@yourplatform.com or use the contact form in the Help section."},
        {"question": "Can I filter tasks by priority?", "answer": "Currently, filtering tasks by priority is not supported but may be included in future updates."}
    ]
    return render_template('faqs.html', faqs=faqs_list)





@app.route('/add_comment', methods=['POST'])
def add_comment():
    user_id = session.get('user', {}).get('id')
    if not user_id:
        flash("Please log in to add a comment.", "error")
        return redirect(url_for('dashboard'))

    task_id = request.form.get('task_id')
    comment_text = request.form.get('comment_text', '').strip()

    if not task_id or not comment_text:
        flash("Task ID and comment text are required.", "error")
        return redirect(url_for('dashboard'))

    task = Task.query.get(task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for('dashboard'))

    new_comment = Comment(task_id=task_id, user_id=user_id, comment_text=comment_text)
    db.session.add(new_comment)
    db.session.commit()

    flash("Comment added successfully!", "success")
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
