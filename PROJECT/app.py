import streamlit as st
from database.database import init_db

from pages.Overview import show_overview
from pages.Upload_Files import show_upload
from pages.Run_Pipeline import show_pipeline
from pages.View_Records import show_records
from pages.Search import show_search
from pages.Analytics import show_analytics
from pages.Email_Report import show_email
from pages.Clear_Data import show_clear

# INIT
init_db()

st.set_page_config(
    page_title="Parallel Text Processor",
    layout="wide"
)

hide_streamlit_style = """
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# SIDEBAR MENU
st.sidebar.markdown("## Parallel Text Processor")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Upload Files",
        "Run Pipeline",
        "View Records",
        "Search",
        "Analytics",
        "Email Report",
        "Clear Data"
    ]
)

# HEADER AND DESCRIPTIONS
section_icons = {
    "Overview": "🎯",
    "Upload Files": "📂",
    "Run Pipeline": "⚙",
    "View Records": "📑",
    "Search": "🔍",
    "Analytics": "📈",
    "Email Report": "📧",
    "Clear Data": "🗑"
}

section_descriptions = {
    "Overview": "View system statistics, stored chunks, and overall performance metrics.",
    "Upload Files": "Upload multiple text, csv files to begin processing and chunk generation.",
    "Run Pipeline": "Create chunks using parallel processing and apply rule-based scoring.",
    "View Records": "Browse, filter and download all processed text records.",
    "Search": "Search stored chunks using keyword or regex-based queries.",
    "Analytics": "Visualize score and sentiment distribution",
    "Email Report": "Generate a PDF report and send results via email.",
    "Clear Data": "Permanently delete all stored records from the database."
}

st.markdown("# Python Parallel Text Processor")
st.markdown(f"## {section_icons.get(menu,'')} {menu}")

st.markdown(
f"""
<div style="background:#1E3A8A;padding:10px;border-radius:8px;color:white">
{section_descriptions.get(menu,"")}
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ROUTING TO PAGES
if menu == "Overview":
    show_overview()

elif menu == "Upload Files":
    show_upload()

elif menu == "Run Pipeline":
    show_pipeline()

elif menu == "View Records":
    show_records()

elif menu == "Search":
    show_search()

elif menu == "Analytics":
    show_analytics()

elif menu == "Email Report":
    show_email()

elif menu == "Clear Data":
    show_clear()