"""
INTERVIEW QUESTION: Hierarchical Access Control System

You are given a tree-like data structure where each node represents a resource.
Each Resource has fields: name, parent, and children.

Implement a system with the following methods:
- grant_access(user, resource): Grant access to a resource and all its children
- revoke_access(user, resource): Revoke access from a resource and all its children  
- has_access(user, resource): Check if a user has access to a specific resource

Key Rules:
1. If you grant access to a resource, you automatically grant access to ALL resources under it
2. If you revoke access from a resource, you automatically revoke access from ALL resources under it
3. Access is inherited down the tree hierarchy

Example Tree Structure:
    root
   /    \
  A      B
 / \    / \
C   D  E   F
   /
  G

If you grant access to "A", user gets access to A, C, D, and G
If you revoke access from "A", user loses access to A, C, D, and G

INSTRUCTIONS FOR INTERVIEW ENVIRONMENT:
1. You have 60 minutes to solve this problem
2. Think about the data structures you'll need
3. Consider time and space complexity for each operation
4. Handle edge cases (root node, leaf nodes, non-existent resources)
5. Write clean, readable code with good variable names
6. Be prepared to discuss your design choices

EDGE CASES TO CONSIDER:
- Granting/revoking access to root node
- Granting/revoking access to leaf nodes
- Checking access for non-existent users/resources
- Multiple grants/revokes to the same resource
- Deep vs wide trees
- Circular references (if applicable)

Good luck!
"""

from re import I


class Resource:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

class AccessControlSystem:
    def __init__(self):
        # TODO: Initialize your data structures here
        # Hint: You'll need to track which users have access to which resources

      
        self.user_resources = {}
        self.resources_to_user = {}
    def pre_node (self, resource):
            if not resource:
                return []
            descendents = []

            for child in resource.children:
                descendents.append(child.name)
                descendents.extend(self.pre_node(child))
            return descendents
    
    def grant_access(self, user, resource):
        """
        Grant access to a resource and all its children
        
        Args:
            user (str): The user to grant access to
            resource (Resource): The resource to grant access to
        
        Returns:
            None
        """

        all_resources = [resource.name] + self.pre_node(resource)
        if user not in self.user_resources:
            self.user_resources[user] = set()
        self.user_resources[user].update(all_resources)

        for i in all_resources:
            if i not in self.resources_to_user:
                self.resources_to_user[i] = set()
            self.resources_to_user[i].add(user)
            

    def revoke_access(self, user, resource):
        """
        Revoke access from a resource and all its children
        
        Args:
            user (str): The user to revoke access from
            resource (Resource): The resource to revoke access from
        
        Returns:
            None
        """
        all_resources = [resource.name] + self.pre_node(resource)

        for i in all_resources:
            self.user_resources[user].discard(i)
            self.resources_to_user[i].discard(user)

        
    
    def has_access(self, user, resource):
        """
        Check if a user has access to a specific resource
        
        Args:
            user (str): The user to check
            resource (Resource): The resource to check access for
        
        Returns:
            bool: True if user has access, False otherwise
        """
        if user not in self.user_resources:
            return False
        return True if resource.name in self.user_resources[user] else False

def build_test_tree():
    """Helper function to build a test tree structure"""
    root = Resource("root")
    A = Resource("A", root)
    B = Resource("B", root)
    C = Resource("C", A)
    D = Resource("D", A)
    E = Resource("E", B)
    F = Resource("F", B)
    G = Resource("G", D)
    return root, A, B, C, D, E, F, G

# Test cases
if __name__ == "__main__":
    print("=== ACCESS CONTROL SYSTEM TEST CASES ===\n")
    
    # Build test tree
    root, A, B, C, D, E, F, G = build_test_tree()
    system = AccessControlSystem()
    
    # Test 1: Basic grant and check
    print("Test 1 - Basic grant and check:")
    system.grant_access("alice", A)
    result = system.has_access("alice", A)
    print(f"  Grant access to 'alice' for resource 'A'")
    print(f"  Check access for 'alice' to 'A': Expected True, Got {result}")
    print(f"  ✓ PASS\n" if result else f"  ✗ FAIL\n")
    
    # Test 2: Inheritance - child access
    print("Test 2 - Inheritance (child access):")
    result = system.has_access("alice", C)
    print(f"  Check access for 'alice' to 'C' (child of A): Expected True, Got {result}")
    print(f"  ✓ PASS\n" if result else f"  ✗ FAIL\n")
    
    # Test 3: Inheritance - grandchild access
    print("Test 3 - Inheritance (grandchild access):")
    result = system.has_access("alice", G)
    print(f"  Check access for 'alice' to 'G' (grandchild of A): Expected True, Got {result}")
    print(f"  ✓ PASS\n" if result else f"  ✗ FAIL\n")
    
    # Test 4: No access to sibling
    print("Test 4 - No access to sibling:")
    result = system.has_access("alice", B)
    print(f"  Check access for 'alice' to 'B' (sibling of A): Expected False, Got {result}")
    print(f"  ✓ PASS\n" if not result else f"  ✗ FAIL\n")
    
    # Test 5: Revoke access
    print("Test 5 - Revoke access:")
    system.revoke_access("alice", A)
    result = system.has_access("alice", A)
    print(f"  Revoke access for 'alice' from resource 'A'")
    print(f"  Check access for 'alice' to 'A': Expected False, Got {result}")
    print(f"  ✓ PASS\n" if not result else f"  ✗ FAIL\n")
    
    # Test 6: Revoke affects children
    print("Test 6 - Revoke affects children:")
    system.grant_access("bob", A)
    system.revoke_access("bob", A)
    result = system.has_access("bob", C)
    print(f"  Grant then revoke access for 'bob' from resource 'A'")
    print(f"  Check access for 'bob' to 'C': Expected False, Got {result}")
    print(f"  ✓ PASS\n" if not result else f"  ✗ FAIL\n")
    
    # Test 7: Root access
    print("Test 7 - Root access:")
    system.grant_access("charlie", root)
    result = system.has_access("charlie", F)
    print(f"  Grant access for 'charlie' to root")
    print(f"  Check access for 'charlie' to 'F': Expected True, Got {result}")
    print(f"  ✓ PASS\n" if result else f"  ✗ FAIL\n")
    
    # Test 8: Multiple users
    print("Test 8 - Multiple users:")
    system.grant_access("david", B)
    result1 = system.has_access("david", E)
    result2 = system.has_access("charlie", E)
    print(f"  Grant access for 'david' to 'B'")
    print(f"  Check access for 'david' to 'E': Expected True, Got {result1}")
    print(f"  Check access for 'charlie' to 'E': Expected True, Got {result2}")
    print(f"  ✓ PASS\n" if result1 and result2 else f"  ✗ FAIL\n")
    
    # Test 9: Non-existent user
    print("Test 9 - Non-existent user:")
    result = system.has_access("unknown", A)
    print(f"  Check access for 'unknown' to 'A': Expected False, Got {result}")
    print(f"  ✓ PASS\n" if not result else f"  ✗ FAIL\n")
    
    # Test 10: Deep tree access
    print("Test 10 - Deep tree access:")
    system.grant_access("eve", D)
    result = system.has_access("eve", G)
    print(f"  Grant access for 'eve' to 'D'")
    print(f"  Check access for 'eve' to 'G' (deep child): Expected True, Got {result}")
    print(f"  ✓ PASS\n" if result else f"  ✗ FAIL\n")
    
    print("=== TESTING COMPLETE ===")
