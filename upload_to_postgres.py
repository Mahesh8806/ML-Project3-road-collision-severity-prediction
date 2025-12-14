"""
PostgreSQL Connection Helper Script

This script demonstrates how to connect to PostgreSQL using environment variables.
All notebooks in this project use this same pattern for database connections.

Usage:
    python upload_to_postgres.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
PROJECT_DIR = Path.cwd()
load_dotenv(PROJECT_DIR / ".env")

# Get PostgreSQL credentials from environment variables
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")
pg_db = os.getenv("POSTGRES_DB")
pg_user = os.getenv("POSTGRES_USER")
pg_pwd = os.getenv("POSTGRES_PASSWORD")

# Build PostgreSQL connection URL
# Format: postgresql+psycopg2://user:password@host:port/dbname
url = f"postgresql+psycopg2://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}"

# Create SQLAlchemy engine
engine = create_engine(url)

# Test connection and display database info
print("=" * 70)
print("PostgreSQL Connection Test")
print("=" * 70)

try:
    with engine.connect() as conn:
        # Check PostgreSQL version
        version = conn.execute(text("SELECT version();")).scalar()
        print(f"\n✓ Connection successful!")
        print(f"Database: {pg_db}")
        print(f"Host: {pg_host}:{pg_port}")
        print(f"User: {pg_user}")
        print(f"\nPostgreSQL Version:")
        print(version)
        
        # List all tables in public schema
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        tables = result.fetchall()
        
        if tables:
            print(f"\n📊 Tables in database:")
            for table in tables:
                table_name = table[0]
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.fetchone()[0]
                print(f"  - {table_name}: {count:,} rows")
        else:
            print("\n⚠ No tables found in the public schema")
            print("Run notebook 01_data_ingestion_profiling.ipynb to create and populate tables")
        
except Exception as e:
    print(f"\n✗ Connection failed!")
    print(f"Error: {e}")
    print("\nPlease check:")
    print("1. PostgreSQL server is running")
    print("2. Credentials in .env file are correct")
    print("3. Database 'Uk_collision' exists")

print("\n" + "=" * 70)
