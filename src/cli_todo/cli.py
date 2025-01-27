import os
import sys
from typing import List, Optional


DEFAULT_FILENAME = ".todo"
DEFAULT_FILEPATH = os.path.join(os.path.expanduser("~"), DEFAULT_FILENAME)


def eprint(msg: str) -> None:
    print("Error: %s" % (msg,), file=sys.stderr)


def print_usage(program: str) -> None:
    print(
        "Todo list manager\n\n"
        "Usage:\n"
        "  %s <command> [arguments]\n\n"
        "Commands:\n"
        "  help           Display this help message\n"
        "  list           Show all tasks in the todo list\n"
        "  add <title>    Add a new task with the specified title\n"
        "  remove <id>    Remove task with specified ID\n\n"
        "Examples:\n"
        "  %s list\n"
        "  %s add 'Buy milk'\n"
        "  %s remove 0\n"
        % (program, program, program, program)
    )


class Todo:
    __slots__ = ("id", "title")
    
    def __init__(self, title: str, *, id: Optional[int] = None) -> None:
        self.id = id if id is not None else 0
        self.title = title

    def __repr__(self) -> str:
        return "Todo(id=%d, title=%s)" % (self.id, repr(self.title))


class TodoFile:
    __slots__ = ("_items", "_file", "filepath")
    
    def __init__(self, filepath: str = DEFAULT_FILEPATH) -> None:
        self._items: List[Todo] = []
        self._file = None

        self.filepath = filepath

    def __str__(self) -> str:
        if not self._items:
            return "Your todo list is empty"

        output = ["Todo List:"]
        for item in self._items:
            output.append("  %d. %s" % (item.id, item.title))

        return "\n".join(output)

    def open(self) -> None:
        try:
            if self._file is None:
                self._file = open(self.filepath, "a+")
                self._file.seek(0)
                self._items = self._parse_data(self._file.read())
        except IOError as err:
            eprint("Failed to load todo file: %s" % (str(err),))
            self._items = []

    def close(self) -> None:
        if self._file:
            try:
                self._file.seek(0)
                self._file.truncate()
                self._file.write(self._encode_data())
            finally:
                self._file.close()
                self._file = None

    def _parse_data(self, raw_data: str) -> List[Todo]:
        if not raw_data.strip():
            return []
            
        items = []
        for section in raw_data.split(";"):
            if not section.strip():
                continue
            try:
                item_id, title = section.split(".", 1)
                items.append(Todo(title=title, id=int(item_id)))
            except (ValueError, IndexError):
                eprint("Skipping invalid entry: %s" % (section,))
        return items

    def _encode_data(self) -> str:
        return ";".join("%d.%s" % (item.id, item.title) for item in self._items)

    def append(self, item: Todo) -> None:
        item.id = len(self._items)
        self._items.append(item)

    def remove(self, item_id: int) -> bool:
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                del self._items[idx]
                for i, todo in enumerate(self._items[idx:]):
                    todo.id = idx + i
                return True
        return False


def app() -> None:
    program, *args = sys.argv
    program = os.path.basename(program)

    if not args:
        print_usage(program)
        sys.exit(1)

    command = args[0].lower()
    todo_file = TodoFile()
    try:
        todo_file.open()
        
        if command == "help":
            print_usage(program)
        elif command == "list":
            print(todo_file)
        elif command == "add":
            if len(args) < 2:
                eprint("Missing task title")
            else:
                todo_file.append(Todo(" ".join(args[1:])))
                print(todo_file)
        elif command == "remove":
            if len(args) < 2:
                eprint("Missing task id")
            else:
                try:
                    item_id = int(args[1])
                    if todo_file.remove(item_id):
                        print(todo_file)
                    else:
                        eprint("Task with id %s not found" % (item_id,))
                except ValueError:
                    eprint("Invalid task id - must be integer")
        else:
            eprint("Unknown command: %s" % (command,))
    except Exception as err:
        eprint("Unexpected error: %s" % (str(err),))
        sys.exit(2)
    finally:
        todo_file.close()
    

if __name__ == "__main__":
    app()
