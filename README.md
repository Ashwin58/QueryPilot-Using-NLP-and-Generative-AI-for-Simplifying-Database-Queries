

# 🚀 QueryPilot - Natural Language to SQL Query Generator  

QueryPilot is an AI-powered Flask web application that converts natural language queries into SQL statements, making database interactions easier for non-technical users. It enables users to retrieve data efficiently without requiring SQL expertise.  

## 📌 Features  
✅ Convert natural language queries into SQL statements  
✅ Execute SQL queries and display results in a Tailwind-styled table  
✅ User authentication (Signup, Login, Logout) with MySQL  
✅ Automatic database setup from CSV files  
✅ Flask-based backend with session management  

## 🛠️ Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/your-username/QueryPilot.git
cd QueryPilot
```

### 2️⃣ Install Dependencies  
```sh
pip install Flask pandas mysql-connector-python
```

### 3️⃣ Set Up MySQL Database  
Create a database (`loginbd`) and a `users` table:  
```sql
CREATE DATABASE loginbd;
USE loginbd;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    dob DATE
);
```

### 4️⃣ Configure Environment Variables  
Edit `app.py` and replace:  
- **MySQL credentials** in `mysql_config`  
- **Dataset folder path**  
- **Gemini API key**  

### 5️⃣ Run the Flask Application  
```sh
python app.py
```
Access the app at **http://127.0.0.1:5000/**  

## 📂 Project Structure  
```
📦 QueryPilot  
 ┣ 📂 templates          # HTML templates  
 ┣ 📂 static             # Static files (CSS, JS)  
 ┣ 📜 app.py             # Main Flask application  
 ┣ 📜 execute_query.py   # Executes SQL queries  
 ┣ 📜 generate_sql_query.py # Converts natural language to SQL  
 ┣ 📜 requirements.txt   # List of dependencies  
 ┗ 📜 README.md          # Project documentation  
```

## ⚡ Usage  
1. **Sign up** or **log in**  
2. **Enter a natural language query** (e.g., "Show all students in the database")  
3. **Get the generated SQL query**  
4. **Execute the query** and view results in a styled table  

## 🛡️ License  
This project is open-source and available under the **MIT License**.  

---

Let me know if you need modifications! 🚀
