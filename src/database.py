import sqlite3
def create_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, prioridad TEXT, fecha_limite TEXT, completada BOOL)')

def create_task(descripcion, prioridad, fecha_limite):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (descripcion, prioridad, fecha_limite) VALUES (?, ?, ?)', (descripcion, prioridad, fecha_limite))
    conn.commit()
    conn.close()

def read_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, descripcion, prioridad, fecha_limite):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET descripcion=?, prioridad=?, fecha_limite=? WHERE id=?', (descripcion, prioridad, fecha_limite, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()