from sqlalchemy import create_engine, text

# Replace with your connection string (without sensitive information)
connection_string = "postgresql://postgres:dev@localhost:5432/MUSQL"

engine = create_engine(connection_string)

def test_database_response_time(timeout=5):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1").execution_options(timeout=timeout))
            print("Result:", result.fetchall())
            return "Database response time is acceptable."
    except Exception as e:
        return f"Error: {e}"

print(test_database_response_time())
