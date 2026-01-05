from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///habits.db"

# check_same_thread is required for SQLite with multiple threads in FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
