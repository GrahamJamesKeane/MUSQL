import os
import tempfile

import pytest
from MUSQL import create_app
from MUSQL.utils.database import db

# Import necessary components from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def app():
    # Use a temporary file for the test database URL
    db_fd, db_path = tempfile.mkstemp()
    db_url = f"sqlite:///{db_path}"

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        # Create all tables for the test database
        db.Model.metadata.create_all(db.engine)

    yield app, db  # Add 'db' to the yield statement

     # Close the database connection
    db.session.close()
    db.engine.dispose()

    # Close and remove the test database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def app_db(app, db):
    return app, db

@pytest.fixture
def client(app_db):
    app, db = app_db  # Unpack 'app' and 'db' from the tuple
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def session(app_db):
    app, db = app_db  # Unpack 'app' and 'db' from the tuple
    connection = db.engine.connect()
    transaction = connection.begin()

    # Bind the session to the connection and start the test
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session

    # Roll back the transaction and close the session after the test
    transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture(scope="module")
def database_session(app_db):
    app, db = app_db  # Unpack 'app' and 'db' from the tuple
    with app.app_context():
        db.create_all()
        yield db.session
        db.drop_all()


class AuthActions(object):
    def __init__(self, client, session):
        self._client = client
        self._session = session

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client, session):
    return AuthActions(client, session)