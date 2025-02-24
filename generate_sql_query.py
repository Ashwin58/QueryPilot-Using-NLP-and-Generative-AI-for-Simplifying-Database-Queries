import requests
# Your Gemini API Key
GEMINI_API_KEY = "AIzaSyBVdzfDouVTrIulEpJQ6Ic27msELcVd--A"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_sql_query(user_query, db_name):
    prompt = f"""
    You are an expert in converting English questions to SQL code! The SQL database has these tables:

    1. `students_dataset`:
    - `Student Id` (int)
    - `First Name` (text)
    - `Last Name` (text)
    - `Email` (text)
    - `Phone` (text)
    - `Department Id` (text)
    - `Enrollment Date` (text)

    2. `teachers_dataset`:
    - `Teacher Id` (text)
    - `First Name` (text)
    - `Last Name` (text)
    - `Email` (text)
    - `Phone` (text)
    - `Specialization` (text)
    - `Department Id` (text)
    - `Hire Date` (text)

    3. `enrollments_dataset`:
    - `Enrollment Id` (text)
    - `Student Id` (text)
    - `Course Id` (text)
    - `Enrollment Date` (text)

    4. `departments_dataset`:
    - `Department Id` (text)
    - `Department Name` (text)

    5. `courses_dataset`:
    - `Course Id` (text)
    - `Course Name` (text)
    - `Course Code` (text)
    - `Department Id` (text)
    - `Teacher Id` (text)
    - `Credits` (text)

    6. `buses_dataset`:
    - `Bus Id` (text)
    - `Bus Number` (text)
    - `Route` (text)
    - `Driver Name` (text)
    - `Driver Phone` (text)

    7. `books_dataset`:
    - `Book Id` (text)
    - `Title` (text)
    - `Author` (text)
    - `ISBN` (text)
    - `Publication Year` (text)
    - `Available Copies` (text)

    8. `attendance_dataset`:
    - `Attendance Id` (text)
    - `Student Id` (text)
    - `Course Id` (text)
    - `Attendance Date` (text)
    - `Attendance Status` (text)


    Convert the following natural language query to a **valid SQL query** for a CSV-based database.
    
    - The table name is `{db_name}`.
    - Do not return JSON or any explanation.
    - Return **only** the SQL query.
    - Use correct column names from the database.
    - Do not include ```sql or ```json formatting.
    - If user query contains part of column_name, include it in sql query.

    Example 1: What is the name of the student with ID 1?
    SQL: SELECT name FROM Students WHERE student_id = 1;

    Example 2: How many students are enrolled in the Computer Science department?
    SQL: SELECT COUNT(*) FROM Students WHERE department = 'Computer Science';

    Example 3: List all courses taught by Dr. Smith.
    SQL: SELECT c.course_name FROM Courses c JOIN Teachers t ON c.department_id = t.department_id WHERE t.name = 'Dr. Smith';

    Example 4: Find the total number of books in the library.
    SQL: SELECT COUNT(*) FROM Books;

    Example 5: Show the attendance status of student ID 2 for course ID 101.
    SQL: SELECT status FROM Attendance WHERE student_id = 2 AND course_id = 101;

    Example:

    User: Show all names of students with GPA above 3.5.
    SQL: SELECT student_name FROM students WHERE GPA > 3.5;

    User: Show all students with GPA above 3.5.
    SQL: SELECT * FROM students WHERE GPA > 3.5;

    Now, convert this query:

    User: {user_query}
    SQL:
    """

    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        # Make the POST request to Gemini API
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        
        # Check if the response is successful
        response.raise_for_status()  # Raise exception for any HTTP errors
        result = response.json()
        
        # Extract and clean the SQL query
        content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        sql_query = content.replace("```sql", "").replace("```", "").strip()
        
        return sql_query if "SELECT" in sql_query.upper() else f"Unexpected response: {content}"
    
    except requests.exceptions.RequestException as e:
        # st.write(f"Error generating SQL: {e}")
        return f"Error: {e}"
