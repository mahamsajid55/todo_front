from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database file path
DB_path = "tasks.db"

# Database setup: Create tasks table
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Get all tasks from the database
def get_tasks():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Add a task to the database
def add_task(title, description):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)', (title, description, False))
    conn.commit()
    conn.close()

# Update task details (e.g., marking it as completed)
def update_task(id, title, description, completed):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?', (title, description, completed, id))
    conn.commit()
    conn.close()

# Delete a task by ID
def delete_task(id):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Home page to list tasks and show form to add a new task
@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html',  tasks=tasks)

# Add task via POST request
@app.route('/add_task', methods=['POST'])
def add_task_route():
    title = request.form['title']
    description = request.form['description']
    add_task(title, description)
    return redirect(url_for('index'))

# Update task via GET and POST request
@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task_route(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        completed = 'completed' in request.form
        update_task(id, title, description, completed)
        return redirect(url_for('index'))

    # Pre-fill form with current task data
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
    task = cursor.fetchone()
    conn.close()
    return render_template('update_task.html', task=task)

# Delete task via GET request
@app.route('/delete_task/<int:id>', methods=['GET'])
def delete_task_route(id):
    delete_task(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(debug=True, port=5002)  
