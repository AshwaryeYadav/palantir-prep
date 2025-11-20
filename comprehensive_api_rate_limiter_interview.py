"""
API Rate Limiter - Comprehensive Implementation
=============================================

You are building a rate limiter for bank APIs that are not designed for large volumes.
The system needs to queue up requests and send them within a rate limit.

This interview covers TWO PARTS of the same problem:

PART 1: Basic Rate Limiter
--------------------------
Simple per-second rate limiting where no more than RATE_LIMIT cost units 
can be processed per second.

PART 2: Windowed Rate Limiter  
------------------------------
Advanced rate limiting with a sliding window where no more than RATE_LIMIT 
cost units can be processed within the last RATE_LIMIT_WINDOW seconds.

REQUIREMENTS:
------------
Both parts implement:
- `request_api_call(cost: int)` - Called when a caller wants to make an API call
- `emit_api_calls() -> List[int]` - Called once per second by automated system
- Requests are processed in FIFO order
- If a single request exceeds the rate limit, it should be rejected

PART 1 SPECIFICS:
----------------
- Rate limit: No more than RATE_LIMIT cost units per second
- Simple per-second processing
- Reject individual requests that exceed the rate limit

PART 2 SPECIFICS:
----------------
- Rate limit: No more than RATE_LIMIT cost units within RATE_LIMIT_WINDOW seconds
- Sliding window: Track requests from the last N seconds
- Expire old requests when they fall outside the window
- More complex state management required

EXAMPLE - PART 1:
----------------
RATE_LIMIT = 4

# Time 0: Multiple requests
request_api_call(2)  # Request "a"
request_api_call(2)  # Request "b"  
request_api_call(1)  # Request "c"
request_api_call(1)  # Request "d"

emit_api_calls()     # Returns [2, 2] - Only first two fit within limit of 4

# Time 1: New request
request_api_call(3)  # Request "e"

emit_api_calls()     # Returns [1, 1] - Remaining from time 0
emit_api_calls()     # Returns [3] - Request from time 1

EXAMPLE - PART 2:
----------------
RATE_LIMIT = 5, RATE_LIMIT_WINDOW = 3

# Time 0: Request cost 2
request_api_call(2)
emit_api_calls()     # Returns [2] - Total cost in window: 2

# Time 1: Request cost 3  
request_api_call(3)
emit_api_calls()     # Returns [3] - Total cost in window: 2+3=5

# Time 2: Request cost 4
request_api_call(4) 
emit_api_calls()     # Returns [] - Would exceed limit (2+3+4=9 > 5)

# Time 3: emit_api_calls() called
# Returns [4] - Request from time 0 (cost 2) expires, window now has cost 3+4=7 > 5

# Time 4: emit_api_calls() called  
# Returns [] - Still exceeds limit (3+4=7 > 5)

# Time 5: emit_api_calls() called
# Returns [4] - Request from time 1 (cost 3) expires, window now has cost 4 <= 5

TIPS:
-----
PART 1:
- Use a simple queue to store pending requests
- Track used capacity when processing requests
- Reject individual requests that exceed the rate limit

PART 2:
- Use a queue for pending requests AND a separate structure for recent requests
- Track time and cost for each processed request
- Implement window expiration logic
- Maintain running sum of costs in the current window

BONUS CHALLENGE - Latency Optimization:
---------------------------------------
Consider how to minimize average latency between request and emission.
Instead of processing large requests first, process smaller requests to reduce
average waiting time.

TEST YOUR SOLUTION:
------------------
Run the test cases below to verify your implementation.
"""

from typing import List
from collections import deque

class BasicApiRateLimiter:
    """
    PART 1: Basic rate limiter with per-second rate limiting.
    """
    def __init__(self, rate_limit: int):
        """
        Initialize the basic rate limiter.
        
        Args:
            rate_limit: Maximum cost units that can be processed per second
        """
        # TODO: Initialize your data structures here
        pass
    
    def request_api_call(self, cost: int) -> None:
        """
        Request an API call with the given cost.
        
        Args:
            cost: The cost of the API call
        """
        # TODO: Add the request to your queue
        pass
    
    def emit_api_calls(self) -> List[int]:
        """
        Process pending API calls, respecting the rate limit.
        Called once per second by the automated system.
        
        Returns:
            List of costs for API calls that were processed this second
        """
        # TODO: Process requests from queue, respecting rate limit
        # TODO: Return list of processed costs in order
        pass

class WindowedApiRateLimiter:
    """
    PART 2: Windowed rate limiter with sliding window rate limiting.
    """
    def __init__(self, rate_limit: int, rate_limit_window: int):
        """
        Initialize the windowed rate limiter.
        
        Args:
            rate_limit: Maximum cost units that can be processed within the window
            rate_limit_window: Window size in seconds
        """
        # TODO: Initialize your data structures here
        # You'll need to track:
        # - Pending requests queue
        # - Recent requests with timestamps
        # - Current time
        # - Running sum of costs in current window
        pass
    
    def request_api_call(self, cost: int) -> None:
        """
        Request an API call with the given cost.
        
        Args:
            cost: The cost of the API call
        """
        # TODO: Add the request to your queue
        # TODO: Reject requests that exceed the rate limit
        pass
    
    def emit_api_calls(self) -> List[int]:
        """
        Process pending API calls, respecting the windowed rate limit.
        Called once per second by the automated system.
        
        Returns:
            List of costs for API calls that were processed this second
        """
        # TODO: Increment time
        # TODO: Expire old requests from the window
        # TODO: Process new requests while respecting windowed rate limit
        # TODO: Return list of processed costs in order
        pass

# Test Cases
def test_basic_rate_limiter():
    """Test the basic rate limiter functionality."""
    print("Testing Basic API Rate Limiter (Part 1)...")
    
    rl = BasicApiRateLimiter(4)
    rl.request_api_call(2)
    rl.request_api_call(2)
    rl.request_api_call(1)
    rl.request_api_call(1)
    
    result1 = rl.emit_api_calls()
    print(f"Test 1 - First emit: {result1}")
    assert result1 == [2, 2], f"Expected [2, 2], got {result1}"
    
    rl.request_api_call(3)
    result2 = rl.emit_api_calls()
    print(f"Test 1 - Second emit: {result2}")
    assert result2 == [1, 1], f"Expected [1, 1], got {result2}"
    
    result3 = rl.emit_api_calls()
    print(f"Test 1 - Third emit: {result3}")
    assert result3 == [3], f"Expected [3], got {result3}"
    
    print("Basic rate limiter tests passed! ✅")

def test_windowed_rate_limiter():
    """Test the windowed rate limiter functionality."""
    print("\nTesting Windowed API Rate Limiter (Part 2)...")
    
    rl = WindowedApiRateLimiter(5, 3)
    
    # Time 0
    rl.request_api_call(2)
    result1 = rl.emit_api_calls()
    print(f"Test 2 - Time 0: {result1}")
    assert result1 == [2], f"Expected [2], got {result1}"
    
    # Time 1
    rl.request_api_call(3)
    result2 = rl.emit_api_calls()
    print(f"Test 2 - Time 1: {result2}")
    assert result2 == [3], f"Expected [3], got {result2}"
    
    # Time 2
    rl.request_api_call(4)
    result3 = rl.emit_api_calls()
    print(f"Test 2 - Time 2: {result3}")
    assert result3 == [], f"Expected [], got {result3}"
    
    # Time 3
    result4 = rl.emit_api_calls()
    print(f"Test 2 - Time 3: {result4}")
    assert result4 == [4], f"Expected [4], got {result4}"
    
    # Time 4
    result5 = rl.emit_api_calls()
    print(f"Test 2 - Time 4: {result5}")
    assert result5 == [], f"Expected [], got {result5}"
    
    # Time 5
    result6 = rl.emit_api_calls()
    print(f"Test 2 - Time 5: {result6}")
    assert result6 == [], f"Expected [], got {result6}"
    
    print("Windowed rate limiter tests passed! ✅")

def test_edge_cases():
    """Test edge cases for both rate limiters."""
    print("\nTesting Edge Cases...")
    
    # Test request exceeding rate limit
    rl1 = BasicApiRateLimiter(4)
    rl1.request_api_call(5)  # Exceeds limit
    rl1.request_api_call(2)
    rl1.request_api_call(1)
    
    result = rl1.emit_api_calls()
    print(f"Edge case - Request exceeding limit: {result}")
    assert result == [2, 1], f"Expected [2, 1], got {result}"
    
    # Test empty queue
    rl2 = BasicApiRateLimiter(4)
    result = rl2.emit_api_calls()
    print(f"Edge case - Empty queue: {result}")
    assert result == [], f"Expected [], got {result}"
    
    print("Edge case tests passed! ✅")

if __name__ == "__main__":
    test_basic_rate_limiter()
    test_windowed_rate_limiter()
    test_edge_cases()
    print("\n🎉 All tests passed! You've successfully implemented both parts of the API rate limiter!")

















