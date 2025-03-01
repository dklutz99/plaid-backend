from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 🔹 Load environment variables from .env file
load_dotenv()

# 🔹 Get the database URL from .env file
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://plaid_user:your_secure_password@localhost:5432/plaid_db")

# 🔹 Set up SQLAlchemy database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔹 Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
