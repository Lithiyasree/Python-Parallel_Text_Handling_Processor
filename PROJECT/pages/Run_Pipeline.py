import streamlit as st
import os
import pandas as pd
from module.loader import parallel_process
from module.rule_engine import apply_rules

def show_pipeline():

    st.header("Step 2: Process Files")

    files = [f"data/{f}" for f in os.listdir("data")]

    if not files:
        st.warning("No files found. Please upload files first.")
        st.stop()

    st.write("Files Ready for Processing:")
    st.write(os.listdir("data"))

    # Detect CSV files
    csv_files = [f for f in files if f.endswith(".csv")]
    selected_column = None

    if csv_files:
        st.subheader("CSV Column Selection")

        df_preview = pd.read_csv(csv_files[0])
        st.write("Preview of first CSV file:")
        st.dataframe(df_preview.head())

        selected_column = st.selectbox(
            "Select column to process (applies to all CSV files)",
            df_preview.columns
        )

    # Settings
    st.subheader("Processing Settings")

    max_workers = max(1, (os.cpu_count() or 2) - 1)
    group_size = st.slider("Words per Chunk", 50, 500, 100)
    
    if st.button("Start Processing"):
        try:
            bar = st.progress(0)
            success = parallel_process(files, selected_column, group_size, max_workers)
            bar.progress(100)

            if success:
                st.success("Chunks Created ✅")
                print("Chunks Created ✅")
            else:
                st.error("Some files failed to process ❌")
        except Exception as e:
            st.error(f"Processing error: {e}")

    st.markdown("---")

    st.header("Step 3: Apply Scoring")
    
    if st.button("Apply Rule Scoring"):
        try:
            bar = st.progress(0)
            apply_rules()
            bar.progress(100)
            st.success("Scoring Completed ✅")
            print("Scoring Completed ✅")
        except Exception as e:
            st.error(f"Rule scoring failed: {e}")