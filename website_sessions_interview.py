"""
WEBSITE SESSIONS INTERVIEW QUESTION
===================================

You are given a dataset containing metadata about user sessions on a website. Each entry in this dataset represents an individual user session, with fields that include:
- user_id: a unique identifier for each user
- name: the name of the user
- login_time: the timestamp of when the user logged into the website
- logout_time: the timestamp of when the user logged off the website

Objective
---------
Identify the top 3 users who have spent the most cumulative time on the website across all their sessions.

Requirements
-----------
1) Calculate Total Session Duration
   - For each unique user_id, calculate the total time spent on the website by summing the durations of all their sessions.

2) Identify Top 3 Users
   - Identify the three users with the highest cumulative session duration.

3) Tie-Breaking Rules
   - If two or more users have the same total time, prioritize alphabetically by name
   - If there is still a tie (e.g., multiple users with identical name and session duration), sort by user_id

4) Output
   - Display the top 3 users in descending order of their total time spent on the website
   - For each user, provide their user_id, name, and total time spent in a human-readable format (e.g., hours, minutes)

Assumptions
-----------
- The login_time and logout_time fields are datetime objects
- Each user may have multiple sessions, which may not be sequentially ordered
- If fewer than 3 users exist, return only the available users in descending order of their total time spent

TASK
----
Implement `top_users_by_session_time(sessions, top_n=3)` that returns a list of dicts for the top users.

Function Signature
------------------
- Input: sessions: list[dict] with keys: 'user_id', 'name', 'login_time', 'logout_time'
- Output: list[dict] with keys: 'user_id', 'name', 'total_time' (timedelta) or formatted string

Interview Tips
--------------
- Consider using a dictionary to aggregate durations per user_id
- Be careful with time arithmetic and ensure logout_time >= login_time
- Ensure sorting respects all tie-breakers
- Decide whether to return raw timedeltas or formatted strings; align with the Output spec
- Think about stability and determinism in sorting
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


def format_duration(delta: timedelta) -> str:
    """Format a timedelta into a human-readable string like 'Xh Ym'.
    Do not change this helper's signature; you may use it in your solution.
    """
    # Guard against negative durations by clamping at zero
    total_seconds = max(0, int(delta.total_seconds()))
    total_minutes = total_seconds // 60
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m"

import heapq
def top_users_by_session_time(sessions: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Compute the top N users by total session time across all their sessions.

    Args:
        sessions: List of session records. Each record contains keys:
                  'user_id' (hashable), 'name' (str), 'login_time' (datetime), 'logout_time' (datetime)
        top_n: The number of users to return, default 3

    Returns:
        A list of dictionaries with keys: 'user_id', 'name', 'total_time' (timedelta or formatted str)
        The list must be ordered from highest to lowest total time, applying the tie-breaker rules.
    """
    maps = {}
    heap = []
    result = []
    if len(sessions) < 3:
        for session in sessions:
            duration = (session['logout_time'] - session['login_time']).total_seconds()
            result.append((session['user_id'], session['name'], duration))
        return result
    for session in sessions:
        if session['user_id'] not in maps:
            maps[session['user_id']] = (0, session['user_id'], session['name'])

        duration = (session['logout_time'] - session['login_time']).total_seconds()
        total_duration, user_id, name = maps[session['user_id']]
        maps[session['user_id']] = (total_duration + duration, user_id, name)

    # Sort by total duration (descending) and get top 3
    sorted_users = sorted(maps.items(), key=lambda x: x[1][0], reverse=True)[:3]
    
    # Return the format expected: list of tuples (user_id, name, total_duration)
    result = []
    for user_id, (total_duration, _, name) in sorted_users:
        result.append((user_id, name, total_duration))
    
    return result
# Example dataset (you can modify or extend during practice)
EXAMPLE_SESSIONS = [
    {
        'user_id': 101,
        'name': 'Alice',
        'login_time': datetime(2024, 5, 1, 9, 0),
        'logout_time': datetime(2024, 5, 1, 11, 15),
    },
    {
        'user_id': 102,
        'name': 'Bob',
        'login_time': datetime(2024, 5, 1, 10, 30),
        'logout_time': datetime(2024, 5, 1, 12, 0),
    },
    {
        'user_id': 101,
        'name': 'Alice',
        'login_time': datetime(2024, 5, 2, 14, 0),
        'logout_time': datetime(2024, 5, 2, 16, 30),
    },
    {
        'user_id': 103,
        'name': 'Charlie',
        'login_time': datetime(2024, 5, 1, 9, 45),
        'logout_time': datetime(2024, 5, 1, 10, 0),
    },
]


if __name__ == '__main__':
    # Test the function with example data
    result = top_users_by_session_time(EXAMPLE_SESSIONS, top_n=3)
    print("Top users by session time:")
    for row in result:
        print(f"User ID: {row[0]}, Name: {row[1]}, Total Duration: {row[2]}")
