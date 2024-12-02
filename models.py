from datetime import datetime
from extensions import db
from sqlalchemy import BigInteger


class User(db.Model):
    __tablename__ = 'users'
    
    uid = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    user_type = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=True)

    def set_password(self, new_password):
        """
        Update the user's password. Currently, no hashing is applied.
        """
        self.password = new_password

    def check_password(self, password):
        """
        Verify if the provided password matches the stored one.
        """
        return self.password == password
class OAuthUser(db.Model):
    __tablename__ = 'oauth_users'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid', ondelete='CASCADE'), primary_key=True)
    oauth_provider = db.Column(db.String(255), nullable=False)
    oauth_id = db.Column(db.String(255), nullable=False, unique=True)
    profile_picture = db.Column(db.Text)
    given_name = db.Column(db.String(255))
    family_name = db.Column(db.String(255))


class Project(db.Model):
    __tablename__ = 'project_table'
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    uid = db.Column(db.BigInteger, db.ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)


class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_table.pid', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OAuthToken(db.Model):
    __tablename__ = 'oauth_tokens'
    oid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.uid', ondelete='CASCADE'), nullable=False
    )
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text)
    token_type = db.Column(db.String(50))
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scope = db.Column(db.Text)
