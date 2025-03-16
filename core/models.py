class Task:
    def __init__(
        self, task_id, name, description="", status="incomplete",
        signifier=None, do_date=None, due_date=None, category=None, estimated_duration=None,
        real_duration=None, start_time=None, end_time=None
    ):
        """
        Represents a Task object.

        :param task_id: Unique ID from SQLite (Primary Key).
        :param name: Name of the task (Required).
        :param description: Optional description.
        :param status: Task status (incomplete, in-progress, paused, cancelled, completed).
        :param signifier: Special marker for the task.
        :param do_date: Do date as a string (YYYY-MM-DD) or None.
        :param due_date: Due date as a string (YYYY-MM-DD) or None.
        :param category: Task category (e.g., Work, Personal, School).
        :param estimated_duration: Estimated time to complete (in minutes).
        :param real_duration: Actual time spent on the task (in minutes).
        :param start_time: Timestamp when task started.
        :param end_time: Timestamp when task was completed.
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.signifier = signifier
        self.do_date = do_date
        self.due_date = due_date
        self.category = category
        self.estimated_duration = estimated_duration
        self.real_duration = real_duration
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        """String representation for debugging."""
        return f"Task(id={self.id}, name='{self.name}', status='{self.status}')"

    def to_dict(self):
        """Converts the Task object to a dictionary (useful for JSON or API handling)."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "signifier": self.signifier,
            "do_date": self.do_date,
            "due_date": self.due_date,
            "category": self.category,
            "estimated_duration": self.estimated_duration,
            "real_duration": self.real_duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_tuple(cls, task_tuple):
        """Converts a database row (tuple) into a Task object."""
        return cls(*task_tuple)
