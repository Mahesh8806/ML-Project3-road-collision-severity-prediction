"""
PostgreSQL Database Setup Script

This script creates the database if it doesn't exist.
Run this before executing the notebooks.

Usage:
    python setup_database.py
"""

import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
PROJECT_DIR = Path.cwd()
load_dotenv(PROJECT_DIR / ".env")

# Get credentials
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")
pg_db = os.getenv("POSTGRES_DB")
pg_user = os.getenv("POSTGRES_USER")
pg_pwd = os.getenv("POSTGRES_PASSWORD")

print("=" * 70)
print("PostgreSQL Database Setup")
print("=" * 70)
print(f"\nTarget Database: {pg_db}")
print(f"Host: {pg_host}:{pg_port}")
print(f"User: {pg_user}")
print("\n" + "-" * 70)

try:
    # Connect to PostgreSQL server (not to specific database)
    print("\n1. Connecting to PostgreSQL server...")
    conn = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        user=pg_user,
        password=pg_pwd,
        database='postgres'  # Connect to default database first
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    print("   ✓ Connected to PostgreSQL server")
    
    # Check if database exists
    print(f"\n2. Checking if database '{pg_db}' exists...")
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (pg_db,)
    )
    exists = cursor.fetchone()
    
    if exists:
        print(f"   ✓ Database '{pg_db}' already exists")
    else:
        # Create database
        print(f"   Creating database '{pg_db}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(pg_db))
        )
        print(f"   ✓ Database '{pg_db}' created successfully")
    
    cursor.close()
    conn.close()
    
    # Connect to the new database to verify
    print(f"\n3. Verifying connection to '{pg_db}'...")
    conn2 = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        user=pg_user,
        password=pg_pwd,
        database=pg_db
    )
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT version();")
    version = cursor2.fetchone()[0]
    print(f"   ✓ Successfully connected to '{pg_db}'")
    print(f"\n   PostgreSQL Version: {version[:60]}...")
    
    cursor2.close()
    conn2.close()
    
    print("\n" + "=" * 70)
    print("✓ DATABASE SETUP COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Run: python upload_to_postgres.py (to verify connection)")
    print("2. Open and run: 01_data_ingestion_profiling.ipynb")
    print("\n" + "=" * 70)
    
except psycopg2.OperationalError as e:
    print(f"\n✗ Connection failed!")
    print(f"Error: {e}")
    print("\nPossible issues:")
    print("1. PostgreSQL service is not running")
    print("2. Host/port is incorrect")
    print("3. Username/password is incorrect")
    print("4. PostgreSQL is not accepting connections")
    print("\nCheck your .env file settings and PostgreSQL service status.")
    
except psycopg2.Error as e:
    print(f"\n✗ Database operation failed!")
    print(f"Error: {e}")
    
except Exception as e:
    print(f"\n✗ Unexpected error!")
    print(f"Error: {e}")

print("\n" + "=" * 70)
