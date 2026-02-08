# Todo In-Memory Python Console App

A simple, elegant command-line todo application built with clean architecture principles and spec-driven development.

## Features

- ✅ **Create Tasks**: Add tasks with titles and descriptions
- 📋 **View Tasks**: See all tasks sorted by status (incomplete first)
- ✏️ **Update Tasks**: Edit task titles and descriptions
- ✓ **Mark Complete**: Toggle tasks between complete and incomplete
- 🗑️ **Delete Tasks**: Remove tasks you no longer need
- 💾 **In-Memory Storage**: Fast, lightweight (data resets on exit)

## Quick Start

### Prerequisites

- Python 3.13+ (or Python 3.10+ with compatible type hints)
- No external dependencies required (uses standard library only)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Phase-1
   ```

2. Run the application:
   ```bash
   python -m src.main
   ```

### Usage

The application presents a menu-driven interface:

```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit
```

#### Example Session

```bash
# Add a task
Enter choice (1-6): 1
Enter title: Buy groceries
Enter description: Milk, eggs, bread

# View tasks
Enter choice (1-6): 2
[Incomplete Tasks]
#1: Buy groceries
   Description: Milk, eggs, bread
   Status: Incomplete

# Mark complete
Enter choice (1-6): 5
Enter task ID: 1
Task #1 is now: Complete

# Exit
Enter choice (1-6): 6
Goodbye!
```

## Architecture

The application follows a clean 5-layer architecture:

```
┌─────────────────────────────────────┐
│         CLI Layer (menu.py)         │  User interaction
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Service Layer (task_service.py)  │  Business logic
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼─────┐   ┌─────▼──────────────┐
│   Domain   │   │  Storage Layer     │
│  (task.py) │   │ (memory_store.py)  │
└────────────┘   └────────────────────┘
       │                │
       └───────┬────────┘
               │
┌──────────────▼──────────────────────┐
│   Utilities (constants.py)          │  Shared constants
└─────────────────────────────────────┘
```

### Layer Responsibilities

- **CLI Layer**: User interaction, input/output formatting
- **Service Layer**: Business logic, validation, orchestration
- **Domain Layer**: Core entities (Task, TaskStatus)
- **Storage Layer**: Data persistence (in-memory dictionary)
- **Utilities Layer**: Shared constants and error messages

## Project Structure

```
Phase-1/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   └── menu.py          # User interface
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task.py          # Task entity
│   ├── storage/
│   │   ├── __init__.py
│   │   └── memory_store.py  # In-memory storage
│   └── utilities/
│       ├── __init__.py
│       └── constants.py     # Constants
├── specs/                   # Feature specifications
├── history/                 # Development history
├── .specify/               # Spec-Kit Plus templates
└── README.md               # This file
```

## Validation Rules

- **Title**: 1-100 characters, non-empty
- **Description**: 1-500 characters, non-empty
- **Task IDs**: Unique integers starting from 1, never reused
- **Newlines**: Automatically converted to spaces for display

## Development

### Code Quality Standards

This project follows strict clean code principles:

- ✅ Functions ≤25 lines (with documented exceptions)
- ✅ Complete type hints on all public functions
- ✅ Google-style docstrings
- ✅ Single responsibility per function/class
- ✅ No circular dependencies
- ✅ Proper layer boundaries

### Running Tests

```bash
# Run acceptance tests
python -c "from src.storage.memory_store import InMemoryTaskStore; ..."

# Run clean code validation
python -c "import ast; from pathlib import Path; ..."
```

See `specs/001-todo-app/tasks.md` for detailed test scenarios.

## Limitations

- **No Persistence**: Data is lost when the application exits (by design)
- **Single User**: No multi-user support or concurrent access
- **Console Only**: No GUI or web interface
- **In-Memory Only**: No database or file storage

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is part of a spec-driven development demonstration.

## Acknowledgments

Built using:
- **Spec-Kit Plus**: Spec-driven development framework
- **Claude Code**: AI-assisted development
- **Python 3.13**: Modern Python with enhanced type hints

---

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: 2026-01-30
