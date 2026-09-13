from models.task import Task
from services.db import get_db_connection

def parsed_task_id(text: str) -> int | None:
    parts = text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return None
    try:
        return int(parts[1].strip())
    except ValueError:
        return None

def _row_to_task(row):
    return Task(id=row[0], name=row[1], is_completed=row[2])

def find_task(task_id, user_id) -> Task | None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, is_completed FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, user_id)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return _row_to_task(row) if row else None

def find_task_by_name(task_name, user_id) -> Task | None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, is_completed FROM tasks WHERE lower(name) = lower(%s) AND user_id = %s",
        (task_name, user_id)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return _row_to_task(row) if row else None

def get_tasks(user_id) -> list[Task]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, is_completed FROM tasks WHERE user_id = %s ORDER BY id",
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [_row_to_task(row) for row in rows]

def add_task(name, user_id) -> Task:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tasks (name, user_id)
        VALUES (%s, %s)
        RETURNING id, name, is_completed
        """,
        (name, user_id)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return _row_to_task(row)

def complete_task(task_id, user_id) -> Task | None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tasks SET is_completed = TRUE
        WHERE id = %s AND user_id = %s
        RETURNING id, name, is_completed
        """,
        (task_id, user_id,)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return _row_to_task(row) if row else None

def delete_task(task_id, user_id) -> Task | None:
    task = find_task(task_id, user_id)
    if task is None:
        return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, user_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return task