# Task Tracker CLI

A simple command-line task tracking tool written in Python. This tool allows you to manage your tasks by adding, updating, deleting, and marking them as in progress or done. Tasks are stored in a `JSON` file, and each task has a unique ID that is auto-incremented.

## Roadmap Project URL

`https://roadmap.sh/projects/task-tracker`

## Features

- [x] Add, Update, and Delete tasks
- [x] Mark a task as in progress or done
- [x] List all tasks
- [x] List all tasks that are done
- [x] List all tasks that are not done
- [x] List all tasks that are in progress

## Getting Started

### Prerequisites

Ensure you have Python installed (version 3.x).

### Usage

The CLI offers several commands to manage tasks. Below is a breakdown of the commands you can use.

- **Add a new task**

```bash
python task-cli.py add "Task description"
```

- **Update an existing task**

```bash
python task-cli.py update <task_id> "New task description"
```

- **Delete a task**

```bash
python task-cli.py delete <task_id>
```

- **Mark a task as "In Progress"**

```bash
python task-cli.py mark-in-progress <task_id>
```

- **Mark a task as "Done"**

```bash
python task-cli.py mark-done <task_id>
```

- **List all tasks**

```bash
python task-cli.py list
```

- **List tasks by status**
  - Done:

    ```bash
    python task-cli.py list done
    ```

  - To Do:

    ```bash
    python task-cli.py list todo
    ```

  - In Progress:

    ```bash
    python task-cli.py list in-progress
    ```

### Task Storage

Tasks are saved in a tasks.json file in the following format:

```json
{
    "tasks": [
        {
            "id": 0,
            "description": "First task",
            "status": -1,
            "created-at": "26 Sep 2024 14:22:12",
            "updated-at": "26 Sep 2024 14:22:12"
        }
    ],
    "next_id": 1
}
```

### Help

To see the available commands, run:

```bash
python task-cli.py
```
