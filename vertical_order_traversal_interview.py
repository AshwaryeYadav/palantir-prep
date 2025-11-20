"""
VERTICAL ORDER TRAVERSAL INTERVIEW QUESTION
==========================================

Given a binary tree, perform a vertical order (column-order) traversal and return 
the word formed by reading columns from left to right.

In a vertical order traversal:
- The root is at column 0
- Left child goes to column -1, right child goes to column +1
- Read all nodes in each column from left to right
- Concatenate the values to form a word

EXAMPLES:

Example 1:
Tree:     a
         / \
        b   c
       / \ / \
      d  e f  g

Column indices:
- Column -1: d
- Column 0:  b, e, f  
- Column 1:  c, g

Reading left to right: d + b + e + f + c + g = "dbefcg"

Example 2:
Tree:     i
         / \
        r   y
       / \
      p   v

Column indices:
- Column -1: p
- Column 0:  r
- Column 1:  y, v

Reading left to right: p + r + y + v = "privy"

TASK:
Implement the vertical_order_traversal function that takes a root node and returns 
the word formed by the vertical order traversal.

CONSTRAINTS:
- Tree can have 1 to 1000 nodes
- Node values are single characters
- Tree may be unbalanced
- Handle empty tree (return empty string)

INTERVIEW TIPS:
- Think about how to assign column indices to nodes
- Consider using BFS or DFS for traversal
- Use a data structure to group nodes by column
- Sort columns or track min/max for efficient processing
- Discuss time and space complexity
"""

from collections import defaultdict, deque
from typing import Optional


class TreeNode:
    """Binary tree node"""
    def __init__(self, val: str):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


def vertical_order_traversal(root):
    """
    Performs vertical order (column-order) traversal
    Returns the word formed by reading columns left to right
    """
    if not root:
        return ""
    
    # Store (row, col, val) tuples
    nodes = []
    queue = deque([(root, 0, 0)])  # (node, row, col)
    
    while queue:
        node, row, col = queue.popleft()
        nodes.append((row, col, node.val))
        
        if node.left:
            queue.append((node.left, row + 1, col - 1))
        if node.right:
            queue.append((node.right, row + 1, col + 1))
    
    # Sort by column first, then by row
    nodes.sort(key=lambda x: (x[1], x[0]))
    
    # Extract values in order
    result = ""
    for row, col, val in nodes:
        result += val
    
    return result


# OPTIMIZED VERSION (commented out for reference)
# def vertical_order_traversal_optimized(root):
#     """
#     Alternative implementation using row/column tracking for explicit ordering
#     Time complexity: O(n log n) due to sorting all nodes
#     """
#     if not root:
#         return ""
#     
#     # Store (row, col, val) tuples
#     nodes = []
#     queue = deque([(root, 0, 0)])  # (node, row, col)
#     
#     while queue:
#         node, row, col = queue.popleft()
#         nodes.append((row, col, node.val))
#         
#         if node.left:
#             queue.append((node.left, row + 1, col - 1))
#         if node.right:
#             queue.append((node.right, row + 1, col + 1))
#     
#     # Sort by column first, then by row
#     nodes.sort(key=lambda x: (x[1], x[0]))
#     
#     # Extract values in order
#     result = ""
#     for row, col, val in nodes:
#         result += val
#     
#     return result


# Test cases (feel free to add more)
if __name__ == "__main__":
    # Test case 1: Simple tree
    # Tree:     a
    #          / \
    #         b   c
    root1 = TreeNode('a')
    root1.left = TreeNode('b')
    root1.right = TreeNode('c')
    
    result1 = vertical_order_traversal(root1)
    print(f"Test 1: {result1}")  # Expected: "bac"
    
    # Test case 2: Tree from example 1
    # Tree:     a
    #          / \
    #         b   c
    #        / \ / \
    #       d  e f  g
    root2 = TreeNode('a')
    root2.left = TreeNode('b')
    root2.right = TreeNode('c')
    root2.left.left = TreeNode('d')
    root2.left.right = TreeNode('e')
    root2.right.left = TreeNode('f')
    root2.right.right = TreeNode('g')
    
    result2 = vertical_order_traversal(root2)
    print(f"Test 2: {result2}")  # Expected: "dbaefcg"
    
    # Test case 3: Tree from example 2
    # Tree:     i
    #          / \
    #         r   y
    #        / \
    #       p   v
    root3 = TreeNode('i')
    root3.left = TreeNode('r')
    root3.right = TreeNode('y')
    root3.left.left = TreeNode('p')
    root3.left.right = TreeNode('v')
    
    result3 = vertical_order_traversal(root3)
    print(f"Test 3: {result3}")  # Expected: "privy"
    
    # Test case 4: Single node
    root4 = TreeNode('x')
    result4 = vertical_order_traversal(root4)
    print(f"Test 4: {result4}")  # Expected: "x"
    
    # Test case 5: Empty tree
    result5 = vertical_order_traversal(None)
    print(f"Test 5: {result5}")  # Expected: ""
    
    # Test case 6: Left-skewed tree
    # Tree:     a
    #          /
    #         b
    #        /
    #       c
    root6 = TreeNode('a')
    root6.left = TreeNode('b')
    root6.left.left = TreeNode('c')
    
    result6 = vertical_order_traversal(root6)
    print(f"Test 6: {result6}")  # Expected: "cba"
    
    # Test case 7: Right-skewed tree
    # Tree:     a
    #            \
    #             b
    #              \
    #               c
    root7 = TreeNode('a')
    root7.right = TreeNode('b')
    root7.right.right = TreeNode('c')
    
    result7 = vertical_order_traversal(root7)
    print(f"Test 7: {result7}")  # Expected: "abc"
    
    # Test case 8: Complex tree
    # Tree:      1
    #          /   \
    #         2     3
    #        / \     \
    #       4   5     6
    #            \
    #             7
    root8 = TreeNode('1')
    root8.left = TreeNode('2')
    root8.right = TreeNode('3')
    root8.left.left = TreeNode('4')
    root8.left.right = TreeNode('5')
    root8.right.right = TreeNode('6')
    root8.left.right.right = TreeNode('7')
    
    result8 = vertical_order_traversal(root8)
    print(f"Test 8: {result8}")  # Expected: "4215376"
