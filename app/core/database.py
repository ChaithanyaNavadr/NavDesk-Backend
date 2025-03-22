from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

# Load settings
settings = get_settings()

# Set up the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # Helps prevent stale connections
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for SQLAlchemy
Base = declarative_base()

# Dependency to get the database session
def get_db():
    """Dependency for getting the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metadata for Alembic migrations
metadata = Base.metadata

def test_connection():
    """Test the database connection."""
    try:
        engine.connect()
        return True
    except:
        return False