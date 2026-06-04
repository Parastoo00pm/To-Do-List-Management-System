# Importing datetime to work with deadlines
from datetime import datetime

# Importing heapq to use heap 
import heapq

# Import deque for BFS queue
from collections import deque

# ------------------------
# Task class represents a single task in the system
class Task:
    def __init__(self, task_id, title, description, deadline, tags):
        # Save task details
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.tags = set(tags)  # Store tags uniquely using a set
        self.status = "Active"  # Default status when created

    # This function helps when we print the task
    def __str__(self):
        return f"ID:{self.task_id} | Title:{self.title} | Status:{self.status}"

# ------------------------
# DLLNode represents one node in our doubly linked list
class DLLNode:
    def __init__(self, task):
        self.task = task  # Each node holds a Task
        self.prev = None  # Pointer to previous node
        self.next = None  # Pointer to next node

# ------------------------
# TaskLinkedList stores all active tasks in order
class TaskLinkedList:
    def __init__(self):
        self.head = None  # Start of the list
        self.tail = None  # End of the list

    # Add a task at the end
    def append(self, task):
        new_node = DLLNode(task)
        if not self.head:
            self.head = self.tail = new_node  # If list empty, new node is head and tail
        else:
            self.tail.next = new_node  # Connect old tail to new node
            new_node.prev = self.tail
            self.tail = new_node  # Update tail to new node

    # Remove a task by its ID
    def remove(self, task_id):
        current = self.head
        while current:
            if current.task.task_id == task_id:
                # Adjust links if found
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return current.task  # Return removed task
            current = current.next
        return None  # Not found

    # Show all tasks one by one
    def traverse(self):
        current = self.head
        while current:
            print(current.task)
            current = current.next

    # Find a task by its ID
    def find_task_by_id(self, task_id):
        current = self.head
        while current:
            if current.task.task_id == task_id:
                return current.task
            current = current.next
        return None

    # Show tasks that have a certain tag
    def show_tasks_by_tag(self, tag):
        current = self.head
        found = False
        while current:
            if tag in current.task.tags:
                print(current.task)
                found = True
            current = current.next
        if not found:
            print(f"No tasks found with tag '{tag}'.")

# ------------------------
# UndoHandler helps us undo last deleted task
class UndoHandler:
    def __init__(self):
        self.stack = []  # Use a list as stack (LIFO)

    # Push a deleted task onto the stack
    def push(self, task):
        self.stack.append(task)

    # Pop the last deleted task and restore it
    def undo_last_delete(self, task_list):
        if self.stack:
            recovered_task = self.stack.pop()  # Take the last deleted task
            task_list.append(recovered_task)   # Add it back to the active tasks
            print("Undo Successful. Task Restored.")
            return recovered_task              # Return it so we can also update hash table
        else:
            print("Nothing to Undo.")
            return None

# ------------------------
# ReminderHandler manages task reminders
class ReminderHandler:
    def __init__(self):
        self.heap = []

    def add_reminder(self, task):
        try:
            deadline = datetime.strptime(task.deadline, "%Y-%m-%d")
            heapq.heappush(self.heap, (deadline, task))
        except ValueError:
            print(f"Invalid date for Task {task.task_id}")

    def show_earliest_reminder(self):
        if self.heap:
            next_task = heapq.heappop(self.heap)[1]
            print("Next Reminder:", next_task)
        else:
            print("No Reminders Found.")

# ------------------------
# BSTNode represents one node in the binary search tree
class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

# ------------------------
# TaskBST manages tasks sorted by Title A-Z
class TaskBST:
    def __init__(self):
        self.root = None  # Start with empty tree

    # Insert a new task into BST
    def insert(self, task):
        self.root = self._insert_recursive(self.root, task)

    # Helper function for inserting recursively
    def _insert_recursive(self, node, task):
        if not node:
            return BSTNode(task)
        if task.title.lower() < node.task.title.lower():  # If title is smaller → go left
            node.left = self._insert_recursive(node.left, task)  # Call itself again to go deeper
        else:
            node.right = self._insert_recursive(node.right, task)  # If title is bigger or equal → go right
        return node

    # Traverse the tree in-order to get sorted tasks
    def inorder_traversal(self):
        result = []  # Empty list
        self._inorder(self.root, result)  # starts the process by calling inorder()
        return result

    # Helper function for in-order traversal-walks through tree
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.task)
            self._inorder(node.right, result)
        return result

# ------------------------
# CompletedHandler stores deleted and done tasks
class CompletedHandler:
    def __init__(self):
        self.completed = []  # List to store completed/deleted tasks

    # Add a task to the completed list
    def add(self, task):
        self.completed.append(task)

    # Show completed/deleted tasks
    def show_completed_tasks(self, task_list):
        for task in self.completed:
            print(task)
        # Also show tasks marked as Done but still in list
        current = task_list.head
        found_done = False
        while current:
            if current.task.status == "Done":
                print(current.task)
                found_done = True
            current = current.next
        if not self.completed and not found_done:
            print("No Completed/Deleted Tasks.")

# ------------------------
# HeapHandler shows tasks by earliest deadline using heap
class HeapHandler:
    def __init__(self):
        pass  # No setup needed

    # Show tasks sorted by deadline (soonest first)
    def show_tasks_by_deadline(self, task_list):
        heap = []
        current = task_list.head
        while current:
            try:
                # Convert string to real date object
                deadline_date = datetime.strptime(current.task.deadline, "%Y-%m-%d")
                # Push (date, task) into the heap
                heapq.heappush(heap, (deadline_date, current.task))
            except ValueError:
                print(f"Skipping Task ID {current.task.task_id} (invalid date).")
            current = current.next

        if not heap:
            print("No tasks with valid deadlines.")
        else:
            while heap:
                item = heapq.heappop(heap)
                print(item[1])  # Only print the task

# ------------------------
# Level-order (BFS) traversal on BST using a simple queue
def bfs_traversal_bst(root):
    if not root:
        print("No tasks in BST.")
        return

    queue = deque()
    queue.append(root)

    print("\nTasks in BST (Level-Order / BFS):")
    while queue:
        node = queue.popleft()
        print(node.task)  # print task at this node

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

# ------------------------
# TaskHandler manages all main task operations and connects everything together (add, delete, edit, ...)
# It’s the one that the user menu talks to.
class TaskHandler:
    def __init__(self, task_list, task_bst, undo_handler, reminder_handler, completed_handler):
        self.task_list = task_list
        self.task_bst = task_bst
        self.undo_handler = undo_handler
        self.reminder_handler = reminder_handler
        self.completed_handler = completed_handler
        self.task_id_counter = 1  # Keeps track of task IDs
        self.task_index = {}      # Hash table (dict) for fast lookup by ID

    # Helper: add task to hash table
    def _add_to_index(self, task):
        self.task_index[task.task_id] = task

    # Helper: remove task from hash table
    def _remove_from_index(self, task):
        if task.task_id in self.task_index:
            del self.task_index[task.task_id]

    # Add a new task
    def add_task(self):
        title = input("Enter Task Title: ")
        description = input("Enter Task Description: ")
        deadline = input("Enter Task Deadline (YYYY-MM-DD): ")
        tags = input("Enter Task Tags (comma separated): ").split(",")

        task = Task(self.task_id_counter, title, description, deadline, tags)
        self.task_list.append(task)       # Add to linked list
        self.task_bst.insert(task)        # Add to BST
        self._add_to_index(task)          # Add to hash table for O(1) ID search

        reminder = input("Set reminder for this task? (yes/no): ").lower()
        if reminder == 'yes':
            self.reminder_handler.add_reminder(task)  # Add to queue if reminder set

        print("Task Added Successfully!")
        self.task_id_counter += 1  # Move to next task ID

    # Delete a task
    def delete_task(self):
        task_id = int(input("Enter Task ID to Delete: "))
        deleted_task = self.task_list.remove(task_id)
        if deleted_task:
            self.undo_handler.push(deleted_task)
            self.completed_handler.add(deleted_task)
            self._remove_from_index(deleted_task)  # Also remove from hash table
            print("Task Deleted.")
        else:
            print("Task Not Found.")

    # Show all tasks (in order added)
    def show_all_tasks(self):
        print("\nAll Tasks (Order Added):")
        self.task_list.traverse()

    # Show tasks sorted by title
    def show_sorted_tasks(self):
        print("\nAll Tasks (Sorted A-Z):")
        sorted_tasks = self.task_bst.inorder_traversal()
        for task in sorted_tasks:
            print(task)

    # Search and show tasks by tag
    def show_tasks_by_tag(self):
        tag = input("Enter Tag to Search: ")
        self.task_list.show_tasks_by_tag(tag)

    # Change status of task to Done
    def change_task_status(self):
        task_id = int(input("Enter Task ID to mark Done: "))
        task = self.task_list.find_task_by_id(task_id)
        if task:
            task.status = "Done"
            print("Task status changed to Done.")
        else:
            print("Task not found.")

    # Edit a task after it's been added
    def edit_existing_task(self):
        task_id = int(input("Enter Task ID to Edit: "))
        task = self.task_list.find_task_by_id(task_id)
        if task:
            while True:
                print("\nCurrent Task Info:")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Deadline: {task.deadline}")
                print(f"Tags: {task.tags}")
                field = input("Edit which field? (title/description/deadline/tags/done): ").lower()
                if field == "title":
                    task.title = input("Enter new title: ")
                elif field == "description":
                    task.description = input("Enter new description: ")
                elif field == "deadline":
                    task.deadline = input("Enter new deadline (YYYY-MM-DD): ")
                elif field == "tags":
                    task.tags = set(input("Enter new tags (comma separated): ").split(","))
                elif field == "done":
                    break
                else:
                    print("Invalid field.")
            print("Task updated successfully.")
        else:
            print("Task ID not found.")

    # Search task by ID using hash table (dict)
    def search_task_by_id_hash(self):
        try:
            task_id = int(input("Enter Task ID to Search (Hash Table): "))
        except ValueError:
            print("Invalid ID.")
            return

        task = self.task_index.get(task_id)
        if task:
            print("Task Found (Hash Table):")
            print(task)
        else:
            print("Task not found in hash index.")

    # Search task by title using Binary Search on sorted list from BST
    def binary_search_task_by_title(self):
        title = input("Enter exact Task Title to search: ").strip().lower()

        # Get tasks sorted A-Z from BST
        sorted_tasks = self.task_bst.inorder_traversal()

        left = 0
        right = len(sorted_tasks) - 1
        found = None

        while left <= right:
            mid = (left + right) // 2
            mid_title = sorted_tasks[mid].title.lower()

            if mid_title == title:
                found = sorted_tasks[mid]
                break
            elif title < mid_title:
                right = mid - 1
            else:
                left = mid + 1

        if found:
            print("Task Found (Binary Search):")
            print(found)
        else:
            print("No task found with that exact title.")

    # Show tasks using BFS level-order on BST
    def show_tasks_bfs(self):
        bfs_traversal_bst(self.task_bst.root)

# ------------------------
# Setting up everything (creating objects for each handler)
task_list = TaskLinkedList()                 # Linked list to store active tasks
task_bst = TaskBST()                         # BST to sort tasks A-Z by title
undo_handler = UndoHandler()                # Stack to manage undo
reminder_handler = ReminderHandler()        # Queue to manage reminders
completed_handler = CompletedHandler()      # List to store completed/deleted tasks
heap_handler = HeapHandler()                # Heap for sorting tasks by deadline
task_handler = TaskHandler(                 # Main task manager
    task_list, task_bst, undo_handler,
    reminder_handler, completed_handler
)

# ------------------------
# Function to show the menu
def display_menu():
    print("\nTo-Do List Menu")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Undo Last Delete")
    print("4. Show All Tasks (Order Added)")
    print("5. Show All Tasks (Sorted A-Z)")
    print("6. Show Tasks by Tag")
    print("7. Show Next Reminder")
    print("8. Show Tasks by Deadline (Earliest First)")
    print("9. Show Deleted/Completed Tasks")
    print("10. Change Task Status to Done")
    print("11. Edit Existing Task")
    print("12. Exit")
    print("13. Search Task by ID (Hash Table)")
    print("14. Search Task by Title (Binary Search)")
    print("15. Show Tasks")

# ------------------------
# This is the main loop that runs the whole program
while True:
    print("-" * 40)
    display_menu()  # Show the menu
    print("-" * 40)
    choice = input("Choose an option (1-15): ")  # Ask user what to do

    if choice == '1':
        task_handler.add_task()

    elif choice == '2':
        task_handler.delete_task()

    elif choice == '3':
        recovered = undo_handler.undo_last_delete(task_list)
        if recovered:
            task_handler._add_to_index(recovered)

    elif choice == '4':
        task_handler.show_all_tasks()

    elif choice == '5':
        task_handler.show_sorted_tasks()

    elif choice == '6':
        task_handler.show_tasks_by_tag()

    elif choice == '7':
        reminder_handler.show_earliest_reminder()

    elif choice == '8':
        heap_handler.show_tasks_by_deadline(task_list)

    elif choice == '9':
        completed_handler.show_completed_tasks(task_list)

    elif choice == '10':
        task_handler.change_task_status()

    elif choice == '11':
        task_handler.edit_existing_task()

    elif choice == '12':
        print("\nExiting... Goodbye!")  # Exit message
        break

    elif choice == '13':
        task_handler.search_task_by_id_hash()

    elif choice == '14':
        task_handler.binary_search_task_by_title()

    elif choice == '15':
        task_handler.show_tasks_bfs()

    else:
        print("Invalid choice. Please try again.")  # If user types wrong option
