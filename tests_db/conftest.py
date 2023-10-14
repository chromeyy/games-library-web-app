import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "games" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///games-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Create db tables
    for table in reversed(metadata.sorted_tables):  # clear tables
        engine.execute(table.delete())
    map_model_to_tables()
    # Creating db session
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # creating SQLAlchemy db repo instance .
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Creating db session factory
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Creating SQLAlchemy dbrepo instance
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_FULL, repo_instance, database_mode)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers() # clearing mappers
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables() # mapping
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)