"""Storage layer - In-memory task storage implementation.

This module provides CRUD operations for tasks using an in-memory dictionary.
Task IDs are generated sequentially starting from 1 and never reused.
"""

from typing import Optional
from src.domain.task import Task, TaskStatus


class InMemoryTaskStore:
    """In-memory storage for tasks using a dictionary.

    This class maintains tasks in memory and provides CRUD operations.
    Task IDs are generated sequentially and never reused, even after deletion.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str) -> Task:
        """Create and store a new task with a unique ID.

        Args:
            title: Task title (already validated)
            description: Task description (already validated)

        Returns:
            The newly created Task object with assigned ID
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status=TaskStatus.INCOMPLETE
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all Task objects (unsorted)
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: str, description: str) -> Task:
        """Update an existing task's title and description.

        Args:
            task_id: The unique task identifier
            title: New task title (already validated)
            description: New task description (already validated)

        Returns:
            The updated Task object

        Raises:
            KeyError: If task_id does not exist
        """
        task = self._tasks[task_id]
        task.title = title
        task.description = description
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The unique task identifier

        Raises:
            KeyError: If task_id does not exist
        """
        del self._tasks[task_id]

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggle a task's status between INCOMPLETE and COMPLETE.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task object

        Raises:
            KeyError: If task_id does not exist
        """
        task = self._tasks[task_id]
        if task.status == TaskStatus.INCOMPLETE:
            task.status = TaskStatus.COMPLETE
        else:
            task.status = TaskStatus.INCOMPLETE
        return task
