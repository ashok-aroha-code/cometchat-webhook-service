"""Initialize database and create tables"""
from app.core.database import engine, Base
from app.models.tenant import Tenant
from app.core.logging import logger


def init_db():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise


def drop_db():
    """Drop all database tables (use with caution!)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        raise


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
