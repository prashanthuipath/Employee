from flask import Flask, render_template, request, redirect, url_for
import pypyodbc as odbc
from flask import jsonify

app = Flask(__name__)

def db_connection():
    driver_name = 'SQL SERVER'
    server_name = 'Abarna-62HT203\SQLEXPRESS'
    database_name = 'employee'

    connection_string = f"""
    DRIVER={{{driver_name}}};
    SERVER={server_name};
    DATABASE={database_name};
    Trust_Connection = yes;
    """

    # conn = odbc.connect(connection_string)
    return odbc.connect(connection_string)

  

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login_employee', methods=['POST'])
def login():
    if request.method == 'POST':
        emp_username = request.form['username']
        emp_password = request.form['password']

        if not emp_username or not emp_password:
            error = 'Please enter both username and password.'
            return render_template('login.html', error=error)
       
        connection = db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM login WHERE emp_id = ? AND emp_password = ?", (emp_username, emp_password))

        user = cursor.fetchone()

        if user:
            # If user exists, redirect to the add employee page
            return redirect(url_for('add_employee'))
        else:
            # If user doesn't exist or credentials are incorrect, show login page again with an error message
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
        


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_name = request.form['name']
        emp_gender = request.form['gender']
        emp_skill = request.form['skill']

        connection = db_connection()
        cursor = connection.cursor()

        # Insert the new employee details into the 'emp' table
        cursor.execute("INSERT INTO emp (emp_name, emp_gender, emp_skill) VALUES (?, ?, ?)",(emp_name, emp_gender, emp_skill))

        connection.commit()
        connection.close()

        return redirect(url_for('load_table'))
    else:
        # If it's a GET request, simply render the add employee page
        return render_template('addemp.html')
    


@app.route('/view_employee', methods=['GET'])
def load_table():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM emp")
    data = cursor.fetchall()
    connection.close()

    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

