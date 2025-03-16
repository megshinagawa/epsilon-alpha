# epsilon-alpha

## FOLDER STUCTURE 

```graphsql
epsilon-alpha/
│── epsilon_alpha.py        # Main CLI entry point
│── cli/
│   │── __init__.py     # Makes the folder a package
│   │── tasks.py        # Task Manager CLI
│   │── notes.py        # Notes Manager CLI
│   │── habits.py       # Habit Tracker CLI
│── core/
│   │── task_manager.py # Task database logic
│   │── note_manager.py # Notes database logic
│   │── habit_manager.py # Habits database logic
│── database/
│   │── epsilon_alpha.db    # SQLite database
│── utils/
│   │── helpers.py      # Shared helper functions
│── README.md

```