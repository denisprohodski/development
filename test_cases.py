# from conftest import db_connection
import pymssql
import pytest

@pytest.fixture(scope='session')  # Please verify database credentials
def db_conn():
    server = 'host.docker.internal:1433'
    user = 'DZIANIS_PRAKHODSKI'
    password = '19eo53Q11111'
    db_name = 'TRN'
    with pymssql.connect(server, user, password, db_name) as conn:
        yield conn
        
def test_1_sum_of_column_values(db_conn):
    """" Test Case #1: [hr].[regions] table has sum of region_id column values as expected """
    cursor = db_conn.cursor()
    cursor.execute('SELECT SUM(region_id) FROM [hr].[regions]')
    actual_result = cursor.fetchone()[0]
    expected_result = 10
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()

def test_2_null_of_column_values(db_conn):
    """" Test Case #2: [hr].[regions] table has not NULL values in region_name column """
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM [hr].[regions] WHERE [region_name] IS NULL;')
    actual_result = cursor.fetchone()
    assert actual_result is None, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()

def test_3_spec_of_column_values(db_conn):
    """" Test Case #3: [hr].[employees] table has at least @ and dot after @ (e.g sss@mail.com, sss@@mail.cob - valid, ss@mm - not valid) """
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM [hr].[employees] WHERE [email] NOT LIKE '%@%.%';")
    actual_result = cursor.fetchone()
    assert actual_result is None, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()

def test_4_max_value_of_column_salary(db_conn):
    """" Test Case #4: [hr].[employees] table has MAX value of salary column values as expected """
    cursor = db_conn.cursor()
    cursor.execute('SELECT MAX([salary]) FROM [hr].[employees];')
    actual_result = cursor.fetchone()[0]
    expected_result = 24000
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()

def test_5_count_rows_for_department_table(db_conn):
    """" Test Case #5: Count of rows of [hr].[departments] table is as expected."""
    cursor = db_conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM [hr].[departments];')
    actual_result = cursor.fetchone()[0]
    expected_result = 11
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()

def test_6_referential_integrity_for_location_id_column_for_departments_table(db_conn):
    """" Test Case #6: Referential integrity for location_id(FK) column of [hr].[departments] table."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT d.location_id FROM [hr].[departments] d "
                   "LEFT JOIN [hr].[locations] l ON d.location_id=l.location_id "
                   "WHERE l.location_id IS NULL")
    actual_result = cursor.fetchone()
    assert actual_result is None, f"Expected {expected_result}, but got {actual_result} instead"
    cursor.close()
