import pandas as pd
from database.database import get_connection

def get_data():

    conn = get_connection()

    df = pd.read_sql_query("""
    SELECT score, sentiment, rule_category
    FROM chunks
    LIMIT 200000
    """, conn)

    conn.close()

    return df