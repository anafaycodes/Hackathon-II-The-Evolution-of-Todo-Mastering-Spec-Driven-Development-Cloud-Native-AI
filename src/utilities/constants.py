"""Constants module for the Todo application.

This module defines application-wide constants including validation limits
and error messages used across all layers.
"""

# Validation limits
MAX_TITLE_LENGTH: int = 100
MAX_DESC_LENGTH: int = 500

# Error messages - Validation
ERROR_EMPTY_TITLE: str = "Title cannot be empty. Please provide a title for your task."
ERROR_EMPTY_DESC: str = "Description cannot be empty. Please provide a description for your task."
ERROR_TITLE_TOO_LONG: str = f"Title is too long! Maximum {MAX_TITLE_LENGTH} characters allowed. Please shorten your title."
ERROR_DESC_TOO_LONG: str = f"Description is too long! Maximum {MAX_DESC_LENGTH} characters allowed. Please shorten your description."

# Error messages - Task operations
ERROR_TASK_NOT_FOUND: str = "Task not found. Please use option 2 to view available tasks and their IDs."
ERROR_INVALID_TASK_ID: str = "Invalid task ID. Please enter a valid task number."

# Error messages - Menu
ERROR_INVALID_CHOICE: str = "Invalid choice. Please enter a number between 1 and 6."
ERROR_INVALID_INPUT: str = "Invalid input. Please enter a number (e.g., 1, 2, 3)."

# Success messages
SUCCESS_TASK_CREATED: str = "Task created successfully"
SUCCESS_TASK_UPDATED: str = "Task updated successfully"
SUCCESS_TASK_DELETED: str = "Task deleted successfully"
SUCCESS_STATUS_TOGGLED: str = "Task status updated successfully"

# Display messages
MSG_NO_TASKS: str = "No tasks found"
MSG_EMPTY_LIST: str = "Your task list is empty"
