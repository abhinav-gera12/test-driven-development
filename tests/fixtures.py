import pytest
from tests.utils.docker_utils import start_database_container
from sqlalchemy import create_engine
from tests.utils.database_utils import migrate_to_db

@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_database_container()
    
    TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5434/inventory"
    engine = create_engine(TEST_DATABASE_URL)
    
    
    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)
        
    # container.stop()
    # container.remove()