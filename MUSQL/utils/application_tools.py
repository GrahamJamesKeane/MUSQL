import json
from MUSQL.models import Result, Assignment
from sqlalchemy import text
from flask import request, session
from MUSQL.utils.grading_engine import evaluate_submission


def join_builder(col, table_1, table_2, table_3, col_a, col_b, col_c, s_id):
    return text(f"""
        SELECT {col} 
        from {table_1} a
        join {table_2} b on b.{col_a} = a.{col_b} 
        join {table_3} c on c.{col_a} = a.{col_c}
        WHERE c.id = {s_id}
        ORDER BY a.{col_b} ASC;
        """)


def check_attempts(assignments):
    attempts = [Result.query.filter(Result.account_id == session['id'], Result.assignment_id ==
                                    assignment['assignment_number']).first().num_attempts for assignment in assignments]
    return [attempt < assignment['max_attempts'] for attempt, assignment in zip(attempts, assignments)], attempts


def check_attempt(assignment_number, max_attempts):
    attempt = Result.query.filter(
        Result.account_id == session['id'], Result.assignment_id == assignment_number).first().num_attempts
    return attempt < max_attempts


def process_assignment_submission(assignment_data, questions):
    from flask import current_app
    db = current_app.db
    result = Result.query.filter(
        Result.account_id == session['id'], Result.assignment_id == request.form['assignment_id']).first()
    result.num_attempts += 1
    db.session.commit()
    
    student_answers = {
        "student_number": session['user_id'],
        "assignment_number": request.form['assignment_id'],
        "queries": [request.form[f"answer_{i}"] for i in range(1, len(questions) + 1)]
    }
    
    grade = evaluate_submission(assignment_data, student_answers)

    result.submission_data = json.dumps(grade)

    result.grade = grade['total']

    db.session.commit()

    return grade


def load_assignment_data(assignment_number):
    assignment_file = f"assignment_{assignment_number}.json"
    with open(f"MUSQL/static/assignments/{assignment_file}", encoding='utf-8') as f:
        assignment_data = json.load(f)
    return assignment_data


def load_saved_grade(assignment_number):
    """
    Load the grade data for the specified assignment number from the database.

    Args:
        assignment_number (int): The assignment number to load the grade data for.

    Returns:
        grade (dict): A dictionary containing the grade data for the specified assignment number, or None if no grade is found.
    """
    assignment = Assignment.query.filter_by(
        assignment_name=f"assignment {assignment_number}").first()
    result = Result.query.filter_by(
        assignment_id=assignment.id, account_id=session['id']).first()
    if result is not None:
        submission_data = json.loads(result.submission_data)
        grade = {
            "student_number": submission_data['student_number'],
            "assignment_number": submission_data['assignment_number'],
            "total": submission_data['total'],
            "query_grades": submission_data['query_grades'],
            "account_id": result.account_id,
            "assignment_id": result.assignment_id,
            "num_attempts": result.num_attempts,
            "grade": result.grade
        }
        return grade
    return None
