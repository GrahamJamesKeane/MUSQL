from .database import db

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String, unique=True, nullable=False)
    max_attempts = db.Column(db.Integer, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    duration_mins = db.Column(db.Integer, nullable=False)