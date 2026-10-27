import os
import sqlite3
import streamlit as st

# Set up paths and database filename
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def init_db():
    """Sets up an SQLite database with sample accounts."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'SuperSecretPass123!', 'Administrator')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('john_doe', 'userpassword123', 'Regular User')")
    conn.commit()
    conn.close()

# Initialize or reset database on startup
init_db()

# Configure Streamlit page layout
st.set_page_config(page_title="SQL Injection Lab", page_icon="🔓", layout="centered")

st.title("🔓 SQL Injection Simulator")
st.markdown("Explore how SQL injection vulnerabilities occur through string interpolation and how parameterized queries keep applications secure.")

# Mode selection toggle
mode = st.radio("Select Mode", ["Vulnerable Mode", "Secure Mode"], horizontal=True)

# Input form for user credentials
with st.form("login_form"):
    username = st.text_input("Username Payload", placeholder="e.g. admin' --")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Execute Query")

executed_sql = "SELECT ..."
response_message = "Click 'Execute Query' to test."
is_success = None

if submit_button:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if mode == "Vulnerable Mode":
        # DANGEROUS: Directly interpolates user input into SQL
        executed_sql = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            cursor.execute(executed_sql)
            user = cursor.fetchone()
            if user:
                response_message = f"Bypassed/Logged in as '{user[0]}' (Role: {user[1]})"
                is_success = True
            else:
                response_message = "Invalid credentials."
                is_success = False
        except Exception as e:
            response_message = f"SQL Error: {str(e)}"
            is_success = False
            
    else:
        # SECURE: '?' placeholders treat input as literal text strings only
        parameterized_sql = "SELECT username, role FROM users WHERE username = ? AND password = ?"
        executed_sql = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}' (Parameterized/Bound)"
        try:
            cursor.execute(parameterized_sql, (username, password))
            user = cursor.fetchone()
            if user:
                response_message = f"Authenticated successfully as '{user[0]}' (Role: {user[1]})"
                is_success = True
            else:
                response_message = "Login blocked: Credentials do not match."
                is_success = False
        except Exception as e:
            response_message = f"SQL Error: {str(e)}"
            is_success = False
            
    conn.close()

# Display Executed SQL Query Block
st.subheader("Executed SQL Query")
st.code(executed_sql, language="sql")

# Display Server Response Block
st.subheader("Server Response")
if submit_button:
    if is_success:
        st.success(response_message)
    else:
        st.error(response_message)
else:
    st.info(response_message)