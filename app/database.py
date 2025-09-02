from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///./rides.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
