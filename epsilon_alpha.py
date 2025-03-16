import argparse
from cli import tasks, notes, habits

def main():
    parser = argparse.ArgumentParser(description="Life Assistant CLI")
    subparsers = parser.add_subparsers(dest="module")

    # Task Manager Commands
    task_parser = subparsers.add_parser("tasks", help="Manage tasks")
    task_parser.add_argument("command", choices=["add", "list", "today", "overdue", "complete"], help="Task command")
    task_parser.add_argument("task_id", nargs="?", help="Task ID (if needed)")

    # Notes Manager Commands
    note_parser = subparsers.add_parser("notes", help="Manage notes")
    note_parser.add_argument("command", choices=["add", "list", "delete"], help="Note command")

    # Habit Tracker Commands
    habit_parser = subparsers.add_parser("habits", help="Manage habits")
    habit_parser.add_argument("command", choices=["add", "track", "list"], help="Habit command")

    args = parser.parse_args()

    # Delegate command execution
    if args.module == "tasks":
        tasks.handle_task_command(args)
    # elif args.module == "notes":
    #     notes.handle_note_command(args)
    # elif args.module == "habits":
    #     habits.handle_habit_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
