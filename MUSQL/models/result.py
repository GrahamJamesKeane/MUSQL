from MUSQL.utils.database import db

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    num_attempts = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    submission_data = db.Column(db.JSON, nullable=True)
