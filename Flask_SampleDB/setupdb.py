import sqlite3

# Connect to the SQLite database. If the database does not exist, it will be created.
conn = sqlite3.connect('sampleDB.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    Age INTEGER,
    Grade REAL
)
''')

cursor.execute('''
CREATE TABLE Courses (
    CourseID INTEGER PRIMARY KEY,
    CourseName TEXT
)
''')

cursor.execute('''
CREATE TABLE Enrollment (
    EnrollmentID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    CourseID INTEGER,
    FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY(CourseID) REFERENCES Courses(CourseID)
)
''')

cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('John', 'Doe', 19, 85.5)''')
cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('Jane', 'Smith', 20, 90.0)''')
cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('Bob', 'Biggs', 22, 75.0)''')
cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('Jim', 'Brown', 21, 78.5)''')
cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('Suzy', 'Smith', 18, 80.0)''')
cursor.execute('''INSERT INTO Students (FirstName, LastName, Age, Grade) VALUES ('Sam', 'Smith', 19, 92.5)''')


cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('English')''')
cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('Math')''')
cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('History')''')
cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('Science')''')
cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('Art')''')
cursor.execute('''INSERT INTO Courses (CourseName) VALUES ('Music')''')

cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (1, 1)''')
cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (1, 2)''')
cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (2, 2)''')
cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (3, 1)''')
cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (3, 3)''')
cursor.execute('''INSERT INTO Enrollment (StudentID, CourseID) VALUES (4, 4)''')


# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")

# Run this script from the command line to create the database and tables:
# python setupdb.py
# open terminal from within Pycharm
# cd Flask_SampleDB
# python setupdb.py