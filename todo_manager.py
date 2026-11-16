"""To-Do List Manager
Syntecxhub Python Programming Internship - Task 1, Project 3

A menu-driven command-line app that adds, views, deletes and completes
tasks. Tasks are saved to tasks.json so they survive restarts.
Extra credit: tags and due dates.
"""

import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


# ---------------------------------------------------------------
# File handling (I/O)
# ---------------------------------------------------------------
def load_tasks(path=DATA_FILE):
    """Load tasks from a JSON file. Returns an empty list if needed."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read saved tasks. Starting fresh.")
        return []


def save_tasks(tasks, path=DATA_FILE):
    """Save tasks to a JSON file. Returns True on success."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
        return True
    except OSError as error:
        print(f"Error: could not save tasks ({error}).")
        return False


# ---------------------------------------------------------------
# Logic (no input/print here, so it is easy to test)
# ---------------------------------------------------------------
def next_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def is_valid_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task(tasks, title, tag="", due=""):
    task = {
        "id": next_id(tasks),
        "title": title.strip(),
        "done": False,
        "tag": tag.strip(),
        "due": due.strip(),
    }
    tasks.append(task)
    return task


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        return False
    tasks.remove(task)
    return True


def mark_done(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        return False
    task["done"] = True
    return True


# ---------------------------------------------------------------
# User interface (input/print)
# ---------------------------------------------------------------
def show_menu():
    print("\n===== TO-DO LIST MANAGER =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Exit")


def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet.")
        return
    print("\nID  Status  Task")
    print("-" * 40)
    for task in tasks:
        status = "[x]" if task["done"] else "[ ]"
        extras = []
        if task["tag"]:
            extras.append(f"#{task['tag']}")
        if task["due"]:
            extras.append(f"due {task['due']}")
        extra_text = f"  ({', '.join(extras)})" if extras else ""
        print(f"{task['id']:<3} {status:<7} {task['title']}{extra_text}")


def read_task_id(prompt):
    """Ask for a task ID; return an int or None if invalid."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None


def handle_add(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    tag = input("Tag (optional, press Enter to skip): ")
    due = input("Due date YYYY-MM-DD (optional): ").strip()
    if due and not is_valid_date(due):
        print("Invalid date format. Task not added.")
        return
    add_task(tasks, title, tag, due)
    save_tasks(tasks)
    print("Task added.")


def handle_mark_done(tasks):
    display_tasks(tasks)
    task_id = read_task_id("Enter task ID to mark as done: ")
    if task_id is None:
        return
    if mark_done(tasks, task_id):
        save_tasks(tasks)
        print("Task marked as done.")
    else:
        print("Task not found.")


def handle_delete(tasks):
    display_tasks(tasks)
    task_id = read_task_id("Enter task ID to delete: ")
    if task_id is None:
        return
    if delete_task(tasks, task_id):
        save_tasks(tasks)
        print("Task deleted.")
    else:
        print("Task not found.")


def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            handle_add(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            handle_mark_done(tasks)
        elif choice == "4":
            handle_delete(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()