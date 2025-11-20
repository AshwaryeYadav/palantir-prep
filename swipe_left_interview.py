"""
2048 SWIPE LEFT FUNCTION INTERVIEW QUESTION
==========================================

DESCRIPTION:
Implement a swipe-left function for a 2048-style game. When swiping left:
1. All tiles move as far left as possible
2. Adjacent equal tiles merge into their sum
3. Each tile can only merge once per swipe
4. Empty positions are filled with 0

RULES:
1. Move all non-zero tiles to the left
2. Merge adjacent equal tiles (leftmost first)
3. Each tile can only participate in one merge per swipe
4. Fill remaining positions with 0

EXAMPLES:
Example 1:
Input: [2,0,2,4]
Step 1: Move left → [2,2,4,0]
Step 2: Merge 2s → [4,4,0,0]
Step 3: Move left → [4,4,0,0]
Step 4: Merge 4s → [8,0,0,0]
Output: [8,0,0,0]

Example 2:
Input: [2,2,4,4]
Step 1: Already moved left
Step 2: Merge first pair of 2s → [4,4,4,0]
Step 3: Move left → [4,4,4,0]
Step 4: Merge first pair of 4s → [8,4,0,0]
Step 5: Move left → [8,4,0,0]
Output: [8,4,0,0]

Example 3:
Input: [8,0,8,0]
Step 1: Move left → [8,8,0,0]
Step 2: Merge 8s → [16,0,0,0]
Output: [16,0,0,0]

TASK:
Implement the swipeLeft function that takes an array of numbers and returns 
the result after performing the swipe-left operation.

CONSTRAINTS:
- Array contains non-negative integers (0 represents empty)
- Process merges from left to right
- Each tile can only merge once per swipe
- The array length remains the same
- Only adjacent equal tiles can merge

INTERVIEW TIPS:
- Think about the two-step process: move + merge
- Consider using a stack or two-pointer approach
- Handle edge cases (empty array, all zeros, no merges possible)
- Discuss your approach before coding
- Consider what happens with multiple pairs (like [2,2,2,2])
"""

def swipeLeft(arr):
    """
    Implement 2048-style swipe-left function that moves tiles left and merges equal adjacent tiles.
    
    Args:
        arr: List of non-negative integers (0 represents empty)
        
    Returns:
        List of integers after swipe-left operation
    """
    # TODO: Implement this function
    pass

# Test cases (feel free to add more)
if __name__ == "__main__":
    # Test case 1
    result1 = swipeLeft([2,0,2,4])
    print(f"Test 1: {result1}")  # Expected: [8,0,0,0]
    
    # Test case 2
    result2 = swipeLeft([2,2,4,4])
    print(f"Test 2: {result2}")  # Expected: [8,4,0,0]
    
    # Test case 3
    result3 = swipeLeft([8,0,8,0])
    print(f"Test 3: {result3}")  # Expected: [16,0,0,0]
    
    # Test case 4
    result4 = swipeLeft([2,4,8,16])
    print(f"Test 4: {result4}")  # Expected: [2,4,8,16] (no merges possible)
    
    # Test case 5
    result5 = swipeLeft([0,0,0,0])
    print(f"Test 5: {result5}")  # Expected: [0,0,0,0]
    
    # Test case 6
    result6 = swipeLeft([2,2,2,2])
    print(f"Test 6: {result6}")  # Expected: [4,4,0,0] (merge first pair, then second pair)
    
    # Test case 7
    result7 = swipeLeft([4,4,2,2])
    print(f"Test 7: {result7}")  # Expected: [8,4,0,0] (merge 4s to 8, merge 2s to 4)
    
    # Test case 8
    result8 = swipeLeft([8,8,8,8])
    print(f"Test 8: {result8}")  # Expected: [16,16,0,0] (merge first pair, then second pair)
