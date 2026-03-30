import streamlit as st
import os

def show_upload():
    st.header("Step 1: Upload Files")

    uploaded_files = st.file_uploader(
        "Upload TXT or CSV Files",
        type=["txt", "csv"],
        accept_multiple_files=True
    )

    os.makedirs("data", exist_ok=True)

    if uploaded_files:
        for file in uploaded_files:
            try:
                file_path = os.path.join("data", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            except Exception as e:
                st.error(f"Failed to upload {file.name}: {e}")

        st.success("Files Uploaded Successfully ✅")

    st.subheader("Saved Files:")
    try:
        st.write(os.listdir("data"))
    except:
        st.write([])

    st.info("Next Go to 'Run Pipeline' to process the uploaded files.")