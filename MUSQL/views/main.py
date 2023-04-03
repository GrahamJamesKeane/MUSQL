# Standard library imports
import json
import os

# Third-party imports
from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)

# Local imports
from MUSQL.models import Account, Result
import MUSQL.utils.application_tools as at

bp = Blueprint('musql', __name__, url_prefix='/musql')

@bp.route('/home', methods=('GET', 'POST'))
def home():
    from flask import current_app
    db = current_app.db
    if 'loggedin' in session:
        grades = [x[0] for x in db.session.execute(at.join_builder(
            'grade', 'results', 'assignments', 'accounts', 'id', 'assignment_id', 'account_id ', session['id']))]
        assignments = []
        for filename in os.listdir('MUSQL/static/assignments'):
            with open(os.path.join('MUSQL/static/assignments', filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                assignments.append(data)
        access, attempts = at.check_attempts(assignments)
        return render_template('musql/home.html', user_id=session['user_id'], assignments=assignments, access=access, grades=grades, attempts=attempts)
    return redirect(url_for('auth.login'))

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    if 'loggedin' in session:
        user_account = Account.query.filter_by(id=session['id']).first()
        grades = Result.query.filter_by(account_id=session['id']).order_by(Result.assignment_id).all()
        return render_template('musql/profile.html', account=user_account, grades=grades)
    return redirect(url_for('auth.login'))

@bp.route('/assignments/<int:assignment_number>', methods=('GET', 'POST'))
def view_assignment(assignment_number):
    assignment_data = at.load_assignment_data(assignment_number)
    questions = assignment_data['questions']
    access = at.check_attempt(assignment_number, assignment_data['max_attempts'])
    start_timer = request.method != 'POST'
    grade = None

    if request.method == 'POST':
        grade = at.process_assignment_submission(assignment_data, questions)
    elif not access:
        grade = at.load_saved_grade(assignment_number)

    return render_template('musql/assignment.html', assignment_data=assignment_data, assignment_number=assignment_number, grade=grade, access=access, start_timer=start_timer)