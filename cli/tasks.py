from core.task_manager import TaskManager

def handle_task_command(args):
    manager = TaskManager()

    if args.command == "add":
        manager.add_task_interactive()
    elif args.command == "delete":
        manager.delete_task_interactive()
    elif args.command == "update":
        manager.update_task_interactive()
    elif args.command == "start":
        manager.start_task_interactive()
    elif args.command == "pause":
        manager.pause_task_interactive()
    elif args.command == "complete":
        manager.complete_task_interactive()
    elif args.command == "list":
        manager.list_tasks()
    elif args.command == "today":
        manager.show_today_tasks()
    elif args.command == "overdue":
        manager.show_overdue_tasks()
    elif args.command == "reschedule":
        manager.show_reschedule_tasks()
    
    manager.close()