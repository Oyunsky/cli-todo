# Todo List Manager

**Todo List Manager** - is a simple console utility for managing the task list.

## Installation

```console
python -m pip install git+https://github.com/Oyunsky/cli-todo.git
```

## Usage

Once installed, you can use the `todo` command to manage tasks.

```console
>>> todo
Todo list manager

Usage:
  todo <command> [arguments]

Commands:
  help           Display this help message
  list           Show all tasks in the todo list
  add <title>    Add a new task with the specified title
  remove <id>    Remove task with specified ID

Examples:
  todo list
  todo add 'Buy milk'
  todo remove 0
```

**list**: show all tasks in the todo list.

```console
>>> todo list
Your todo list is empty
```

**add**: add a new task with the specified title.

```console
>>> todo add "Buy milk"
Todo list:
  0. Buy milk
```

**remove**: remove task with specified id.

```console
>>> todo remove 0
Your todo list is empty
```
