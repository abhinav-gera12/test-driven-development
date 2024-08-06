import pytest
from tests.utils.docker_utils import start_database_container
from sqlalchemy import create_engine
from tests.utils.database_utils import migrate_to_db
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_database_container()
    
    TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5434/inventory"
    engine = create_engine(TEST_DATABASE_URL)
    
    
    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)
        
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    yield SessionLocal
            
    # container.stop()
    # container.remove()
    engine.dispose()