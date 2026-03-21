"""
Test file to test connection to db
"""

import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="local",
        user="admin",
        password="admin"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"Te conectaste a: {record}")

    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'expenses'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    print("\n--- users ---")
    print(f"{'columna':<25} {'tipo':<30} {'nullable':<10} {'default'}")
    print("-" * 90)
    for col in columns:
        print(f"{col[0]:<25} {col[1]:<30} {col[2]:<10} {col[3] or ''}")

    cursor.close()
    connection.close()
except Exception as error:
    print(f"Error: {error}")