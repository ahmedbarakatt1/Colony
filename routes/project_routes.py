from flask import Blueprint, request, session, redirect, url_for, flash
from extensions import db
from models import Project, Task
from datetime import datetime

project_blueprint = Blueprint('project', __name__)


@project_blueprint.route('/create_task', methods=['POST'])
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



@project_blueprint.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form['project_name']
    project_description = request.form['project_description']
    user = session.get('user')  

    if user and project_name:
        user_id = int(user['id'])  
        new_project = Project(
            pname=project_name,
            description=project_description,
            start_date=datetime.utcnow().date(),
            uid=user_id
        )
        try:
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            print(f"Error creating project: {e}")  
    else:
        flash('Failed to create project', 'error')
    return redirect(url_for('dashboard'))


@project_blueprint.route('/update_task_status', methods=['POST'])
def update_task_status():
    project_id = request.form.get('project_id')
    task_id = request.form.get('task_id')
    status = request.form.get('status')

    if task_id and status:
        task = Task.query.get(task_id)
        if task:
            task.status = status
            try:
                db.session.commit()
                flash('Task status updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Failed to update task status.', 'error')
                print(e)
        else:
            flash('Task not found.', 'error')
    else:
        flash('Invalid input. Please try again.', 'error')

    return redirect(url_for('dashboard'))

@project_blueprint.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        try:
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save(upload_path)
            flash('File uploaded successfully!', 'success')
        except Exception as e:
            flash('An error occurred while uploading the file.', 'error')
            print(e)
    else:
        flash('No file selected for upload.', 'error')
    return redirect(url_for('project.dashboard'))

@project_blueprint.route('/add_comment', methods=['POST'])
def add_comment():
    task_id = request.form['task_id']
    comment_text = request.form['comment_text']
    user = session.get('user')
    
    if not user:
        flash('You must be logged in to add a comment', 'error')
        return redirect(url_for('login'))
    
    user_id = user['id']
    new_comment = Comment(task_id=task_id, user_id=user_id, comment_text=comment_text)
    
    try:
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'error')
        print(e)
    
    return redirect(url_for('dashboard'))
@project_blueprint.route('/update_priority', methods=['POST'])
def update_priority():
    task_id = request.form['task_id']
    priority = request.form['priority']
    
    task = Task.query.get(task_id)
    if task:
        task.priority = priority
        try:
            db.session.commit()
            flash('Task priority updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update task priority.', 'error')
            print(e)
    else:
        flash('Task not found.', 'error')
    
    return redirect(url_for('dashboard'))
