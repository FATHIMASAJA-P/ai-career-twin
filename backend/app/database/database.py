import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_twin.db.migrated")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def add_missing_columns():
    inspector = inspect(engine)

    if "activities" in inspector.get_table_names():
        activity_columns = {
            column["name"] for column in inspector.get_columns("activities")
        }

        if "career_roadmap" not in activity_columns:
            with engine.begin() as connection:
                connection.execute(
                    text("ALTER TABLE activities ADD COLUMN career_roadmap TEXT")
                )


# 👇 Add this function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()