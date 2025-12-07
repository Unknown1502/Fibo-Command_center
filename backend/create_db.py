"""
Database migration script to create all tables
Run this after configuring database connection
"""
from database import Base, engine
from sqlalchemy import inspect

def create_tables():
    """Create all tables defined in models"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print("Creating database tables...")
    print(f"Existing tables: {existing_tables}")
    
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    new_tables = inspector.get_table_names()
    print(f"Tables after creation: {new_tables}")
    print("Database setup completed successfully!")

if __name__ == "__main__":
    create_tables()
