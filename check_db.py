import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
PROJECT_DIR = Path.cwd()
load_dotenv(PROJECT_DIR / ".env")

# Get PostgreSQL credentials
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")
pg_db = os.getenv("POSTGRES_DB")
pg_user = os.getenv("POSTGRES_USER")
pg_pwd = os.getenv("POSTGRES_PASSWORD")

# Create connection
url = f"postgresql+psycopg2://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}"
engine = create_engine(url)

print("📊 Database Tables:")
with engine.connect() as conn:
    # Get all tables in public schema
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """))
    tables = result.fetchall()
    
    for table in tables:
        table_name = table[0]
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = count_result.fetchone()[0]
        print(f"  - {table_name}: {count:,} rows")
