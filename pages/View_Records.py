import streamlit as st
import pandas as pd
from database.database import get_connection
import streamlit as st
import pandas as pd
from database.database import get_connection

def show_records():
    conn = get_connection()
    cursor = conn.cursor()

    # FILTERS

    sentiment_filter = st.selectbox(
        "Sentiment",
        ["All","Positive","Negative","Neutral"]
    )

    conditions = []

    if sentiment_filter != "All":
        conditions.append(f"sentiment='{sentiment_filter}'")

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # COUNT TOTAL RECORDS 

    cursor.execute(f"SELECT COUNT(*) FROM chunks {where_clause}")
    total_records = cursor.fetchone()[0]

    st.write("Total Records:", total_records)

    # PAGINATION 

    page_size = 1000
    total_pages = max((total_records // page_size)+1,1)

    page = st.number_input("Page",1,total_pages,1)

    offset = (page-1)*page_size

    query = f"""
    SELECT id, uid, chunk, score, matched_rules, sentiment
    FROM chunks
    {where_clause}
    LIMIT {page_size}
    OFFSET {offset}
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    # Display Sentiment with colors and download option

    if not df.empty:

        def color_sentiment(val):
            if val=="Positive":
                return "color:green;font-weight:bold"
            elif val=="Negative":
                return "color:red;font-weight:bold"
            else:
                return "color:gray;font-weight:bold"

        styled = df.style.map(color_sentiment,subset=["sentiment"])

        st.dataframe(styled,use_container_width=True)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name=f"records_page_{page}.csv"
        )

    else:
        st.warning("No records found")

    st.write(f"Page {page} of {total_pages}")