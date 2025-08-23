#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    import psycopg2
    print("✓ psycopg2 imported successfully")
    
    # Test database connection
    conn_string = (
        "postgresql://avnadmin:AVNS_QzflMrR3BXGAgudXgwL@"
        "pg-7fabea4-nikshithkyathrigi2005-3753.g.aivencloud.com:14586/defaultdb"
        "?sslmode=require"
    )
    
    print("Testing database connection...")
    conn = psycopg2.connect(conn_string)
    print("✓ Database connection successful")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✓ PostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
    print("✓ Connection closed successfully")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except psycopg2.Error as e:
    print(f"✗ Database error: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

