import os
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, MetaData, Date, text
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from MUSQL.models import Account, Assignment, Result

# Load database credentials from env file
load_dotenv("MUSQL\env\.env")

DB_NAME = 'MUSQL'
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Define database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and metadata
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres")
metadata = MetaData()

# Create MUSQL database if it doesn't exist
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))

# Define the declarative base
Base = declarative_base()

# Create tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add test data
account = Account(student_id='12345678', password='12345678', email='12345678@mumail.ie')
session.add(account)
session.commit()

assignments = [
    Assignment(assignment_name='assignment 1', max_attempts=2, due_date='2023-03-24', duration_mins=90),
    Assignment(assignment_name='assignment 2', max_attempts=2, due_date='2023-04-24', duration_mins=90),
    Assignment(assignment_name='assignment 3', max_attempts=2, due_date='2023-05-24', duration_mins=90),
    Assignment(assignment_name='assignment 4', max_attempts=2, due_date='2023-06-24', duration_mins=90)
]

session.add_all(assignments)
session.commit()

# Insert default rows for test account into results table
test_account = session.query(Account).filter(Account.student_id == '12345678').first()
all_assignments = session.query(Assignment).all()

for assignment in all_assignments:
        result = Result(account_id=test_account.id, assignment_id=assignment.id)
        session.add(result)

session.commit()

# Add postgis extension to MUSQL database
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

# Run external SQL files to build additional tables
sql_files = [
    'CS621-LabExam1-2022-DEMO-TABLE-final.sql',
    'CS621-LabExam2b-Dar-es-Salaam-DEMO-TABLES.sql',
    'LabExam2b-Firenza-2022-INSERTS-TABLES.sql',
    'LabExam12022-Table-SQL.sql.sql',
    'windows_queries_table.sql'
]

# Define the directory containing the SQL files
sql_dir = r"C:\\Users\\18146619\\OneDrive - Maynooth University\\Computer Science\\CS460_Final_Year_Project_2022-23_MH201\\Test_DBs"

# Loop over each SQL file and run it on the database
for sql_file in sql_files:
    print(f"Running SQL file {sql_file}")
    with open(os.path.join(sql_dir, sql_file), 'r') as f:
        print(f"SQL file {sql_file} Open")
        sql = f.read()
    try:
        with engine.connect() as conn:
            print(f"Executing SQL file {sql_file}")
            conn.execute(text(sql))
    except Exception as e:
        print(f"Error running SQL file {sql_file}: {e}")

print("Database created successfully.")
