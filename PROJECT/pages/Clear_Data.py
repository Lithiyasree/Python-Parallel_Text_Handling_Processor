import streamlit as st
from module.clear_records import clear_all_records

def show_clear():
    st.warning("⚠ This will permanently delete all records.")

    confirm = st.checkbox("I confirm that I want to delete all records.")

    if st.button("🗑 Clear All Records"):
        try:
            if confirm:
                clear_all_records()
                st.success("All records deleted successfully. ✅")
                print("Data Cleared ✅")
            else:
                st.error("Please confirm before deleting.")
        except Exception as e:
            st.error(f"Deletion failed: {e}")

