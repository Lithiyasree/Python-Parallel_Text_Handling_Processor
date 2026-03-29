import os
import shutil
from database.database import get_connection

def clear_all_records():

    # Clear Database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks")
    conn.commit()
    conn.close()

    # Clear data folder files
    data_folder = "data"

    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)

            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Error deleting file:", e)