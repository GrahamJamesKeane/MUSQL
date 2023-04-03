import re
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

SYNTAX_SCORE = 20
KEYWORD_SCORE = 20
RESULT_SCORE = 60

ORDER_SCORE_WEIGHT = 0.25
CONTENT_SCORE_WEIGHT = 0.25
ROW_SCORE_WEIGHT = 0.25
COL_SCORE_WEIGHT = 0.25

PRECISION = 2

def keyword_filter(query):
    """
    Extracts all keywords from the given SQL query and returns them as a set.

    Args:
    - query (str): The SQL-like query to extract keywords from.

    Returns:
    - A set containing all keywords found in the query.

    Example:
    >>> keyword_filter("SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC")
    {'select', 'name', 'age', 'from', 'customers', 'where', '>=', '18', 'order', 'by', 'desc'}
    """
    pattern = r'(\w{2,}|\d+\.\d+|~|~\*|\s\*|=|<=|>=|!=)'
    return set(re.findall(pattern, query.lower()))

def evaluate_query_syntax(query):
    """
    Checks the syntax of a SQL query using the EXPLAIN command.

    Args:
        query (str): the SQL query to check the syntax of.
        session (Session): the SQLAlchemy session object.

    Returns:
        A list of two elements: the syntax score (either SYNTAX_SCORE or 0) and either None or a list of error messages
        (if syntax is incorrect).
    """
    from flask import current_app
    db = current_app.db
    try:
        db.session.execute(text(f"EXPLAIN {query}"))
        return [SYNTAX_SCORE, None]
    except Exception as e:
        error = str(e).split("\n")
        output = [item.strip() for item in error if "LINE" not in item and "^" not in item and item != ""]
        db.session.rollback()
        return [0, output]
    
def evaluate_submission_keywords(submission, answer):
    """
    Checks the user submission against the correct answer to see how many keywords match.

    Args:
    submission (str): The user's SQL submission
    answer (str): The correct SQL query answer

    Returns:
    float: The percentage of correct keywords in the user submission, multiplied by KEYWORD_SCORE
    """
    user_keywords = keyword_filter(submission)
    answer_keywords = keyword_filter(answer)
    num_correct = len(user_keywords & answer_keywords)
    return round((num_correct / len(answer_keywords)) * KEYWORD_SCORE, PRECISION)

def evaluate_result_data(index, submission, answer):
    """Checks the correctness of a user submission by comparing its result set against the expected one.

    Args:
        index (int): The index of the question being evaluated.
        submission (str): The SQL query submitted by the user.
        answer (str): The SQL query that generates the expected result set.
        session (Session): The SQLAlchemy session object.

    Returns:
        dict: The final score and a dictionary containing individual scores.
    """
    from flask import current_app
    db = current_app.db
    scoring = {
        'final_score': 0,
        'individual_scores': {'order_score': 0, 'content_score': 0, 'row_by_row_score': 0, 'column_score': 0}
    }
    try:
        user_rows = db.session.execute(text(submission))
        user_columns = [col for col in user_rows.keys()]
        correct_rows = db.session.execute(text(answer))
        correct_columns = [col for col in correct_rows.keys()]
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error in query syntax (Question {index}): {e}")
        return scoring

    column_score = int(user_columns == correct_columns)
    if column_score == 0:
        return scoring
    user_results = user_rows.fetchall()
    correct_results = correct_rows.fetchall()
    order_score = 1 if len(user_results) > 0 else 0
    row_by_row_score = 0
    for s_row, c_row in zip(user_results, correct_results):
        if s_row == c_row:
            row_by_row_score += 1
        else:
            order_score = 0
    len_correct_rows = len(correct_results)
    row_by_row_score /= len_correct_rows
    content_score = len(set(user_results).intersection(
        set(correct_results))) / len_correct_rows

    final_column_score = round(column_score * COL_SCORE_WEIGHT * RESULT_SCORE, PRECISION)
    final_order_score = round(order_score * ORDER_SCORE_WEIGHT * RESULT_SCORE, PRECISION)
    final_row_by_row_score = round(row_by_row_score * ROW_SCORE_WEIGHT * RESULT_SCORE, PRECISION)
    final_content_score = round(content_score * CONTENT_SCORE_WEIGHT * RESULT_SCORE, PRECISION)

    scoring['final_score'] = round(final_column_score + final_content_score + final_row_by_row_score + final_order_score, PRECISION)
    scoring['individual_scores'] = {'order_score': final_order_score, 'content_score': final_content_score,
                                    'row_by_row_score': final_row_by_row_score, 'column_score': final_column_score}
    return scoring

def calculate_grade(query, syntax, keywords, results):
    """
    Calculate the grade for a given SQL query based on its syntax, keyword usage, and results.

    Args:
    - query (str): The SQL query submitted by the user.
    - syntax (int or list): The syntax score for the query, or a list containing the score and any feedback.
    - keywords (float): The keyword score for the query.
    - results (dict): The results scoring dictionary for the query.

    Returns:
    - A dictionary containing the query, feedback (if any), syntax score, keyword score, results score, individual scores, and the total grade for the query.
    """
    syntax_score = syntax if type(syntax) == int else syntax[0]
    feedback = None if type(syntax) == int else syntax[1]
    results_score = results if type(results) == int else results['final_score']
    total_score = syntax_score + keywords + results_score

    return {
        "query": query,
        "feedback": feedback,
        "syntax": syntax_score,
        "keywords": keywords,
        "results": results_score,
        "order_score": 0 if type(results) == int else results['individual_scores']['order_score'],
        "content_score": 0 if type(results) == int else results['individual_scores']['content_score'],
        "row_by_row_score": 0 if type(results) == int else results['individual_scores']['row_by_row_score'],
        "column_score": 0 if type(results) == int else results['individual_scores']['column_score'],
        "query_total": round(total_score, PRECISION)
    }

def evaluate_submission(assignment, submission):
    """
    Checks the user's queries against the instructor's answers for an assignment and returns the user's grade.

    Parameters:
    - assignment (dict): A dictionary representing an assignment with questions and answers.
    - submission (dict): A dictionary representing a user's submission with queries and user number.
    - session (Session): A session object for making database queries.

    Returns:
    - user_grade (dict): A dictionary containing the user's grade for the assignment with total and query grades.
                            The query grades is a list of dictionaries containing the grade for each query.
                            Each query grade dictionary contains keys for 'query', 'feedback', 'syntax', 'keywords',
                            'results', and 'query_total'.
    """

    instructor_queries = [question["answer"]
                          for question in assignment["questions"]]
    user_queries = submission["queries"]

    user_grade = {
        "student_number": submission["student_number"],
        "assignment_number": submission["assignment_number"],
        "total": 0,
        "query_grades": []
    }

    for index, (query, answer) in enumerate(zip(user_queries, instructor_queries), start=1):
        syntax, keywords, results = 0, 0, 0
        if len(query) != 0:
            rebuilt_answer = "".join(answer)
            syntax = evaluate_query_syntax(query)
            keywords = evaluate_submission_keywords(query, rebuilt_answer)
            if syntax[0] != 0:
                results = evaluate_result_data(index, query, rebuilt_answer)
        grade = calculate_grade(query, syntax, keywords, results)
        user_grade["total"] += grade["query_total"]
        user_grade["query_grades"].append(grade)

    user_grade["total"] = round(
        user_grade["total"] / (len(user_queries) * 100) * 100, 2)
    return user_grade