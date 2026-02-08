# Manual Testing Guide - Todo App

## Quick Test

Run the application:
```bash
cd "E:\Hackathon II\Phase-1"
python -m src.main
```

## Test Scenarios

### Scenario 1: Basic Task Creation and Viewing

**Steps:**
1. Start the app
2. Select option `1` (Add Task)
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread`
5. Select option `2` (View Tasks)

**Expected Result:**
- Task #1 appears with title, description, and "Incomplete" status
- Task is displayed under "[Incomplete Tasks]" section

### Scenario 2: Mark Task Complete

**Steps:**
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `1`
3. Select option `2` (View Tasks)

**Expected Result:**
- Task #1 now shows "Complete" status
- Task appears under "[Complete Tasks]" section

### Scenario 3: Update Task

**Steps:**
1. Select option `3` (Update Task)
2. Enter task ID: `1`
3. Enter new title: `Buy groceries and supplies`
4. Enter new description: `Milk, eggs, bread, and cleaning supplies`
5. Select option `2` (View Tasks)

**Expected Result:**
- Task #1 shows updated title and description
- Status remains "Complete"

### Scenario 4: Create Multiple Tasks and Verify Sorting

**Steps:**
1. Select option `1` (Add Task)
2. Create task #2: `Write report` / `Q4 financial summary`
3. Select option `1` (Add Task)
4. Create task #3: `Call dentist` / `Schedule checkup`
5. Select option `5` (Mark Complete/Incomplete)
6. Mark task #2 as complete (ID: 2)
7. Select option `2` (View Tasks)

**Expected Result:**
- Incomplete tasks appear first: #3
- Complete tasks appear second: #1, #2
- Within each group, tasks sorted by ID

### Scenario 5: Delete Task

**Steps:**
1. Select option `4` (Delete Task)
2. Enter task ID: `3`
3. Select option `2` (View Tasks)

**Expected Result:**
- Task #3 no longer appears
- Tasks #1 and #2 still present

### Scenario 6: Validation Testing

**Test 6a: Empty Title**
1. Select option `1` (Add Task)
2. Enter title: `` (press Enter without typing)
3. Enter description: `Test description`

**Expected**: Error message "Title cannot be empty"

**Test 6b: Empty Description**
1. Select option `1` (Add Task)
2. Enter title: `Test title`
3. Enter description: `` (press Enter without typing)

**Expected**: Error message "Description cannot be empty"

**Test 6c: Title Too Long**
1. Select option `1` (Add Task)
2. Enter title: (101+ characters)
3. Enter description: `Test`

**Expected**: Error message "Title cannot exceed 100 characters"

**Test 6d: Invalid Task ID**
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `999`

**Expected**: Error message "Task not found"

**Test 6e: Non-numeric Task ID**
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `abc`

**Expected**: Error message "Please enter a valid number"

**Test 6f: Invalid Menu Choice**
1. At main menu, enter: `7`

**Expected**: Error message "Invalid choice. Please enter a number between 1 and 6"

### Scenario 7: Newline Handling

**Steps:**
1. Select option `1` (Add Task)
2. Enter title: `Multi
line
title` (with actual newlines)
3. Enter description: `Multi
line
description`
4. Select option `2` (View Tasks)

**Expected Result:**
- Newlines converted to spaces
- Title displays as: `Multi line title`
- Description displays as: `Multi line description`

### Scenario 8: Unicode Support

**Steps:**
1. Select option `1` (Add Task)
2. Enter title: `Café meeting ☕`
3. Enter description: `Discuss project über details 🚀`
4. Select option `2` (View Tasks)

**Expected Result:**
- Unicode characters display correctly
- Emojis preserved (if terminal supports)

### Scenario 9: ID Never Reused

**Steps:**
1. Create task #1
2. Create task #2
3. Create task #3
4. Delete task #2
5. Create a new task
6. Select option `2` (View Tasks)

**Expected Result:**
- New task has ID #4 (not #2)
- IDs: 1, 3, 4 (gap at 2 is permanent)

### Scenario 10: Exit Application

**Steps:**
1. Select option `6` (Exit)

**Expected Result:**
- Message "Goodbye!" displayed
- Application terminates cleanly

## Acceptance Criteria Checklist

- [ ] SC-001: Can create task in 3 interactions (menu → title → description)
- [ ] SC-002: Can distinguish complete from incomplete tasks visually
- [ ] SC-003: Full lifecycle works without crashes
- [ ] SC-004: All validation errors show clear messages
- [ ] SC-005: Task IDs remain unique throughout session
- [ ] SC-006: Can manage 100+ tasks without degradation
- [ ] SC-007: All operations complete within 1 second
- [ ] SC-008: Console output is readable and well-formatted

## Performance Test

Create 100+ tasks and verify:
```bash
# Run automated performance test
python -c "
from src.storage.memory_store import InMemoryTaskStore
from src.services.task_service import TaskService
import time

storage = InMemoryTaskStore()
service = TaskService(storage)

# Create 100 tasks
start = time.time()
for i in range(100):
    service.add_task(f'Task {i}', f'Description {i}')
create_time = time.time() - start

# View all tasks
start = time.time()
tasks = service.list_tasks()
view_time = time.time() - start

print(f'Created 100 tasks in {create_time:.4f}s')
print(f'Retrieved 100 tasks in {view_time:.4f}s')
print(f'Average per operation: {(create_time + view_time) / 101:.4f}s')

assert create_time < 1.0, 'Create operations too slow'
assert view_time < 1.0, 'View operation too slow'
print('Performance test: PASSED')
"
```

## Test Results Template

```
Date: ___________
Tester: ___________

Scenario 1: [ ] PASS [ ] FAIL
Scenario 2: [ ] PASS [ ] FAIL
Scenario 3: [ ] PASS [ ] FAIL
Scenario 4: [ ] PASS [ ] FAIL
Scenario 5: [ ] PASS [ ] FAIL
Scenario 6a-f: [ ] PASS [ ] FAIL
Scenario 7: [ ] PASS [ ] FAIL
Scenario 8: [ ] PASS [ ] FAIL
Scenario 9: [ ] PASS [ ] FAIL
Scenario 10: [ ] PASS [ ] FAIL

Performance: [ ] PASS [ ] FAIL

Overall: [ ] PASS [ ] FAIL

Notes:
_________________________________
_________________________________
```
