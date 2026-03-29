import streamlit as st
from module.search import search_keyword, search_regex

def show_search():
    
    mode = st.radio("Search Mode", ["Keyword", "Regex"])

    query = st.text_input("Enter Search Query")

    limit = st.slider("Max Results", 1, 100, 20)

    if st.button("Search"):
        try:
            if not query:
                st.warning("Please enter a search query")
                st.stop()

            if mode == "Keyword":
                result = search_keyword(query, limit)
            else:
                result = search_regex(query, limit)

            if result.empty:
                st.info("No results found")
            else:
                
                result = result.drop(columns=["rule_category"], errors="ignore")

                st.dataframe(result, use_container_width=True)

                st.download_button(
                    "Download Search Results",
                    result.to_csv(index=False),
                    file_name="search_results.csv"
                )
        except Exception as e:
            st.error(f"Search failed: {e}")