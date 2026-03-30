import streamlit as st
import os
import pandas as pd
from database.database import get_connection

def get_total_csv_records():
    total = 0
    if os.path.exists("data"):
        for file in os.listdir("data"):
            if file.endswith(".csv"):
                try:
                    df = pd.read_csv(os.path.join("data", file))
                    total += len(df)
                except:
                    pass
    return total


def get_overview_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chunks")
    total_chunks = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM chunks")
    avg_score = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT uid) FROM chunks")
    unique_uids = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chunks WHERE sentiment='Positive'")
    positive = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chunks WHERE sentiment='Negative'")
    negative = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chunks WHERE sentiment='Neutral'")
    neutral = cursor.fetchone()[0]

    conn.close()

    return total_chunks, avg_score, unique_uids, positive, negative, neutral


# OVERVIEW PAGE
def show_overview():
    
    total_chunks, avg_score, unique_uids, positive, negative, neutral = get_overview_metrics()
    total_csv_records = get_total_csv_records()

    # Processing Summary 
    st.markdown("### Processing Summary")

    overview_table = f"""
    <table style="width:100%; border-collapse: collapse; text-align:center;">
        <tr style="background-color:#1E3A8A; color:white;">
            <th>Total CSV Records</th>
            <th>Chunks Stored</th>
            <th>Average Score</th>
            <th>Unique UIDs</th>
        </tr>
        <tr>
            <td><b>{total_csv_records}</b></td>
            <td><b>{total_chunks}</b></td>
            <td><b>{round(avg_score,2)}</b></td>
            <td><b>{unique_uids}</b></td>
        </tr>
    </table>
    """

    st.markdown(overview_table, unsafe_allow_html=True)


    # Sentiment Summary 
    st.markdown("### Sentiment Summary")

    sentiment_table = f"""
    <table style="width:100%; border-collapse: collapse; text-align:center;">
        <tr style="background-color:#1E3A8A; color:white;">
            <th>🟢 Positive</th>
            <th>⚪ Neutral</th>
            <th>🔴 Negative</th>
        </tr>
        <tr>
            <td><b>{positive}</b></td>
            <td><b>{neutral}</b></td>
            <td><b>{negative}</b></td>
        </tr>
    </table>
    """

    st.markdown(sentiment_table, unsafe_allow_html=True)