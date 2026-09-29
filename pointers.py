"""
Linked Lists and Pointers in Python
====================================

In Python, "pointers" are references to objects in memory.
Unlike C/C++, Python doesn't have explicit pointer syntax, but variables 
store references to objects. This file demonstrates linked lists using Python references.
"""


class Node:
    """
    A node in a linked list.
    
    In Python, we use object references instead of explicit pointers.
    The 'next' attribute is a reference to the next Node object.
    """
    def __init__(self, data):
        self.data = data      # The actual data stored in the node
        self.next = None      # Reference to the next node (initially None/null)
    
    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """
    A singly linked list implementation.
    
    A linked list is a linear data structure where each element (node) 
    points to the next element, allowing efficient insertion and deletion.
    """
    def __init__(self):
        self.head = None      # Reference to the first node
    
    def append(self, data):
        """Add a node to the end of the list."""
        new_node = Node(data)
        
        if not self.head:
            # If list is empty, new node becomes the head
            self.head = new_node
            return
        
        # Traverse to the last node
        current = self.head
        while current.next is not None:
            current = current.next
        
        # Point the last node to the new node
        current.next = new_node
    
    def prepend(self, data):
        """Add a node to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head  # New node points to what was the head
        self.head = new_node        # Update head to the new node
    
    def insert_after(self, prev_data, data):
        """Insert a node after the first node with prev_data."""
        current = self.head
        
        while current and current.data != prev_data:
            current = current.next
        
        if current is None:
            print(f"Node with data {prev_data} not found!")
            return
        
        new_node = Node(data)
        new_node.next = current.next  # New node points to what current was pointing to
        current.next = new_node        # Current now points to the new node
    
    def delete(self, data):
        """Delete the first node with the given data."""
        # Handle deletion of head node
        if self.head and self.head.data == data:
            self.head = self.head.next
            return
        
        # Search for the node to delete
        current = self.head
        while current and current.next:
            if current.next.data == data:
                current.next = current.next.next  # Skip over the node
                return
            current = current.next
    
    def search(self, data):
        """Search for a node with the given data."""
        current = self.head
        
        while current:
            if current.data == data:
                return True
            current = current.next
        
        return False
    
    def display(self):
        """Print all elements in the linked list."""
        elements = []
        current = self.head
        
        while current:
            elements.append(str(current.data))
            current = current.next
        
        print(" -> ".join(elements) + " -> None")
    
    def __len__(self):
        """Return the number of nodes in the list."""
        count = 0
        current = self.head
        
        while current:
            count += 1
            current = current.next
        
        return count
    
    def reverse(self):
        """Reverse the linked list in-place."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next  # Save reference to next node
            current.next = prev        # Reverse the pointer
            prev = current             # Move prev forward
            current = next_node        # Move current forward
        
        self.head = prev


# ============================================================================
# TEST SCRIPT
# ============================================================================

def test_linked_list():
    """Comprehensive test script for linked list operations."""
    
    print("=" * 60)
    print("LINKED LIST AND POINTERS IN PYTHON - TEST SCRIPT")
    print("=" * 60)
    
    # Test 1: Create an empty list and append elements
    print("\n[TEST 1] Creating a linked list and appending elements...")
    ll = LinkedList()
    print(f"Empty list - Head: {ll.head}")
    
    for value in [10, 20, 30, 40]:
        ll.append(value)
    
    print("After appending 10, 20, 30, 40:")
    ll.display()
    print(f"Length: {len(ll)}")
    
    # Test 2: Prepend elements
    print("\n[TEST 2] Prepending elements...")
    ll.prepend(5)
    print("After prepending 5:")
    ll.display()
    
    # Test 3: Insert after
    print("\n[TEST 3] Inserting after specific node...")
    ll.insert_after(20, 25)
    print("After inserting 25 after 20:")
    ll.display()
    
    # Test 4: Search
    print("\n[TEST 4] Searching for elements...")
    print(f"Search for 25: {ll.search(25)}")
    print(f"Search for 100: {ll.search(100)}")
    
    # Test 5: Delete
    print("\n[TEST 5] Deleting elements...")
    ll.delete(25)
    print("After deleting 25:")
    ll.display()
    
    ll.delete(5)  # Delete head
    print("After deleting head (5):")
    ll.display()
    
    # Test 6: Reverse
    print("\n[TEST 6] Reversing the linked list...")
    ll.reverse()
    print("After reversing:")
    ll.display()
    
    # Test 7: Understanding pointers/references
    print("\n[TEST 7] Understanding Python references (pointers)...")
    print("Creating two variables pointing to the same node:")
    node1 = Node(100)
    node2 = node1  # Both reference the same object
    print(f"node1: {node1}, node2: {node2}")
    print(f"node1 is node2: {node1 is node2} (same object in memory)")
    print(f"node1 == node2: {node1 == node2} (same data)")
    
    node3 = Node(100)
    print(f"node1 is node3: {node1 is node3} (different objects)")
    print(f"node1 == node3: {node1 == node3} (but same data)")
    
    # Test 8: Complex operations
    print("\n[TEST 8] Creating a new list for more complex tests...")
    ll2 = LinkedList()
    values = [1, 2, 3, 4, 5]
    for v in values:
        ll2.append(v)
    
    print("New list:")
    ll2.display()
    print(f"Length: {len(ll2)}")
    
    # Demonstrate traversal
    print("\nManual traversal:")
    current = ll2.head
    step = 1
    while current:
        print(f"  Step {step}: Data = {current.data}, Next = {current.next}")
        current = current.next
        step += 1
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    test_linked_list()
