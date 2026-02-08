"""Domain layer - Task entity and status definitions.

This module defines the core Task entity and its status enumeration.
These are pure data structures with no business logic.
"""

from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task completion status enumeration.

    Attributes:
        INCOMPLETE: Task is not yet completed
        COMPLETE: Task has been completed
    """
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a todo task.

    This is a pure data structure representing a task entity.
    Business logic and validation are handled in the service layer.

    Attributes:
        id: Unique task identifier (never reused within session)
        title: Short description of the task (1-100 characters)
        description: Detailed explanation of the task (1-500 characters)
        status: Current completion status (INCOMPLETE or COMPLETE)
    """
    id: int
    title: str
    description: str
    status: TaskStatus
