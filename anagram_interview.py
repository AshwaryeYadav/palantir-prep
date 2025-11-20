"""
INTERVIEW QUESTION: Anagram Finder

Given a string and a dictionary (list of strings), return all anagrams of the string that are also in the dictionary.

Example:
Input: "race", ["bat", "acer", "caer", "apple"]
Output: ["acer", "caer"]

INSTRUCTIONS FOR INTERVIEW ENVIRONMENT:
1. You have 45 minutes to solve this problem
2. Think out loud as you work through the solution
3. Consider time and space complexity
4. Write clean, readable code
5. Test your solution with the provided example and edge cases
6. Be prepared to discuss your approach and any optimizations

EDGE CASES TO CONSIDER:
- Empty string or empty dictionary
- No anagrams found
- Case sensitivity
- Duplicate words in dictionary
- Very long strings or large dictionaries

Good luck!
"""
from collections import Counter
def find_anagrams(word, dictionary):
    """
    TODO: Implement this function
    
    Args:
        word (str): The input string to find anagrams for
        dictionary (list): List of strings to search through
    
    Returns:
        list: All anagrams of 'word' that exist in the dictionary
    """
    #The goal here is to be able to find all the anagrams of a word in a dictionary, the way we can do this is through a counter object that can couunt all of the different 
    #characters, etc
    if len(dictionary) == 0 or len(word) == 0:
        return []
    counter = Counter(word.lower())
    val = []
    for i in dictionary:
        word1 = Counter(i.lower())
        if word1 == counter:
            val.append(i)
    return val


# Test cases
if __name__ == "__main__":
    print("=== ANAGRAM FINDER TEST CASES ===\n")
    
    # Test 1: Basic example from problem
    result = find_anagrams("race", ["bat", "acer", "caer", "apple"])
    print(f"Test 1 - Basic example:")
    print(f"  Input: 'race', ['bat', 'acer', 'caer', 'apple']")
    print(f"  Expected: ['acer', 'caer'], Got: {result}")
    print(f"  ✓ PASS\n" if result == ['acer', 'caer'] else f"  ✗ FAIL\n")
    
    # Test 2: Empty dictionary
    result = find_anagrams("test", [])
    print(f"Test 2 - Empty dictionary:")
    print(f"  Input: 'test', []")
    print(f"  Expected: [], Got: {result}")
    print(f"  ✓ PASS\n" if result == [] else f"  ✗ FAIL\n")
    
    # Test 3: No anagrams found
    result = find_anagrams("hello", ["world", "python", "code"])
    print(f"Test 3 - No anagrams found:")
    print(f"  Input: 'hello', ['world', 'python', 'code']")
    print(f"  Expected: [], Got: {result}")
    print(f"  ✓ PASS\n" if result == [] else f"  ✗ FAIL\n")
    
    # Test 4: Case sensitivity
    result = find_anagrams("Listen", ["Silent", "LISTEN", "silent", "enlist"])
    print(f"Test 4 - Case sensitivity:")
    print(f"  Input: 'Listen', ['Silent', 'LISTEN', 'silent', 'enlist']")
    print(f"  Expected: ['Silent', 'LISTEN', 'silent', 'enlist'], Got: {result}")
    print(f"  ✓ PASS\n" if set(result) == {'Silent', 'LISTEN', 'silent', 'enlist'} else f"  ✗ FAIL\n")
    
    # Test 5: Empty string
    result = find_anagrams("", ["a", "b", "c"])
    print(f"Test 5 - Empty string:")
    print(f"  Input: '', ['a', 'b', 'c']")
    print(f"  Expected: [], Got: {result}")
    print(f"  ✓ PASS\n" if result == [] else f"  ✗ FAIL\n")
    
    # Test 6: Single character
    result = find_anagrams("a", ["a", "b", "c", "aa"])
    print(f"Test 6 - Single character:")
    print(f"  Input: 'a', ['a', 'b', 'c', 'aa']")
    print(f"  Expected: ['a'], Got: {result}")
    print(f"  ✓ PASS\n" if result == ['a'] else f"  ✗ FAIL\n")
    
    # Test 7: Duplicate characters in word
    result = find_anagrams("aab", ["aba", "baa", "aabb", "ab"])
    print(f"Test 7 - Duplicate characters:")
    print(f"  Input: 'aab', ['aba', 'baa', 'aabb', 'ab']")
    print(f"  Expected: ['aba', 'baa'], Got: {result}")
    print(f"  ✓ PASS\n" if set(result) == {'aba', 'baa'} else f"  ✗ FAIL\n")
    
    # Test 8: Long word
    result = find_anagrams("listen", ["silent", "enlist", "tinsel", "listen", "listens"])
    print(f"Test 8 - Longer word:")
    print(f"  Input: 'listen', ['silent', 'enlist', 'tinsel', 'listen', 'listens']")
    print(f"  Expected: ['silent', 'enlist', 'tinsel', 'listen'], Got: {result}")
    print(f"  ✓ PASS\n" if set(result) == {'silent', 'enlist', 'tinsel', 'listen'} else f"  ✗ FAIL\n")
    
    # Test 9: Numbers and special characters
    result = find_anagrams("123", ["321", "132", "1234", "12"])
    print(f"Test 9 - Numbers:")
    print(f"  Input: '123', ['321', '132', '1234', '12']")
    print(f"  Expected: ['321', '132'], Got: {result}")
    print(f"  ✓ PASS\n" if set(result) == {'321', '132'} else f"  ✗ FAIL\n")
    
    # Test 10: Both empty inputs
    result = find_anagrams("", [])
    print(f"Test 10 - Both empty:")
    print(f"  Input: '', []")
    print(f"  Expected: [], Got: {result}")
    print(f"  ✓ PASS\n" if result == [] else f"  ✗ FAIL\n")
    
    print("=== TESTING COMPLETE ===")
