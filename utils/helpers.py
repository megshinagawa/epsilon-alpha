from datetime import datetime

def format_duration(minutes):
    """Converts minutes into HH:MM format."""
    if minutes is None:
        return "00:00"  # Default if no duration is given
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02}:{mins:02}"

def format_time(time_str):
    """Convert ISO time to a readable format."""
    if time_str:
        dt = datetime.fromisoformat(time_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

def print_task(task):
    if task.signifier:
        print(f"{signifier_dict[task.signifier]} [{status_dict[task.status]}] ({task.id}) {task.name}")
    else: 
        print(f"  [{status_dict[task.status]}] ({task.id}) {task.name}")

    line2 = []
    if task.category:
        line2.append(f"# {task.category}")
    if task.description:
        line2.append(f"{task.description}")
    if line2:
        print(f"    {' | '.join(line2)}")
    
    line3 = []
    if task.do_date:
        line3.append(f"{task.do_date}")
    if task.due_date:
        line3.append(f"〆 {task.due_date}")
    # if task.status in timer_status_dict:
    #     line3.append(f"({timer_status_dict[task.status]})")
    if task.estimated_duration and (task.real_duration is None):
        estimate = format_duration(task.estimated_duration)
        line3.append(f"00:00 // {estimate}")
    elif task.estimated_duration and task.real_duration:
        estimate = format_duration(task.estimated_duration)
        real = format_duration(task.real_duration)
        line3.append(f"{real} // {estimate}")
    elif (task.estimated_duration is None) and task.real_duration:
        line3.append(f"{real} // 00:00")
    else:
        line3.append(f"00:00 // 00:00")

    if line3:
        print(f"    {' | '.join(line3)}")
    print("-" * 40)


def print_task_simple(task):
    estimate_duration = format_duration(task.estimated_duration)  
    real_duration = format_duration(task.real_duration)  
    print(f"[{task.id}] {task.name} - {task.status} ({task.do_date or 'Not Scheduled'})")
    if task.category:
        print(f"   # {task.category}")
    if task.description:
        print(f"   {task.description}")
    if task.due_date:
        print(f"   Due: {task.due_date}")
    if task.estimated_duration:
        print(f"   Duration: {real_duration} // {estimate_duration}")
    print("-" * 40)

status_dict = {
    'incomplete':' ',
    'completed' : 'x',
    'in-progress':'/',
    'paused':'^',
    'cancelled':'-'
}

signifier_dict = {
    'important':'*',
    'repeats':'~'
}

timer_status_dict = {
    'in-progress':'>',
    'paused':'='
}