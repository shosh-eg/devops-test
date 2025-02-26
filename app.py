from flask import Flask, request
import sqlite3

app = Flask(__name__)

DATABASE = 'db.sqlite'

def add_task(task_name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    conn.close()

@app.route('/tasks', methods=['POST'])
def add():
    task_name = request.form['task']
    add_task(task_name)
    return 'Task added', 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT task_name FROM tasks")
    tasks = [row[0] for row in c.fetchall()]
    conn.close()
    return {'tasks': tasks}

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
