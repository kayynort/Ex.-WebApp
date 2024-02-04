# main.py

# Step 1: Install Flask Framework

# Step 2: Create Python Script

# Step 2.2: Import components from the Flask framework
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import BadRequestKeyError  # Import BadRequestKeyError
import sqlite3

# Step 2.3: Create the Flask App
app = Flask(__name__)

# Step 2.4: Create a connection to the database and define the 'courses' table
conn = sqlite3.connect('educational_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        uid INTEGER NOT NULL,
        year TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        satisfaction INTEGER NOT NULL,
        feedback TEXT,
        credits_completed INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()


# Step 2.5: Create a route for the home page
# Step 2.5: Create a route for the home page
@app.route('/')
def index():
    # No need to fetch courses from the database
    return render_template('index.html')



# Step 2.6: Create a route for adding a new course
@app.route('/add_course', methods=['POST'])
def add_course():
    try:
        # Extract course details from the form
        uid = int(request.form['uid'])
        year = request.form['year']
        name = request.form['name']
        description = request.form['description']
        satisfaction = int(request.form['satisfaction'])
        feedback = request.form['reason']
        credits_completed = int(request.form['credits_completed'])

        # Add the new course to the database
        conn = sqlite3.connect('educational_data.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO courses (uid, year, name, description, satisfaction, feedback, credits_completed) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (uid, year, name, description, satisfaction, feedback, credits_completed))
        conn.commit()
        conn.close()

        # Redirect to the home page after adding a course
        return redirect(url_for('index'))
    except BadRequestKeyError as e:
        # Handle the BadRequestKeyError here, e.g., redirect to an error page
        return render_template('error.html', error_message="Bad Request: Missing Form Field")
    except ValueError as e:
        # Handle ValueError if conversion to int fails
        return render_template('error.html', error_message=str(e))
    except Exception as e:
        # Handle other exceptions if needed
        return render_template('error.html', error_message=str(e))


# Step 2.7: Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
