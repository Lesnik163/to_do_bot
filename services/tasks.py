from models.task import Task

tasks = []

def parsed_task_id(text: str) -> int | None:
    parts = text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return None
    try:
        return int(parts[1].strip())
    except ValueError:
        return None

def find_task(task_id: int) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None

def find_task_by_name(task_name: str) -> Task | None:
    name = task_name.strip().lower()
    for task in tasks:
        if task.name.strip().lower() == name:
            return task
    return None