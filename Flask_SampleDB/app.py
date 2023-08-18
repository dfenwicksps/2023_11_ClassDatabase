from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3

DATABASE = 'sampleDB.db'
app = Flask(__name__)

# Function to get/connect to the database
def get_db_connection():
    """Connect to the database and return the connection."""
    # Check if we've already established a connection
    db_connection = getattr(g, '_database_connection', None)
    # If not, create a new connection
    if db_connection is None:
        db_connection = g._database_connection = sqlite3.connect(DATABASE)
    return db_connection

# Query function - to execute queries
def query_db(query, parameters=(), return_one_record=False):
    """Execute a query on the database."""
    connection = get_db_connection()
    cursor = connection.execute(query, parameters)
    all_records = cursor.fetchall()
    cursor.close()
    if return_one_record and all_records:
        return all_records[0]
    return all_records

# Teardown function to close the database connection at the end of request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

'''@app.route('/')
def index():
    students = query_db('SELECT FirstName, LastName FROM Students')
    return render_template('index.html', students=students)'''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # Check if the form has been submitted
        first_name = request.form.get('first_name')  # Get the first name from the form
        last_name = request.form.get('last_name')  # Get the last name from the form
        age = request.form.get('age')  # Get the age from the form
        grade = request.form.get('grade')  # Get the grade from the form

        # Check if all fields are filled
        if first_name and last_name and age and grade:
            # Insert the new student into the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, age, grade))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))  # Redirect to the index page to display the updated list

    students = query_db("SELECT * FROM Students")
    return render_template('index.html', students=students)

'''@app.route('/courses')
def courses():
    courses = query_db('SELECT CourseName FROM Courses')
    return render_template('courses.html', courses=courses)'''
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        if course_name:
            # Insert the new course into the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Courses (CourseName) VALUES (?)", (course_name,))
            connection.commit()
            connection.close()
            return redirect(url_for('courses')) # Redirect to the same courses page to display the updated list

    courses = query_db("SELECT * FROM Courses")
    return render_template('courses.html', courses=courses)


if __name__ == '__main__':
    app.run(debug=True)