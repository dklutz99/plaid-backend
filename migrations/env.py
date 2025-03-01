import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from models import Base  # ✅ Import your SQLAlchemy models

# Load Alembic configuration
config = context.config

# Ensure the database URL is properly set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://plaid_user:B2tF307010#1@localhost:5432/plaid_db")

# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Apply logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)  

# ✅ Add metadata reference so Alembic can detect models
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
