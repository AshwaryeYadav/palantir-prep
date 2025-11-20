"""
PLANET INTERVALS INTERVIEW QUESTION
===================================

A spaceship is approaching some planets that are arranged in a 1-dimensional line. 
It needs to pass through the line of the planets, but can't get too close to any planet, 
otherwise it would get caught in that planet's gravitational field.

Given a list of planets, where each planet is specified by its position along the line 
and the range of its gravitational field, compute the list of gaps from [0, 1000] through 
which the spaceship can fly.

INPUT FORMAT:
- Each planet is represented as [location, orbit]
- location: position of the planet on the line
- orbit: radius of the gravitational field (the field extends from location-orbit to location+orbit)

OUTPUT FORMAT:
- List of gaps where the spaceship can safely fly
- Each gap is represented as [start, end] inclusive

EXAMPLES:
Input: [3,2]                Output: [0,1],[5,1000]          Reasoning: The field covers [1,5].
Input: [3,2],[5,1]          Output: [0,1],[6,1000]          Reasoning: The fields cover [1,5] and [4,6].
Input: [2,1],[5,1]          Output: [0,1],[3,4],[6,1000]    Reasoning: The fields cover [1,3] and [4,6].
Input: [2,2],[7,1],[4,1]    Output: [5,6],[8,1000]          Reasoning: The fields cover [0,4], [6,8], and [3,5].

TASK:
Implement the computeGaps function that takes a list of planets and returns the safe gaps.

CONSTRAINTS:
- Planet positions are integers
- Orbit radii are positive integers
- We need to find gaps in the range [0, 1000]
- Overlapping gravitational fields should be merged

INTERVIEW TIPS:
- Think about how to handle overlapping intervals
- Consider edge cases (no planets, planets at boundaries)
- Discuss your approach before coding
- Consider time and space complexity
"""

def computeGaps(planets):
    """
    Compute the safe gaps for spaceship navigation.
    
    Args:
        planets: List of [location, orbit] pairs representing planets
        
    Returns:
        List of [start, end] gaps where spaceship can safely fly
    """
    results = []
    for lists in planets:
       location, orbit = lists
       results.append([location - orbit, location+orbit])
    
    results.sort(key=lambda x: x[0])
    merged = [results[0]]
    for curr in results[1:]:
        last = merged[-1]

        if curr[0] <= last[1]:
            merged[-1] = [last[0], max(last[1], curr[1])]
        else:
            merged.append(curr)
    gaps = []
    currpos = 0

    for interval in merged:

        if currpos<interval[0]:
            gaps.append([currpos, interval[0]-1])
        currpos = interval[1] + 1
    if currpos < 1000:
        gaps.append([currpos, 1000])
    return gaps



        





# Test cases (feel free to add more)
if __name__ == "__main__":
    # Test case 1
    result1 = computeGaps([[3,2]])
    print(f"Test 1: {result1}")  # Expected: [[0,1],[5,1000]]
    
    # Test case 2
    result2 = computeGaps([[3,2],[5,1]])
    print(f"Test 2: {result2}")  # Expected: [[0,1],[6,1000]]
    
    # Test case 3
    result3 = computeGaps([[2,1],[5,1]])
    print(f"Test 3: {result3}")  # Expected: [[0,1],[3,4],[6,1000]]
    
    # Test case 4
    result4 = computeGaps([[2,2],[7,1],[4,1]])
    print(f"Test 4: {result4}")  # Expected: [[5,6],[8,1000]]
