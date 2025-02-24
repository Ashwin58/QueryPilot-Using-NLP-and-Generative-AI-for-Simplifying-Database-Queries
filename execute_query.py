import pandas as pd
import os
import sqlite3
# Path to the dataset folder where CSV files are stored
#DATASET_FOLDER = r"D:\querypilot\spider\database"

'''def load_csv_file(db_name):
    """
    Loads the selected CSV file into a Pandas DataFrame.
    
    :param db_name: The name of the CSV file selected by the user.
    :return: Pandas DataFrame containing the CSV data.
    """
    file_path = os.path.join(DATASET_FOLDER, db_name + ".csv")  # Convert db_name to filename
    if os.path.exists(file_path):
        return pd.read_csv(file_path)  # Load CSV into DataFrame
    else:
        return None  # File not found'''


# Connect to the SQLite database
DATABASE_FILE = "college.db"
def execute_query(query):
    try:
        # Create a new connection inside the function
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()

            query = query.strip()

            # Handle SELECT queries
            if query.startswith("SELECT"):
                query = query.replace("SELECT", "SELECT DISTINCT", 1)
                df = pd.read_sql_query(query, conn)
                return df if not df.empty else "No records found."

            # Handle INSERT, UPDATE, DELETE, CREATE, DROP, etc.
            else:
                cursor.execute(query)
                conn.commit()
                return "Query executed successfully."

    except sqlite3.Error as e:
        return f"SQL Error: {e}"
