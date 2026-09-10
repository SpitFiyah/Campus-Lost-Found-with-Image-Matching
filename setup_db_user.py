#!/usr/bin/env python3
"""Setup MySQL user for the application."""
from getpass import getpass

import pymysql

try:
    root_password = getpass("MySQL root password: ")
    print("Connecting to MySQL as root...")
    conn = pymysql.connect(host='localhost', user='root', password=root_password, database='mysql')
    cursor = conn.cursor()
    
    # Create user and grant privileges
    print("Creating user 'campus_user'...")
    cursor.execute("CREATE USER IF NOT EXISTS 'campus_user'@'localhost' IDENTIFIED BY 'campus_password'")
    print("✓ User created or already exists")
    
    print("Granting privileges...")
    cursor.execute("GRANT ALL PRIVILEGES ON campus_lost_found.* TO 'campus_user'@'localhost'")
    cursor.execute("FLUSH PRIVILEGES")
    print("✓ Privileges granted")
    
    cursor.execute("SELECT User, Host FROM mysql.user WHERE User='campus_user'")
    result = cursor.fetchone()
    print(f"✓ Verified: {result}")
    
    conn.commit()
    conn.close()
    print("\n✓ Database user setup complete!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
