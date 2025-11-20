"""
API RATE LIMITER INTERVIEW QUESTION
===================================

PROBLEM DESCRIPTION:
You are building an API rate limiter for a bank's APIs that are not built for large volumes.
You need to queue up requests and send them within some rate limit.

REQUIREMENTS:
1. Track the sum of costs of calls made in the last N seconds
2. Allow only up to RATE_LIMIT cost of calls within RATE_LIMIT_WINDOW seconds
3. Minimize average latency between request and emission

KEY CONCEPTS:
- Sliding window rate limiting
- Queue management
- Time-based expiration
- Latency optimization

EXAMPLES:

Example 1 - Basic Rate Limiting:
RATE_LIMIT = 5, RATE_LIMIT_WINDOW = 3

At t=0: request_api_call(2) → queue: [2]
emit_api_calls() → returns [2], recent: [(0,2)], sum: 2

At t=1: request_api_call(3) → queue: [3]
emit_api_calls() → returns [3], recent: [(0,2), (1,3)], sum: 5

At t=2: request_api_call(4) → queue: [4]
emit_api_calls() → returns [], recent: [(0,2), (1,3)], sum: 5
(4 would exceed limit of 5)

At t=3: emit_api_calls() → returns [4], recent: [(1,3), (3,4)], sum: 7
(expired (0,2), now sum is 3+4=7, but 7>5, so this is wrong!)

Wait, let me recalculate...
At t=3: (0,2) expires, recent: [(1,3)], sum: 3
Can add 4? 3+4=7 > 5, so NO.

At t=4: (1,3) expires, recent: [], sum: 0
Can add 4? 0+4=4 <= 5, so YES.

Example 2 - Latency Optimization:
RATE_LIMIT = 3, RATE_LIMIT_WINDOW = 1

At t=0: requests [2, 2, 1, 1] → queue: [2, 2, 1, 1]

Naive approach (FIFO):
emit_api_calls() → [2] (latency: 0)
emit_api_calls() → [2] (latency: 1) 
emit_api_calls() → [1, 1] (latency: 2)
Average latency: (0+1+2+2)/4 = 1.25

Optimized approach (smallest first):
emit_api_calls() → [1, 1] (latency: 0)
emit_api_calls() → [2] (latency: 1)
emit_api_calls() → [2] (latency: 2)
Average latency: (0+0+1+2)/4 = 0.75

TASK:
Implement an ApiRateLimiter class with:
1. request_api_call(cost) - adds request to queue
2. emit_api_calls() - processes queued requests within rate limit
3. Optimize for minimum average latency

CONSTRAINTS:
- Rate limit is based on sum of costs in sliding window
- Requests expire after RATE_LIMIT_WINDOW seconds
- emit_api_calls() is called exactly once per second
- Minimize average latency (time between request and emission)

INTERVIEW TIPS:
- Think about sliding window with deque
- Consider latency optimization strategies
- Handle edge cases (empty queue, expired requests)
- Discuss trade-offs between fairness and latency
"""

from typing import List
from collections import deque
import heapq

class ApiRateLimiter:
    """
    API Rate Limiter with sliding window and latency optimization
    """
    
    def __init__(self, rate_limit: int, rate_limit_window: int):
        """
        Initialize rate limiter
        
        Args:
            rate_limit: Maximum cost allowed in window
            rate_limit_window: Time window in seconds
        """
        self.rate_limit = rate_limit
        self.window = rate_limit_window
        self.recent = deque()  # (timestamp, cost) pairs for active window
        self.queue = deque()   # Pending requests (cost, request_time)
        self.current_time = 0
        self.recent_sum = 0
    
    def request_api_call(self, cost: int) -> None:
        """
        Add a new API call request to the queue
        
        Args:
            cost: Cost of the API call
        """
        # TODO: Implement this function
        pass
    
    def emit_api_calls(self) -> List[int]:
        """
        Process queued requests within rate limit
        
        Returns:
            List of costs that were successfully emitted
        """
        # TODO: Implement this function
        pass
    
    def _expire_old_requests(self) -> None:
        """
        Remove requests that are outside the sliding window
        """
        # TODO: Implement this helper function
        pass
    
    def _process_requests(self) -> List[int]:
        """
        Process requests from queue while respecting rate limit
        
        Returns:
            List of costs that were emitted
        """
        # TODO: Implement this helper function
        pass


# Test cases
if __name__ == "__main__":
    print("=== API RATE LIMITER TEST CASES ===\n")
    
    # Test 1: Basic rate limiting
    print("Test 1 - Basic Rate Limiting:")
    rl = ApiRateLimiter(5, 3)
    rl.request_api_call(2)
    result = rl.emit_api_calls()
    print(f"  Request(2), Emit: {result}")  # Expected: [2]
    
    rl.request_api_call(3)
    result = rl.emit_api_calls()
    print(f"  Request(3), Emit: {result}")  # Expected: [3]
    
    rl.request_api_call(4)
    result = rl.emit_api_calls()
    print(f"  Request(4), Emit: {result}")  # Expected: [] (would exceed limit)
    
    # Test 2: Window expiration
    print("\nTest 2 - Window Expiration:")
    rl = ApiRateLimiter(5, 3)
    rl.request_api_call(2)
    rl.emit_api_calls()  # t=0: emit [2], sum=2
    
    rl.request_api_call(3)
    rl.emit_api_calls()  # t=1: emit [3], sum=5
    
    rl.request_api_call(4)
    rl.emit_api_calls()  # t=2: emit [], sum=5 (can't fit 4)
    
    result = rl.emit_api_calls()  # t=3: emit [4], sum=3 (2 expired)
    print(f"  After expiration, Emit: {result}")  # Expected: [4]
    
    # Test 3: Multiple requests in one second
    print("\nTest 3 - Multiple Requests:")
    rl = ApiRateLimiter(4, 1)
    rl.request_api_call(2)
    rl.request_api_call(2)
    rl.request_api_call(1)
    rl.request_api_call(1)
    
    result = rl.emit_api_calls()
    print(f"  Multiple requests, Emit: {result}")  # Expected: [2, 2] (total=4)
    
    result = rl.emit_api_calls()
    print(f"  Next second, Emit: {result}")  # Expected: [1, 1] (total=2)
    
    # Test 4: Latency optimization
    print("\nTest 4 - Latency Optimization:")
    rl = ApiRateLimiter(3, 1)
    rl.request_api_call(2)
    rl.request_api_call(2)
    rl.request_api_call(1)
    rl.request_api_call(1)
    
    # Optimized: process smaller requests first
    result = rl.emit_api_calls()
    print(f"  Optimized Emit: {result}")  # Expected: [1, 1] (better latency)
    
    result = rl.emit_api_calls()
    print(f"  Next Emit: {result}")  # Expected: [2] (one of the 2s)
    
    result = rl.emit_api_calls()
    print(f"  Final Emit: {result}")  # Expected: [2] (remaining 2)




















