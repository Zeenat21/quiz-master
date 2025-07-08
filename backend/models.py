from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Association table for roles and users
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow) 
    
    active = db.Column(db.Boolean(), default=True)
    # confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    scores = db.relationship('Score', backref='user', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship('Chapter', backref='subject', lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    quizzes = db.relationship('Quiz', backref='chapter', lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    date_of_quiz = db.Column(db.Date)
    time_duration = db.Column(db.String(5))  # Format: HH:MM
    remarks = db.Column(db.String(255))

    questions = db.relationship('Question', backref='quiz', lazy=True,cascade="all, delete-orphan", passive_deletes=True)
    scores = db.relationship('Score', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # 1 to 4

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) #to capture submit
    total_score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float)
    correct_answers = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)

# class CSVExportStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     export_type = db.Column(db.String(50))  # 'user' or 'admin'
#     status = db.Column(db.String(20), default='pending')  # pending/completed/failed
#     file_path = db.Column(db.String(255))
#     requested_at = db.Column(db.DateTime, default=datetime.utcnow)
#     completed_at = db.Column(db.DateTime)

# class ReminderLog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     type = db.Column(db.String(50))  # 'daily', 'monthly'
#     sent_at = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(50), default='sent')  # sent/failed

