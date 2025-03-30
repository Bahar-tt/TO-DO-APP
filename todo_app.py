import json
import threading
import time
from plyer import notification
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.root.geometry("500x600")
        self.root.config(bg="#f1f1f1")

        self.tasks = []

        # Frame for input area
        self.input_frame = tk.Frame(self.root, bg="#f1f1f1")
        self.input_frame.pack(pady=20)

        self.task_input = tk.Entry(self.input_frame, width=30, font=("Arial", 12), bd=2, relief="solid")
        self.task_input.grid(row=0, column=0, padx=10)

        self.add_button = ttk.Button(self.input_frame, text="Add Task", command=self.add_task_from_input, style="TButton")
        self.add_button.grid(row=0, column=1, padx=10)

        # Task list frame
        self.task_list_frame = tk.Frame(self.root, bg="#f1f1f1")
        self.task_list_frame.pack(pady=20)

        self.show_button = ttk.Button(self.root, text="Show Tasks", command=self.show_tasks, style="TButton")
        self.show_button.pack()

        # Style for button
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=6)

        self.load_tasks()

    def add_task(self, task, remind_in=None):
        if task:
            task_data = {'task': task, 'remind_in': remind_in}
            self.tasks.append(task_data)
            self.task_input.delete(0, tk.END)
            self.show_tasks()

        if remind_in:
            threading.Thread(target=self.schedule_notification,
                             args=(task, remind_in), daemon=True).start()

    def add_task_from_input(self):
        task = self.task_input.get()
        if not task:
            return

        remind_in = simpledialog.askinteger("Reminder", "Set reminder in seconds (optional):")
        self.add_task(task, remind_in)

    def schedule_notification(self, task, remind_in):
        time.sleep(remind_in)
        notification.notify(
            title="Reminder Task",
            message=f"It is time to do this: {task}",
            timeout=10
        )

    def remove_task(self, index):
        del self.tasks[index]
        self.show_tasks()

    def edit_task(self, index):
        new_task = simpledialog.askstring("Edit Task", "Enter new task description:")
        if new_task:
            self.tasks[index]['task'] = new_task
            self.show_tasks()

    def show_tasks(self):
        # Clear current tasks from UI
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        if not self.tasks:
            label = tk.Label(self.task_list_frame, text="No tasks available!", bg="#f1f1f1", font=("Arial", 12))
            label.pack()
        else:
            for idx, task_data in enumerate(self.tasks):
                task_frame = tk.Frame(self.task_list_frame, bg="#ffffff", bd=2, relief="solid", pady=10, padx=10)
                task_frame.pack(pady=5, fill="x")

                task_label = tk.Label(task_frame, text=task_data['task'], width=30, anchor='w', bg="#ffffff", font=("Arial", 12))
                task_label.pack(side=tk.LEFT, padx=10)

                edit_button = ttk.Button(task_frame, text="Edit", command=lambda idx=idx: self.edit_task(idx), style="TButton")
                edit_button.pack(side=tk.LEFT, padx=5)

                remove_button = ttk.Button(task_frame, text="Remove", command=lambda idx=idx: self.remove_task(idx), style="TButton")
                remove_button.pack(side=tk.LEFT)

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

            for idx, task_data in enumerate(self.tasks):
                if not isinstance(task_data, dict):
                    self.tasks[idx] = {'task': task_data, 'remind_in': None}

        except FileNotFoundError:
            print("No existing task file found. Starting with an empty task list.")


root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
