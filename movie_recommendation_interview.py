"""
INTERVIEW QUESTION: Movie Recommendation System

You are designing a movie recommendation system with the following rules:

1. Users and Movies:
   - There are n users, and movies are numbered from 1 to 1e9.
   - Each user likes a specific range of movies, represented as a segment [l_i, r_i],
     where l_i is the starting movie and r_i is the ending movie they like.

2. Predictor:
   - A user j is a "predictor" for another user i (where j != i) if:
     - User j likes all the movies that user i likes, and possibly some additional movies.
     - (This implies: l_j <= l_i and r_i <= r_j)

3. Strong Recommendation:
   - A movie is "strongly recommended" to user i if:
     - The movie is not already liked by user i.
     - The movie is liked by every predictor of user i.

4. Task:
   - For each user, calculate the number of "strongly recommended" movies.
   - If a user does not have any predictors, the answer is 0.

Example 1:
Input:
3
3 8
2 5
4 5

Output:
0 0 1

Explanation:
- User 1 (3-8) has no predictors, so no strongly recommended movies → Output: 0
- User 2 (2-5) has no predictors → Output: 0
- User 3 (4-5) has User 2 as a predictor. User 2 likes movies (2-5), and User 3 likes (4-5).
  The only movie liked by User 2 but not User 3 is 3 → Output: 1

Example 2:
Input:
2
42 42
1 1000000000

Output:
999999999 0

Explanation:
- User 1 (42-42) has User 2 as a predictor. User 2 likes movies (1-1000000000).
  The strongly recommended movies for User 1 are all movies except 42 → Output: 999999999
- User 2 (1-1000000000) has no predictors → Output: 0

INSTRUCTIONS FOR INTERVIEW ENVIRONMENT:
1. You have 45 minutes to solve this problem
2. Think out loud as you work through the solution
3. Consider time and space complexity
4. Write clean, readable code
5. Test your solution with the provided examples and edge cases
6. Be prepared to discuss your approach and optimizations

EDGE CASES TO CONSIDER:
- Single user (no predictors possible)
- All users like the same range
- Users with no predictors
- Users with many predictors
- Movie ranges that are very large (up to 1e9)
- Overlapping ranges, nested ranges
- Disjoint ranges
- Maximum number of users (2e5)

Good luck!
"""

s



# Test cases
if __name__ == "__main__":
    print("=== MOVIE RECOMMENDATION SYSTEM TEST CASES ===\n")
    
    # Test 1: Example 1 from problem description
    test_1_input = [(3, 8), (2, 5), (4, 5)]
    test_1_expected = [0, 0, 1]
    test_1_result = solve_movie_recommendation(test_1_input)
    print(f"Test 1 - Basic example:")
    print(f"  Input: {test_1_input}")
    print(f"  Expected: {test_1_expected}, Got: {test_1_result}")
    print(f"  {'✓ PASS' if test_1_result == test_1_expected else '✗ FAIL'}\n")
    
    # Test 2: Example 2 from problem description
    test_2_input = [(42, 42), (1, 1000000000)]
    test_2_expected = [999999999, 0]
    test_2_result = solve_movie_recommendation(test_2_input)
    print(f"Test 2 - Large range example:")
    print(f"  Input: {test_2_input}")
    print(f"  Expected: {test_2_expected}, Got: {test_2_result}")
    print(f"  {'✓ PASS' if test_2_result == test_2_expected else '✗ FAIL'}\n")
    
    # Test 3: Single user (no predictors)
    test_3_input = [(10, 20)]
    test_3_expected = [0]
    test_3_result = solve_movie_recommendation(test_3_input)
    print(f"Test 3 - Single user:")
    print(f"  Input: {test_3_input}")
    print(f"  Expected: {test_3_expected}, Got: {test_3_result}")
    print(f"  {'✓ PASS' if test_3_result == test_3_expected else '✗ FAIL'}\n")
    
    # Test 4: User with one predictor
    # User 0: [5, 10], User 1: [1, 15] (predictor for User 0)
    # Predictors for User 0: {User 1}
    # Intersection: [1, 15]
    # Recommended: [1, 15] - [5, 10] = [1, 4] + [11, 15] = 4 + 5 = 9
    test_4_input = [(5, 10), (1, 15)]
    test_4_expected = [9, 0]
    test_4_result = solve_movie_recommendation(test_4_input)
    print(f"Test 4 - User with one predictor:")
    print(f"  Input: {test_4_input}")
    print(f"  Expected: {test_4_expected}, Got: {test_4_result}")
    print(f"  {'✓ PASS' if test_4_result == test_4_expected else '✗ FAIL'}\n")
    
    # Test 5: User with multiple predictors
    # User 0: [10, 20]
    # User 1: [5, 25] (predictor for User 0)
    # User 2: [8, 22] (predictor for User 0)
    # Predictors for User 0: {User 1, User 2}
    # Intersection: [5, 25] ∩ [8, 22] = [8, 22]
    # Recommended: [8, 22] - [10, 20] = [8, 9] + [21, 22] = 2 + 2 = 4
    test_5_input = [(10, 20), (5, 25), (8, 22)]
    test_5_expected = [4, 0, 0]
    test_5_result = solve_movie_recommendation(test_5_input)
    print(f"Test 5 - User with multiple predictors:")
    print(f"  Input: {test_5_input}")
    print(f"  Expected: {test_5_expected}, Got: {test_5_result}")
    print(f"  {'✓ PASS' if test_5_result == test_5_expected else '✗ FAIL'}\n")
    
    # Test 6: No predictors for any user
    test_6_input = [(1, 5), (6, 10), (11, 15)]
    test_6_expected = [0, 0, 0]
    test_6_result = solve_movie_recommendation(test_6_input)
    print(f"Test 6 - No predictors:")
    print(f"  Input: {test_6_input}")
    print(f"  Expected: {test_6_expected}, Got: {test_6_result}")
    print(f"  {'✓ PASS' if test_6_result == test_6_expected else '✗ FAIL'}\n")
    
    # Test 7: Complex nested predictors
    # User 0: [10, 20]
    # User 1: [5, 25] (predictor for User 0)
    # User 2: [1, 30] (predictor for User 0, predictor for User 1)
    # Predictors for User 0: {User 1, User 2}
    # Intersection: [5, 25] ∩ [1, 30] = [5, 25]
    # Recommended for User 0: [5, 25] - [10, 20] = [5, 9] + [21, 25] = 5 + 5 = 10
    # Predictors for User 1: {User 2}
    # Intersection: [1, 30]
    # Recommended for User 1: [1, 30] - [5, 25] = [1, 4] + [26, 30] = 4 + 5 = 9
    test_7_input = [(10, 20), (5, 25), (1, 30)]
    test_7_expected = [10, 9, 0]
    test_7_result = solve_movie_recommendation(test_7_input)
    print(f"Test 7 - Complex nested predictors:")
    print(f"  Input: {test_7_input}")
    print(f"  Expected: {test_7_expected}, Got: {test_7_result}")
    print(f"  {'✓ PASS' if test_7_result == test_7_expected else '✗ FAIL'}\n")
    
    # Test 8: Edge case - same ranges
    test_8_input = [(10, 20), (10, 20)]
    test_8_expected = [0, 0]
    test_8_result = solve_movie_recommendation(test_8_input)
    print(f"Test 8 - Same ranges:")
    print(f"  Input: {test_8_input}")
    print(f"  Expected: {test_8_expected}, Got: {test_8_result}")
    print(f"  {'✓ PASS' if test_8_result == test_8_expected else '✗ FAIL'}\n")
    
    print("=== TESTING COMPLETE ===")
