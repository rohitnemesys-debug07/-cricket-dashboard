from db import get_connection

conn = get_connection()

if conn:
    conn.close()
else:
    print("Still failing")