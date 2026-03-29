import streamlit as st
import pandas as pd
import os
from module.email_service import send_email
from module.export_module import export_pdf
from module.analytics_module import get_data
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



def show_email():

    recipient = st.text_input("Recipient Email")

    if st.button("Generate & Send Report"):
        try:
            bar = st.progress(0)
            if not recipient:
                st.warning("Please enter a recipient email.")
                st.stop()

            os.makedirs("report", exist_ok=True)

            # CSV EXPORT
            conn = get_connection()
            df_full = pd.read_sql_query("SELECT id, uid, chunk, score, matched_rules, sentiment FROM chunks", conn)
            conn.close()

            if df_full.empty:
                st.warning("No records available.")
                st.stop()

            max_csv_rows = 20000

            if len(df_full) > max_csv_rows:
                df_csv = df_full.head(max_csv_rows)
            else:
                df_csv = df_full

            csv_path = "report/view_records_report.csv"
            df_csv.to_csv(csv_path, index=False)

            # METRICS 
            (
                total_chunks,
                avg_score,
                unique_uids,
                positive,
                negative,
                neutral
            ) = get_overview_metrics()

            total_csv_records = get_total_csv_records()

            data = get_data()

            # PDF 
            pdf_path = export_pdf(
                data,
                total_csv_records,
                total_chunks,
                avg_score,
                unique_uids,
                positive,
                negative,
                neutral
            )

            # EMAIL BODY 
            body = f"""
Parallel Text Processing Report

Total CSV Records: {total_csv_records}
Chunks Stored: {total_chunks}
Average Score: {round(avg_score,2)}
Unique UIDs: {unique_uids}

Sentiment Counts
Positive: {positive}
Negative: {negative}
Neutral: {neutral}

Attachments
1. PDF Analytics Report
2. CSV Data 
"""

            # SEND EMAIL 
            send_email(
                recipient,
                "Parallel Text Processing Report",
                body,
                attachments=[pdf_path, csv_path]
            )
            
            bar.progress(100)
            st.success("✅ Email Sent Successfully")
        
        except Exception as e:
            st.error(f"Email sending failed: {e}")