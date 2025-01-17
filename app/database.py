# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./books.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = 'sqlite:///./books.db'

# Create the SQLAlchemy engine and session maker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # for SQLite in multi-threaded apps
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Check Database Connection
def check_db_connection():
    try:
        # Attempt to connect to the database by querying a sample table or performing a simple query
        session = SessionLocal()
        # Test connection with a simple query, wrapped with text()
        result = session.execute(text("SELECT 1"))
        logger.info("Database connected successfully!")
        session.close()
    except SQLAlchemyError as e:
        logger.error(f"Error connecting to database: {e}")

# Run the check_db_connection function when the script is executed directly
if __name__ == "__main__":
    check_db_connection()

