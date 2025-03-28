import json
class ToDoApp:
    def __init__(self, filename = "tasks.json"):
        self.filename = filename
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        
    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
        else:
            print("Task not found!")

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for tasks in self.tasks:
                print(f"- {tasks}")

    def save_tasks(self):
        """Save Tasks in json file"""

        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        """Json load tasks of file"""
        try:
            with open(self.filename, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            print(f"No existing task file found. Starting with an empty task list.")
            
app = ToDoApp()

app.add_task("Learn Python")
app.add_task("Build a To-Do app")
app.add_task("Meditation")
app.add_task("Yoga")
app.add_task("English Practice")
app.add_task("Runing")

app.show_tasks()
app.save_tasks()

print("********************")
app.remove_task("Runing")

app.show_tasks()

app.save_tasks()
        
   

