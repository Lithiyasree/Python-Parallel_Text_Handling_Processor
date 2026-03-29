import pandas as pd
import re
from database.database import get_connection


# KEYWORD SEARCH
def search_keyword(keyword, limit):

    conn = get_connection()

    query = """
    SELECT *
    FROM chunks
    LIMIT 50000
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    pattern = r"\b" + re.escape(keyword) + r"\b"

    result = df[df["chunk"].str.contains(pattern, flags=re.IGNORECASE, regex=True)]

    return result.head(limit)



# REGEX SEARCH
def search_regex(pattern, limit):

    conn = get_connection()

    query = """
    SELECT *
    FROM chunks
    LIMIT 50000
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    try:

        result = df[df["chunk"].str.contains(pattern, flags=re.IGNORECASE, regex=True)]

    except re.error:

        return pd.DataFrame()

    return result.head(limit)