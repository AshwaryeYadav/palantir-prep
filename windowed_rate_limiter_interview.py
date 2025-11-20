"""
Windowed API Rate Limiter - Interview Problem
============================================

You are building a rate limiter for bank APIs that are not designed for large volumes.
The system needs to queue up requests and send them within a rate limit.

PROBLEM STATEMENT:
-----------------
Implement a windowed rate limiter that tracks the total cost of API calls made 
within a sliding time window. No more than RATE_LIMIT cost units can be processed 
within the last RATE_LIMIT_WINDOW seconds.

KEY REQUIREMENTS:
----------------
- `request_api_call(cost: int)` - Called when a caller wants to make an API call
- `emit_api_calls() -> List[int]` - Called once per second by automated system
- Requests are processed in FIFO order (first requested, first processed)
- If a single request exceeds the rate limit, it should be rejected
- Track sliding window of processed requests with their timestamps
- Expire old requests when they fall outside the window

EXAMPLE:
--------
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
# Returns [] - Still exceeds limit (3+4=7 > 5)

# Time 6: emit_api_calls() called
# Returns [] - Still exceeds limit (4=4 <= 5, but we need to check if 3 expired)

# Time 7: emit_api_calls() called
# Returns [4] - Request from time 1 (cost 3) expires, window now has cost 4 <= 5

WINDOW EXPIRATION CLARIFICATION:
------------------------------
If window = 3 seconds and a request was made at time t=0:
- At time t=3, the request is still counted (inclusive)
- At time t=4, the request expires and is no longer counted

So a request at time t expires at time t + window (exclusive).

TIPS:
-----
1. Use a queue to store pending requests
2. Use a separate structure to track recent requests with timestamps
3. Maintain a running sum of costs in the current window
4. Implement window expiration logic to remove old requests
5. Track current time and increment it on each emit_api_calls()
6. Reject individual requests that exceed the rate limit

DATA STRUCTURES TO CONSIDER:
---------------------------
- Queue for pending requests
- Queue/deque for recent requests with (timestamp, cost) pairs
- Running sum of costs in current window
- Current time counter

TEST YOUR SOLUTION:
------------------
Run the test cases below to verify your implementation.
"""

from typing import List
from collections import deque

class WindowedApiRateLimiter:
    """
    Windowed rate limiter with sliding window rate limiting.
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
def test_basic_windowed_limiter():
    """Test basic windowed rate limiter functionality."""
    print("Testing Basic Windowed Rate Limiter...")
    
    rl = WindowedApiRateLimiter(5, 3)
    
    # Time 0
    rl.request_api_call(2)
    result1 = rl.emit_api_calls()
    print(f"Time 0: {result1}")
    assert result1 == [2], f"Expected [2], got {result1}"
    
    # Time 1
    rl.request_api_call(3)
    result2 = rl.emit_api_calls()
    print(f"Time 1: {result2}")
    assert result2 == [3], f"Expected [3], got {result2}"
    
    # Time 2
    rl.request_api_call(4)
    result3 = rl.emit_api_calls()
    print(f"Time 2: {result3}")
    assert result3 == [], f"Expected [], got {result3}"
    
    # Time 3
    result4 = rl.emit_api_calls()
    print(f"Time 3: {result4}")
    assert result4 == [4], f"Expected [4], got {result4}"
    
    # Time 4
    result5 = rl.emit_api_calls()
    print(f"Time 4: {result5}")
    assert result5 == [], f"Expected [], got {result5}"
    
    # Time 5
    result6 = rl.emit_api_calls()
    print(f"Time 5: {result6}")
    assert result6 == [], f"Expected [], got {result6}"
    
    # Time 6
    result7 = rl.emit_api_calls()
    print(f"Time 6: {result7}")
    assert result7 == [], f"Expected [], got {result7}"
    
    # Time 7
    result8 = rl.emit_api_calls()
    print(f"Time 7: {result8}")
    assert result8 == [], f"Expected [], got {result8}"
    
    print("Basic windowed rate limiter tests passed! ✅")

def test_request_rejection():
    """Test that requests exceeding rate limit are rejected."""
    print("\nTesting Request Rejection...")
    
    rl = WindowedApiRateLimiter(5, 3)
    
    # Request that exceeds the rate limit should be rejected
    rl.request_api_call(6)  # Exceeds limit of 5
    rl.request_api_call(2)
    rl.request_api_call(3)
    
    result1 = rl.emit_api_calls()
    print(f"With rejected request: {result1}")
    assert result1 == [2], f"Expected [2], got {result1}"
    
    result2 = rl.emit_api_calls()
    print(f"Next emit: {result2}")
    assert result2 == [3], f"Expected [3], got {result2}"
    
    print("Request rejection tests passed! ✅")

def test_window_expiration():
    """Test window expiration logic."""
    print("\nTesting Window Expiration...")
    
    rl = WindowedApiRateLimiter(4, 2)  # Smaller window for easier testing
    
    # Time 0: Add request
    rl.request_api_call(2)
    result1 = rl.emit_api_calls()
    print(f"Time 0: {result1}")
    assert result1 == [2], f"Expected [2], got {result1}"
    
    # Time 1: Add another request
    rl.request_api_call(3)
    result2 = rl.emit_api_calls()
    print(f"Time 1: {result2}")
    assert result2 == [3], f"Expected [3], got {result2}"
    
    # Time 2: Try to add request that would exceed limit
    rl.request_api_call(2)
    result3 = rl.emit_api_calls()
    print(f"Time 2: {result3}")
    assert result3 == [], f"Expected [], got {result3}"
    
    # Time 3: First request should expire, second request should still be in window
    result4 = rl.emit_api_calls()
    print(f"Time 3: {result4}")
    assert result4 == [2], f"Expected [2], got {result4}"
    
    print("Window expiration tests passed! ✅")

def test_empty_queue():
    """Test behavior with empty queue."""
    print("\nTesting Empty Queue...")
    
    rl = WindowedApiRateLimiter(5, 3)
    
    result1 = rl.emit_api_calls()
    print(f"Empty queue: {result1}")
    assert result1 == [], f"Expected [], got {result1}"
    
    result2 = rl.emit_api_calls()
    print(f"Still empty: {result2}")
    assert result2 == [], f"Expected [], got {result2}"
    
    print("Empty queue tests passed! ✅")

def test_complex_scenario():
    """Test a more complex scenario with multiple requests."""
    print("\nTesting Complex Scenario...")
    
    rl = WindowedApiRateLimiter(6, 3)
    
    # Time 0: Multiple requests
    rl.request_api_call(1)
    rl.request_api_call(2)
    rl.request_api_call(3)
    result1 = rl.emit_api_calls()
    print(f"Time 0: {result1}")
    assert result1 == [1, 2, 3], f"Expected [1, 2, 3], got {result1}"
    
    # Time 1: Request that would exceed limit
    rl.request_api_call(4)
    result2 = rl.emit_api_calls()
    print(f"Time 1: {result2}")
    assert result2 == [], f"Expected [], got {result2}"
    
    # Time 2: Another request
    rl.request_api_call(2)
    result3 = rl.emit_api_calls()
    print(f"Time 2: {result3}")
    assert result3 == [], f"Expected [], got {result3}"
    
    # Time 3: First request expires, window now has cost 2+3+4=9 > 6
    result4 = rl.emit_api_calls()
    print(f"Time 3: {result4}")
    assert result4 == [], f"Expected [], got {result4}"
    
    # Time 4: Second request expires, window now has cost 3+4=7 > 6
    result5 = rl.emit_api_calls()
    print(f"Time 4: {result5}")
    assert result5 == [], f"Expected [], got {result5}"
    
    # Time 5: Third request expires, window now has cost 4 <= 6
    result6 = rl.emit_api_calls()
    print(f"Time 5: {result6}")
    assert result6 == [4], f"Expected [4], got {result6}"
    
    # Time 6: Fourth request can now be processed
    result7 = rl.emit_api_calls()
    print(f"Time 6: {result7}")
    assert result7 == [2], f"Expected [2], got {result7}"
    
    print("Complex scenario tests passed! ✅")

if __name__ == "__main__":
    test_basic_windowed_limiter()
    test_request_rejection()
    test_window_expiration()
    test_empty_queue()
    test_complex_scenario()
    print("\n🎉 All tests passed! You've successfully implemented the windowed API rate limiter!")

















