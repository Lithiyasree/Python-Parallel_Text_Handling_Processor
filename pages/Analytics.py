import streamlit as st
import matplotlib.pyplot as plt
from database.database import get_connection
from module.analytics_module import get_data

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

# ANALYTICS PAGE 
def show_analytics():
    
    df = get_data()

    if df.empty:
        st.warning("No data available")
        st.stop()

    st.markdown("### Analytics Dashboard")

    # Get overview metrics
    total_chunks, avg_score, unique_uids, positive, negative, neutral = get_overview_metrics()

    col1, col2 = st.columns(2)

    # Sentiment Pie 
    with col1:
        st.subheader("Sentiment Distribution")
        fig1, ax1 = plt.subplots(figsize=(5, 4))

        ax1.pie(
            [positive, negative, neutral],
            labels=["Positive", "Negative", "Neutral"],
            autopct="%1.0f%%",
            colors=["#10F759", "#EF4444", "#3F94BB"],
            startangle=90,
            pctdistance=0.8,   
            labeldistance=1.1 
        )
        ax1.axis("equal")
        st.pyplot(fig1)

    # Score Histogram 
    with col2:
        st.subheader("Score Distribution")
        fig2, ax2 = plt.subplots(figsize=(5, 4))

        ax2.hist(
            df["score"],
            bins=10,
            color="#7D1ADA",
            edgecolor="white"
        )
        ax2.set_xlabel("Score")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)
