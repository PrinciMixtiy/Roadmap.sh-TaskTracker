import json
import time

COL_WIDTHS = [5, 40, 15, 25, 25]

HELP_MESSAGE = """\
Task Tracker CLI

Commands:
    add <"task description">
    update <task_id> <"task description">
    delete <task_id>
    
    task-cli mark-in-progress <task_id>
    task-cli mark-done <task_id>

    task-cli list

    task-cli list done
    task-cli list todo
    task-cli list in-progress
"""


def get_current_time():
    return time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time()))


def read_tasks() -> tuple:
    """Extract tasks list and next id from tasks.json file.

    Returns:
        tuple: tasks, next_id
    """
    try:
        with open('tasks.json', 'r') as file:
            try:
                data = json.load(file)
                tasks = data.get("tasks", []) # Default empty list if no task
                next_id = data.get("next_id", 0)  # Default to 0 if not present
            except json.JSONDecodeError:
                tasks = []
                next_id = 0
    except FileNotFoundError:
        tasks = []
        next_id = 0

    return tasks, next_id


def write_tasks(tasks: list, next_id: int):
    """Write tasks list and next id to tasks.json file.

    Args:
        tasks (list): Tasks list
        next_id (int): next id
    """
    with open('tasks.json', 'w') as file:
        json.dump({"tasks": tasks, "next_id": next_id}, file, indent=4)


def get_status(code: int):
    match code:
        case 1:
            return 'Done'
        case 0:
            return 'In Progress'
        case -1:
            return 'Todo'
        case _:
            return 'Undefined'


def print_table_title():
    print(f"{'ID':<{COL_WIDTHS[0]}}" +
          f"{'Description':<{COL_WIDTHS[1]}}" +
          f"{'Status':<{COL_WIDTHS[2]}}" +
          f"{'Created At':<{COL_WIDTHS[3]}}" +
          f"{'Updated At':>{COL_WIDTHS[4]}}")

    print("-" * sum(COL_WIDTHS))


def print_tasks(tasks: list):
    print_table_title()

    for task in tasks:
        print(f"{task['id']:<{COL_WIDTHS[0]}}" +
              f"{task['description']:<{COL_WIDTHS[1]}}" +
              f"{get_status(task['status']):<{COL_WIDTHS[2]}}" +
              f"{task['created-at']:<{COL_WIDTHS[3]}}" +
              f"{task['updated-at']:>{COL_WIDTHS[4]}}"
              )


def add_task(description: str) -> None:
    """Add new task to tasks.json

    Args:
        description (str): Task description
    """
    tasks, next_id = read_tasks()

    new_task = {
        "id": next_id,
        "description": description,
        # Status: | -1 => todo | 0 => in progress | 1 => done
        "status": -1,
        "created-at": get_current_time(),
        "updated-at": get_current_time()
    }

    tasks.append(new_task)
    next_id += 1  # Increment the next_id for the future task
    write_tasks(tasks, next_id)

    print(f'New task added. ID: {new_task["id"]}')


def update_task(id: int, description: str) -> None:
    """Update existing task.

    Args:
        id (int): Task ID
        description (str): New description
    """
    tasks, next_id = read_tasks()

    for task in tasks:
        if task["id"] == id:
            task["description"] = description
            task["updated-at"] = get_current_time()
            write_tasks(tasks, next_id)
            print(f'Task {id} updated.')
            return

    print(f"No task with ID: {id}")


def delete_task(id: int):
    """Delete a task.

    Args:
        id (int): Task ID
    """
    tasks, next_id = read_tasks()

    tasks = [task for task in tasks if task["id"] != id]

    write_tasks(tasks, next_id)
    print(f"Task {id} removed.")


def mark_in_progress(id: int):
    """Mark a task as in progress.

    Args:
        id (int): Task ID
    """
    tasks, next_id = read_tasks()

    for task in tasks:
        if task['id'] == id:
            task['status'] = 0
            write_tasks(tasks, next_id)
            print(f"Task {id} marked as in progress.")
            return

    print(f"No task with ID: {id}")


def mark_done(id: int):
    """Mark a task as done.

    Args:
        id (int): Task ID
    """
    tasks, next_id = read_tasks()

    for task in tasks:
        if task['id'] == id:
            task['status'] = 1
            write_tasks(tasks, next_id)
            print(f"Task {id} marked as done.")
            return

    print(f"No task with ID: {id}")


def list_tasks():
    tasks, _ = read_tasks()

    if tasks:
        print('ALL TASKS\n')
        print_tasks(tasks)
    else:
        print("No task.")


def list_done_tasks():
    tasks, _ = read_tasks()
    tasks = filter(lambda task: task['status'] == 1, tasks)

    if tasks:
        print('TASKS DONE\n')
        print_tasks(list(tasks))
    else:
        print("No task done.")


def list_todo_tasks():
    tasks, _ = read_tasks()
    tasks = filter(lambda task: task['status'] == -1, tasks)

    if tasks:
        print('TASKS TO DO\n')
        print_tasks(list(tasks))
    else:
        print("No task to do.")


def list_in_progress_tasks():
    tasks, _ = read_tasks()
    tasks = filter(lambda task: task['status'] == 0, tasks)

    if tasks:
        print('TASKS IN PROGRESS\n')
        print_tasks(list(tasks))
    else:
        print("No task in progress.")


if __name__ == "__main__":
    import sys

    # If a command is passed.
    if not len(sys.argv) <= 1:

        # Add Task Command
        if sys.argv[1] == 'add':
            # If a description parameter is passed.
            if len(sys.argv) == 3:
                add_task(sys.argv[2])
            # If zero or more than one parameters.
            else:
                print("COMMAND ERROR")
                print(HELP_MESSAGE)

        # Update Task Command
        elif sys.argv[1] == 'update':
            if len(sys.argv) == 4:
                try:
                    id = int(sys.argv[2])
                except ValueError:
                    print(f'ERROR: ID parameter [{sys.argv[2]}] not an Integer.')
                    print(HELP_MESSAGE)
                else:
                    update_task(id, sys.argv[3])

            else:
                print("COMMAND ERROR")
                print(HELP_MESSAGE)

        # Delete Task Command
        elif sys.argv[1] == 'delete':
            if len(sys.argv) == 3:
                try:
                    id = int(sys.argv[2])
                except ValueError:
                    print(f'ERROR: ID parameter [{sys.argv[2]}] not an Integer.')
                    print(HELP_MESSAGE)
                else:
                    delete_task(id)

            else:
                print("COMMAND ERROR")
                print(HELP_MESSAGE)
                
        # Mark Task as In Progress Command
        elif len(sys.argv) == 3 and sys.argv[1] == 'mark-in-progress':
            try:
                id = int(sys.argv[2])
            except ValueError:
                print(f'ERROR: ID parameter [{sys.argv[2]}] not an Integer.')
                print(HELP_MESSAGE)
            else:
                mark_in_progress(id)
                
        # Mark Task as Done Command
        elif len(sys.argv) == 3 and sys.argv[1] == 'mark-done':
            try:
                id = int(sys.argv[2])
            except ValueError:
                print(f'ERROR: ID parameter [{sys.argv[2]}] not an Integer.')
                print(HELP_MESSAGE)
            else:
                mark_done(id)
            

        # Listing Tasks Commands
        elif sys.argv[1] == 'list':
            if len(sys.argv) == 2:
                list_tasks()
                
            elif len(sys.argv) == 3:
                if sys.argv[2] == 'done':
                    list_done_tasks()
                if sys.argv[2] == 'todo':
                    list_todo_tasks()
                if sys.argv[2] == 'in-progress':
                    list_in_progress_tasks()
                    
            else:
                print("COMMAND ERROR")
                print(HELP_MESSAGE)
                
        else:
            print("COMMAND ERROR")
            print(HELP_MESSAGE)

    else:
        print(HELP_MESSAGE)
