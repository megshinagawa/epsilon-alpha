import sqlite3
import datetime
from models import Task
from utils.helpers import format_time, format_duration, print_task

TASK_FORMAT = print_task
DB_FILE = "database/tasks.db"

class TaskManager:
    def __init__(self):
        """Initialize the database connection and create the table if it doesn't exist."""
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the tasks table if it does not exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT CHECK(status IN ('incomplete', 'in-progress', 'paused', 'cancelled', 'completed')) DEFAULT 'incomplete',
                signifier TEXT,
                do_date TEXT, 
                due_date TEXT,
                category TEXT,
                estimated_duration INTEGER,
                real_duration INTEGER,
                start_time TEXT NULL,
                end_time TEXT NULL
            )
        """)
        self.conn.commit()

    def add_task(self, name, description=None, status="incomplete", signifier=None,
                 do_date=None, due_date=None, category=None, estimated_duration=None):
        """Adds a new task to the database and returns the task ID."""
        self.cursor.execute("""
            INSERT INTO tasks (name, description, status, signifier, do_date, due_date, category, estimated_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, status, signifier, do_date, due_date, category, estimated_duration))

        self.conn.commit()
        return self.cursor.lastrowid  # Return the ID of the newly created task

    def list_tasks(self):
        """Retrieves all tasks from the database and returns them as Task objects."""
        self.cursor.execute("SELECT * FROM tasks")
        task_rows = self.cursor.fetchall()
        tasks = [Task.from_tuple(row) for row in task_rows]
        if not tasks:
            print("\nNo tasks found.")
            return
        print("\nTask List\n" + "-" * 40)
        for task in tasks:
            TASK_FORMAT(task)
        TaskManager().close()

    def get_task_by_id(self, task_id):
        """Fetch a task by its ID."""
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = self.cursor.fetchone()
        return Task.from_tuple(row) if row else None

    def update_task(self, task_id, **updates):
        """Updates a task with the provided values."""
        allowed_fields = ['name', 'description', 'status', 'signifier', 'do_date', 'due_date',
                          'category', 'estimated_duration', 'real_duration', 'start_time', 'end_time']
        update_pairs = ", ".join([f"{field} = ?" for field in updates if field in allowed_fields])
        values = list(updates.values()) + [task_id]

        if update_pairs:
            query = f"UPDATE tasks SET {update_pairs} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        return False

    def delete_task(self, task_id):
        """Deletes a task by its ID."""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0  # Returns True if a row was deleted
    
    def start_task(self, task_id):
        """Starts timer on the specified task."""
        start_time = datetime.datetime.now().isoformat()
        self.cursor.execute("UPDATE tasks SET start_time = ?, status = ? WHERE id = ?", (start_time, 'in-progress', task_id))
        self.conn.commit()
        print(f"Started task {task_id} at {format_time(start_time)}.")

    def pause_task(self, task_id):
        """Pause timer on the specified task."""
        self.cursor.execute("SELECT status, start_time, real_duration FROM tasks WHERE id = ?", (task_id,))
        row = self.cursor.fetchone()
        if row[0] == 'completed':
            print("Task is complete.")
        else: 
            if row and row[1]:
                start_time = datetime.datetime.fromisoformat(row[1])
                pause_time = datetime.datetime.now()
                additional_duration = (pause_time - start_time).total_seconds() // 60 
                if row[2]:
                    current_duration = row[2] + additional_duration
                else: 
                    current_duration = additional_duration
                
                self.cursor.execute("""
                    UPDATE tasks 
                    SET real_duration = ?, status = 'paused', start_time = NULL
                    WHERE id = ?
                """, (current_duration, task_id))
                self.conn.commit()
                print(f"Task {task_id} paused. Current duration: {format_duration(int(current_duration))}.")
            else:
                print("Task is not started.")

    def complete_task(self, task_id):
        """Stop the timer and calculate total duration."""
        self.cursor.execute("SELECT start_time, real_duration FROM tasks WHERE id = ?", (task_id,))
        row = self.cursor.fetchone()
        if row and row[0]:
            start_time = datetime.datetime.fromisoformat(row[0])
            end_time = datetime.datetime.now()
            additional_duration = (end_time - start_time).total_seconds() // 60 
            if row[1]:
                real_duration = row[2] + additional_duration
            else:
                real_duration = additional_duration
            self.cursor.execute("""
                UPDATE tasks 
                SET end_time = ?, real_duration = ?, status = 'completed' 
                WHERE id = ?
            """, (end_time.isoformat(), real_duration, task_id))
            self.conn.commit()
            print(f"Task {task_id} completed. Total duration: {format_duration(int(real_duration))}.")
        else:
            print("Task was never started.")

    def get_tasks_for_today(self):
        """Fetches tasks that have a do_date of today."""
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM tasks WHERE do_date = ?", (today_date,))
        tasks = self.cursor.fetchall()
        return [Task.from_tuple(task) for task in tasks]
        

    def get_overdue_tasks(self):
        """Fetches tasks that are overdue (past due_date and not completed)."""
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT * FROM tasks 
            WHERE due_date < ? AND status != 'completed'
            ORDER BY due_date ASC
        """, (today_date,))
        
        tasks = self.cursor.fetchall()
        return [Task.from_tuple(task) for task in tasks]
    
    def get_reschedule_tasks(self):
        """Fetches tasks that need to be rescheduled (past do_date and not completed)."""
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT * FROM tasks 
            WHERE do_date < ? AND status != 'completed'
            ORDER BY do_date ASC
        """, (today_date,))
        
        tasks = self.cursor.fetchall()
        return [Task.from_tuple(task) for task in tasks]

    def close(self):
        """Closes the database connection."""
        self.conn.close()

    def add_task_interactive(self):
        """Interactive function to add a new task via CLI input."""
        print("\nAdd a New Task\n" + "-" * 20)
        name = input("Task Name (*): ").strip()
        while not name:
            print("ERROR: Task name cannot be empty.")
            name = input("Task Name (*): ").strip()
        description = input("Description: ").strip() or None
        status = "incomplete"
        signifier = input("Signifier: ").strip() or None
        do_date = input("Do Date (YYYY-MM-DD): ").strip() or None
        due_date = input("Due Date (YYYY-MM-DD): ").strip() or None
        category = input("Category: ").strip() or None
        estimated_duration = input("Estimated Duration (minutes): ").strip()
        estimated_duration = int(estimated_duration) if estimated_duration.isdigit() else None
        manager = TaskManager()
        task_id = manager.add_task(
            name=name, description=description, status=status,
            signifier=signifier, do_date=do_date, due_date=due_date, category=category,
            estimated_duration=estimated_duration
        )
        print(f"\nSUCCESS: '{name}' added successfully with ID: {task_id}")
        manager.close()

    def update_task_interactive(self):
        """Updates an existing task interactively."""
        manager = TaskManager()
        task_id = input("Enter Task ID to update: ").strip()
        if not task_id.isdigit():
            print("ERROR: Invalid Task ID.")
            return
        task = manager.get_task_by_id(int(task_id))
        if not task:
            print("ERROR: Task not found.")
            return
        print(f"\nEditing Task: {task.name} (Current Status: {task.status})")
        new_name = input(f"New Name (Press Enter to keep: {task.name}): ").strip() or task.name
        new_description = input("New Description (Press Enter to keep current): ").strip() or task.description
        new_status = input(f"New Status (Press Enter to keep: {task.status}): ").strip() or task.status
        new_category = input(f"New Category (Press Enter to keep: {task.category}): ").strip() or task.category
        manager.update_task(task.id, name=new_name, description=new_description, status=new_status, category=new_category)
        print(f"\nSUCCESS: Task [{task.id}] updated successfully!")
        manager.close()

    def start_task_interactive(self):
        manager = TaskManager()
        task_id = input("Enter Task ID to start: ").strip()
        if not task_id.isdigit():
            print("ERROR: Invalid Task ID.")
            return
        manager.start_task(int(task_id))
        manager.close()

    def pause_task_interactive(self):
        manager = TaskManager()
        task_id = input("Enter Task ID to pause: ").strip()
        if not task_id.isdigit():
            print("ERROR: Invalid Task ID.")
            return
        manager.pause_task(int(task_id))
        manager.close()

    def complete_task_interactive(self):
        manager = TaskManager()
        task_id = input("Enter Task ID to complete: ").strip()
        if not task_id.isdigit():
            print("ERROR: Invalid Task ID.")
            return
        manager.complete_task(int(task_id))
        manager.close()

    def delete_task_interactive(self):
        """Deletes a task by ID."""
        manager = TaskManager()
        task_id = input("Enter Task ID to delete: ").strip()
        if not task_id.isdigit():
            print("ERROR: Invalid Task ID.")
            return
        success = manager.delete_task(int(task_id))
        if success:
            print(f"\nSUCCESS: Task [{task_id}] deleted successfully!")
        else:
            print("ERROR: Task not found.")
        manager.close()

    def show_today_tasks(self):
        """Displays tasks that are due today."""
        manager = TaskManager()
        tasks = manager.get_tasks_for_today()
        manager.close()
        if not tasks:
            print("\nNo tasks for today!")
            return
        print("\nTasks for Today\n" + "-" * 40)
        for task in tasks:
            TASK_FORMAT(task)

    def show_overdue_tasks(self):
        """Displays overdue tasks that are not completed."""
        manager = TaskManager()
        tasks = manager.get_overdue_tasks()
        manager.close()
        if not tasks:
            print("\nNo overdue tasks!")
            return
        print("\nOverdue Tasks\n" + "-" * 40)
        for task in tasks:
            TASK_FORMAT(task)

    def show_reschedule_tasks(self):
        """Displays tasks to be rescheduled."""
        manager = TaskManager()
        tasks = manager.get_reschedule_tasks()
        manager.close()
        if not tasks:
            print("\nNo tasks to reschedule!")
            return
        print("\nTasks to Reschedule\n" + "-" * 40)
        for task in tasks:
            TASK_FORMAT(task)