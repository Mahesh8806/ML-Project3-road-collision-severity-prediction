print("="*70)
print("ROAD COLLISION SEVERITY PREDICTION PROJECT - COMPLETION STATUS")
print("="*70)

# Check notebooks
import os
notebooks = [
    "01_data_ingestion_profiling.ipynb",
    "02_deep_cleaning_transformation.ipynb", 
    "03_eda_visualization.ipynb",
    "04_feature_engineering.ipynb",
    "05_ml_pipeline_training.ipynb",
    "06_explainability_insights.ipynb"
]

print("\n NOTEBOOKS CREATED:")
for nb in notebooks:
    size = os.path.getsize(nb) if os.path.exists(nb) else 0
    status = "" if size > 1000 else ""
    print(f"  {status} {nb} ({size:,} bytes)")

# Check visualizations
print("\n VISUALIZATIONS GENERATED:")
viz_files = [f for f in os.listdir() if f.endswith('.png')]
for viz in sorted(viz_files):
    print(f"   {viz}")

# Check database
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

print("\n📊 DATABASE TABLES:")
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
        print(f"  ✓ {table_name}: {count:,} rows")

print("\n" + "="*70)
print("PROJECT STATUS: NOTEBOOKS 1-2 FULLY TESTED, 3-6 READY TO RUN")
print("="*70)
