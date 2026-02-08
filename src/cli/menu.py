"""CLI layer - Menu display and user interaction.

This module handles all console I/O, menu display, user input,
and output formatting. No business logic is implemented here.
"""

from src.services.task_service import TaskService
from src.domain.task import Task, TaskStatus
from src.utilities.constants import (
    ERROR_INVALID_CHOICE,
    ERROR_INVALID_INPUT,
    SUCCESS_TASK_CREATED,
    SUCCESS_TASK_UPDATED,
    SUCCESS_TASK_DELETED,
    SUCCESS_STATUS_TOGGLED,
    MSG_NO_TASKS
)


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")


def get_user_choice() -> int:
    """Get and validate user's menu choice.

    Returns:
        Valid menu choice (1-6)

    Raises:
        ValueError: If input is invalid
    """
    try:
        choice = int(input("\nEnter choice (1-6): "))
        if choice < 1 or choice > 6:
            raise ValueError(ERROR_INVALID_CHOICE)
        return choice
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(ERROR_INVALID_INPUT)
        raise


def handle_add_task(service: TaskService) -> None:
    """Handle the add task flow.

    Args:
        service: The task service instance
    """
    print("\n--- Add Task ---")
    print(f"Note: Title max {100} characters, Description max {500} characters")

    title = input("\nEnter title: ")
    description = input("Enter description: ")

    try:
        task = service.add_task(title, description)
        print(f"\n{SUCCESS_TASK_CREATED}")
        print(f"Task #{task.id}: {task.title}")
        print(f"Description: {task.description}")
        print(f"Status: Incomplete")
    except ValueError as e:
        print(f"\nError: {e}")
        print("Hint: Make sure both title and description are not empty and within length limits.")


def handle_view_tasks(service: TaskService) -> None:
    """Handle the view tasks flow.

    Args:
        service: The task service instance
    """
    print("\n--- Task List ---")
    tasks = service.list_tasks()

    if not tasks:
        print(MSG_NO_TASKS)
        return

    formatted = format_task_list(tasks)
    print(formatted)


def handle_update_task(service: TaskService) -> None:
    """Handle the update task flow.

    Args:
        service: The task service instance
    """
    print("\n--- Update Task ---")
    print("Tip: Use option 2 to view all tasks and their IDs first")
    print("Note: Leave a field empty to keep its current value")

    # Parse task ID input
    task_id_input = input("\nEnter task ID (number): ")
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\nError: {ERROR_INVALID_INPUT}")
        print("Hint: Task ID should be a number like 1, 2, 3, etc.")
        return

    # Get existing task to show current values
    existing_tasks = service.list_tasks()
    existing_task = next((t for t in existing_tasks if t.id == task_id), None)

    if existing_task:
        print(f"\nCurrent values:")
        print(f"  Title: {existing_task.title}")
        print(f"  Description: {existing_task.description}")
        print("\nEnter new values (or press Enter to keep current):")

    title = input("Enter new title (or press Enter to keep): ")
    description = input("Enter new description (or press Enter to keep): ")

    try:
        task = service.update_task(task_id, title, description)
        print(f"\n{SUCCESS_TASK_UPDATED}")
        print(f"Task #{task.id}: {task.title}")
        print(f"Description: {task.description}")
    except ValueError as e:
        print(f"\nError: {e}")
        print("Hint: Make sure the task ID exists and any provided values are valid.")


def handle_delete_task(service: TaskService) -> None:
    """Handle the delete task flow.

    Args:
        service: The task service instance
    """
    print("\n--- Delete Task ---")
    print("Tip: Use option 2 to view all tasks and their IDs first")
    print("Warning: This action cannot be undone!")

    # Parse task ID input
    task_id_input = input("\nEnter task ID to delete (number): ")
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\nError: {ERROR_INVALID_INPUT}")
        print("Hint: Task ID should be a number like 1, 2, 3, etc.")
        return

    confirm = input("Are you sure you want to delete this task? (yes/no): ").lower()
    if confirm not in ['yes', 'y']:
        print("\nDeletion cancelled.")
        return

    try:
        service.delete_task(task_id)
        print(f"\n{SUCCESS_TASK_DELETED}")
        print(f"Task #{task_id} has been permanently removed.")
    except ValueError as e:
        print(f"\nError: {e}")


def handle_toggle_status(service: TaskService) -> None:
    """Handle the toggle status flow.

    Args:
        service: The task service instance
    """
    print("\n--- Mark Complete/Incomplete ---")
    print("Tip: Use option 2 to view all tasks and their IDs first")

    # Parse task ID input
    task_id_input = input("\nEnter task ID (number): ")
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\nError: {ERROR_INVALID_INPUT}")
        print("Hint: Task ID should be a number like 1, 2, 3, etc.")
        return

    try:
        task = service.toggle_task_status(task_id)
        status_text = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
        print(f"\n{SUCCESS_STATUS_TOGGLED}")
        print(f"Task #{task.id} is now: {status_text}")
    except ValueError as e:
        print(f"\nError: {e}")


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of Task objects (already sorted)

    Returns:
        Formatted string representation of tasks
    """
    lines = []
    current_status = None

    for task in tasks:
        # Add status header when status changes
        if task.status != current_status:
            current_status = task.status
            if task.status == TaskStatus.INCOMPLETE:
                lines.append("\n[Incomplete Tasks]")
            else:
                lines.append("\n[Complete Tasks]")

        # Format task details
        status_text = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
        lines.append(f"#{task.id}: {task.title}")
        lines.append(f"   Description: {task.description}")
        lines.append(f"   Status: {status_text}")

    return "\n".join(lines)
