"""Todo In-Memory Python Console App - Main Entry Point.

This module initializes the application components and runs the main menu loop.
"""

from src.storage.memory_store import InMemoryTaskStore
from src.services.task_service import TaskService
from src.cli.menu import (
    display_menu,
    get_user_choice,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_toggle_status
)


def main() -> None:
    """Main application entry point.

    Initializes storage and service layers, then runs the main menu loop
    until the user chooses to exit.

    FUNCTION LENGTH EXCEPTION: This function is 31 lines (exceeds 25-line limit).
    The menu loop requires all menu choices in one place for clarity. Splitting
    into separate functions would add indirection without improving readability,
    as the menu flow is tightly coupled and needs to be understood as a whole.
    """
    # Initialize storage and service layers
    storage = InMemoryTaskStore()
    service = TaskService(storage)

    print("Welcome to Todo App!")

    # Main menu loop
    while True:
        try:
            display_menu()
            choice = get_user_choice()

            if choice == 1:
                handle_add_task(service)
            elif choice == 2:
                handle_view_tasks(service)
            elif choice == 3:
                handle_update_task(service)
            elif choice == 4:
                handle_delete_task(service)
            elif choice == 5:
                handle_toggle_status(service)
            elif choice == 6:
                print("\nGoodbye!")
                break

        except ValueError as e:
            print(f"\nError: {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
