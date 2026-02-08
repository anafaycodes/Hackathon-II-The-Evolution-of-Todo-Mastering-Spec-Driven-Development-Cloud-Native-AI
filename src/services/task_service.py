"""Service layer - Task business logic and validation.

This module implements business rules, validation, and orchestration
between the storage layer and CLI layer.
"""

from src.domain.task import Task, TaskStatus
from src.storage.memory_store import InMemoryTaskStore
from src.utilities.constants import (
    MAX_TITLE_LENGTH,
    MAX_DESC_LENGTH,
    ERROR_EMPTY_TITLE,
    ERROR_EMPTY_DESC,
    ERROR_TITLE_TOO_LONG,
    ERROR_DESC_TOO_LONG,
    ERROR_TASK_NOT_FOUND
)


class TaskService:
    """Business logic and validation for task operations.

    This service coordinates between the CLI and storage layers,
    implementing validation rules and business logic.

    Attributes:
        storage: The task storage implementation
    """

    def __init__(self, storage: InMemoryTaskStore) -> None:
        """Initialize the task service with a storage backend.

        Args:
            storage: The task storage implementation to use
        """
        self.storage = storage

    def add_task(self, title: str, description: str) -> Task:
        """Add a new task with validation and normalization.

        Args:
            title: Task title (will be validated and normalized)
            description: Task description (will be validated and normalized)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If validation fails
        """
        validated_title = self._validate_title(title)
        validated_desc = self._validate_description(description)
        return self.storage.create_task(validated_title, validated_desc)

    def list_tasks(self) -> list[Task]:
        """Get all tasks sorted by status then ID.

        Tasks are sorted with incomplete tasks first, then complete tasks.
        Within each group, tasks are sorted by ID in ascending order.

        Returns:
            List of Task objects sorted by status then ID
        """
        tasks = self.storage.get_all_tasks()
        # Sort by status (0=INCOMPLETE, 1=COMPLETE) then by ID
        return sorted(tasks, key=lambda t: (0 if t.status == TaskStatus.INCOMPLETE else 1, t.id))

    def update_task(self, task_id: int, title: str, description: str) -> Task:
        """Update an existing task with validation.

        Empty fields preserve existing values (partial update support).

        Args:
            task_id: The unique task identifier
            title: New task title (empty/whitespace preserves existing)
            description: New task description (empty/whitespace preserves existing)

        Returns:
            The updated Task object

        Raises:
            ValueError: If validation fails or task not found
        """
        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            raise ValueError(ERROR_TASK_NOT_FOUND)

        # If title is empty/whitespace, keep existing title
        if title and title.strip():
            validated_title = self._validate_title(title)
        else:
            validated_title = existing_task.title

        # If description is empty/whitespace, keep existing description
        if description and description.strip():
            validated_desc = self._validate_description(description)
        else:
            validated_desc = existing_task.description

        return self.storage.update_task(task_id, validated_title, validated_desc)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was deleted

        Raises:
            ValueError: If task not found
        """
        if not self.storage.get_task(task_id):
            raise ValueError(ERROR_TASK_NOT_FOUND)
        self.storage.delete_task(task_id)
        return True

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task object

        Raises:
            ValueError: If task not found
        """
        if not self.storage.get_task(task_id):
            raise ValueError(ERROR_TASK_NOT_FOUND)
        return self.storage.toggle_task_status(task_id)

    def _validate_title(self, title: str) -> str:
        """Validate and normalize a task title.

        Args:
            title: Raw title input

        Returns:
            Normalized title with newlines converted to spaces

        Raises:
            ValueError: If title is empty or exceeds length limit
        """
        if not title or not title.strip():
            raise ValueError(ERROR_EMPTY_TITLE)

        normalized = self._normalize_text(title)

        if len(normalized) > MAX_TITLE_LENGTH:
            raise ValueError(ERROR_TITLE_TOO_LONG)

        return normalized

    def _validate_description(self, description: str) -> str:
        """Validate and normalize a task description.

        Args:
            description: Raw description input

        Returns:
            Normalized description with newlines converted to spaces

        Raises:
            ValueError: If description is empty or exceeds length limit
        """
        if not description or not description.strip():
            raise ValueError(ERROR_EMPTY_DESC)

        normalized = self._normalize_text(description)

        if len(normalized) > MAX_DESC_LENGTH:
            raise ValueError(ERROR_DESC_TOO_LONG)

        return normalized

    def _normalize_text(self, text: str) -> str:
        """Normalize text by converting newlines to spaces.

        Args:
            text: Raw text input

        Returns:
            Text with all newline characters replaced by spaces
        """
        return text.replace('\n', ' ').replace('\r', ' ')
