import sqlite3
import tkinter as tk
from tkinter import messagebox

# Create the database and tasks table
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")
conn.commit()
conn.close()

# Function to add a task
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to load tasks
def load_tasks():
    task_listbox.delete(0, tk.END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    for task in tasks:
        display_text = f"{task[0]}. {task[1]} - [{task[2]}]"
        task_listbox.insert(tk.END, display_text)

# Function to mark a task as done
def mark_done():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        task_id = selected_task.split(".")[0]
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task!")

# Function to delete a task
def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        task_id = selected_task.split(".")[0]
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task!")

# GUI Setup
app = tk.Tk()
app.title("To-Do List App")
app.geometry("400x400")

task_entry = tk.Entry(app, width=40)
task_entry.pack(pady=10)

add_button = tk.Button(app, text="Add Task", command=add_task)
add_button.pack()

task_listbox = tk.Listbox(app, width=50, height=10)
task_listbox.pack(pady=10)

done_button = tk.Button(app, text="Mark as Done", command=mark_done)
done_button.pack()

delete_button = tk.Button(app, text="Delete Task", command=delete_task)
delete_button.pack()

# Load tasks when the app starts
load_tasks()

# Run the application
app.mainloop()
