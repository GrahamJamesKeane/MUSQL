import pytest
from MUSQL.utils import query_evaluation_tools as qet

def test_keyword_filter():
    query = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    expected_keywords = {'select', 'name', 'age', 'from', 'customers', 'where', '>=', '18', 'order', 'by', 'desc'}
    assert qet.keyword_filter(query) == expected_keywords

def test_check_keywords():
    submission = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    answer = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    assert qet.check_keywords(submission, answer) == qet.KEYWORD_SCORE

def test_check_results_no_columns_match(database_session):
    submission = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    answer = "SELECT name FROM customers WHERE age >= 18 ORDER BY age DESC"
    result = qet.check_results(1, submission, answer, database_session)
    assert result['final_score'] == 0

def test_check_results_full_match(database_session):
    submission = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    answer = "SELECT name, age FROM customers WHERE age >= 18 ORDER BY age DESC"
    result = qet.check_results(1, submission, answer, database_session)

    assert result['final_score'] == qet.RESULT_SCORE
    assert result['individual_scores']['order_score'] == round(qet.ORDER_SCORE_WEIGHT * qet.RESULT_SCORE, qet.PRECISION)
    assert result['individual_scores']['content_score'] == round(qet.CONTENT_SCORE_WEIGHT * qet.RESULT_SCORE, qet.PRECISION)
    assert result['individual_scores']['row_by_row_score'] == round(qet.ROW_SCORE_WEIGHT * qet.RESULT_SCORE, qet.PRECISION)
    assert result['individual_scores']['column_score'] == round(qet.COL_SCORE_WEIGHT * qet.RESULT_SCORE, qet.PRECISION)
