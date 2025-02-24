from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import pandas as pd
import sqlite3
import mysql.connector
from execute_query import execute_query  # Import query execution function
from generate_sql_query import generate_sql_query  # Import NLP to SQL function

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# MySQL database configuration
mysql_config = {
    'user': 'root',
    'password': '153415',
    'host': 'localhost',
    'database': 'loginbd',
    'raise_on_warnings': True
}

# Correct dataset path (CSV files)
DATASET_FOLDER = r"D:\final year project\final year project"
DATABASE_FILE = "college.db"

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyBVdzfDouVTrIulEpJQ6Ic27msELcVd--A"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize the SQLite database
available_dbs = [f.replace(".csv", "") for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

for db_name in available_dbs:
    csv_path = os.path.join(DATASET_FOLDER, f"{db_name}.csv")
    df = pd.read_csv(csv_path)
    
    columns = ", ".join([f'"{col}" TEXT' for col in df.columns])  # Assuming text format for simplicity
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{db_name}" ({columns});'
    cursor.execute(create_table_query)

    for _, row in df.iterrows():
        placeholders = ", ".join(["?" for _ in df.columns])
        insert_query = f'INSERT INTO "{db_name}" VALUES ({placeholders});'
        cursor.execute(insert_query, tuple(row))

conn.commit()
conn.close()

def df_to_tailwind_table(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a Tailwind CSS styled HTML table."""
    # Start the table with Tailwind classes for full width and proper styling.
    html = '<table class="min-w-full divide-y divide-gray-700 table-auto">'
    
    # Build the header
    html += '<thead class="bg-gray-700"><tr>'
    for col in df.columns:
        html += (
            f'<th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">'
            f'{col}'
            f'</th>'
        )
    html += '</tr></thead>'
    
    # Build the body rows
    html += '<tbody class="bg-gray-800 divide-y divide-gray-700">'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            html += f'<td class="px-6 py-4 whitespace-nowrap text-sm text-white">{row[col]}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', databases=available_dbs)  # Show index if logged in
    return redirect(url_for('login'))  # Redirect to login if not logged in


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['email'] = email  # Save email in session
            session['password'] = password  # Save password in session
            return redirect(url_for('index'))  # Redirect to index after login
        else:
            flash('Invalid email or password')  # Show error if invalid
    return render_template('login.html')  # Render login page if not POST or invalid credentials


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        dob = request.form['dob']
        
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, username, dob) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, email, password, username, dob))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    data = request.json
    user_query = data.get("user_query")
    db_name = data.get("db_name")

    if not user_query or not db_name:
        return jsonify({"error": "Invalid input"}), 400

    try:
        sql_query = generate_sql_query(user_query, db_name)  # Generate SQL query
        return jsonify({"sql_query": sql_query})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/execute_query', methods=['POST'])
def execute_sql():
    data = request.json
    sql_query = data.get("sql_query")
    
    if not sql_query:
        return "No SQL query provided", 400
    
    try:
        # Execute the query and obtain a DataFrame
        results_df = execute_query(sql_query)  # This returns a DataFrame
        # Convert the DataFrame to a Tailwind-styled HTML table
        results_html = df_to_tailwind_table(results_df)
        return results_html  # Return the HTML string directly
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)