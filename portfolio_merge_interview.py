"""
INTERVIEW QUESTION: Stock Portfolio Value Merger

You have historical records of different stocks in your portfolio, recorded on specific dates. 
The updates are sorted chronologically within each stock's record.

Key Rules:
1. On any given date, a stock's value applies from that date until the next update
2. Portfolio total = sum of all stock values on any given date
3. Only include dates when at least one stock value changes
4. Output should be in chronological order

Example:
- On May 1, you own $100 of PLTR
- On May 5, you update to show $200 of PLTR
- This means from May 1-4: PLTR = $100, from May 5 onwards: PLTR = $200

Input Format:
A list of lists, one list per stock.
Each stock's list contains tuples of (date, value) sorted by date.
- date: string in "m/d" format
- value: integer dollar value of holdings in that stock

Example Input:
[
    [('5/1', 100), ('5/5', 200)],  # PLTR
    [('5/5',  50), ('5/8', 100)],  # MSFT  
    [('5/1', 200), ('5/8', 100)]   # AMZN
]

Expected Output:
[('5/1', 300), ('5/5', 450), ('5/8', 400)]

Explanation:
- 5/1: PLTR=$100, MSFT=$0, AMZN=$200 → Total=$300
- 5/5: PLTR=$200, MSFT=$50, AMZN=$200 → Total=$450  
- 5/8: PLTR=$200, MSFT=$100, AMZN=$100 → Total=$400

INSTRUCTIONS FOR INTERVIEW ENVIRONMENT:
1. You have 45 minutes to solve this problem
2. Think about how to merge multiple sorted lists
3. Consider how to track current values for each stock
4. Handle edge cases (empty lists, single stock, etc.)
5. Write clean, readable code
6. Be prepared to explain your approach

EDGE CASES TO CONSIDER:
- Empty stock lists
- Single stock
- All stocks change on same date
- Stocks with no updates (always $0)
- Very large number of stocks/dates

Good luck!
"""
def parse_date(date_str):
    """Helper function to parse 'm/d' format for sorting"""
    part = date_str.split("/")
    month = int(part[0])
    day = int(part[1])
    return (month, day)

def format_date(month, day):
    """Helper function to format date back to 'm/d' string"""
    return f"{month}/{day}"


def merge_portfolio_records_heap(stock_records):
    """
    Merge stock portfolio records into chronological total values
    Using O(n log k) approach with min-heap where n = total records, k = unique companies
    
    Algorithm:
    1. Use min-heap to process records in chronological order
    2. Keep track of current value for each stock company
    3. Process all updates for the same date together
    4. Only output when total portfolio value changes
    
    Time Complexity: O(n log k) where n = total records, k = unique companies
    Space Complexity: O(k) for heap and current_values tracking
    
    Args:
        stock_records (list): List of lists, each containing (date, value) tuples
    
    Returns:
        list: List of (date, total_portfolio_value) tuples in chronological order
    """
    import heapq
    heap = []
    curr_value = [0] * len(stock_records)
    next_index = [0] * len(stock_records)
    result= []
    portfolio = 0
    for stock_id, stock_list in enumerate(stock_records):
        if stock_list:
            date, value = stock_list[0]
            heapq.heappush(heap, (parse_date(date), stock_id))
    prev_date = None
    while len(heap) != 0:
        prev_date = heap[0][0]
        touched = {}
        while heap and heap[0][0] == prev_date:
            stock_id = heapq.heappop(heap)[1]
            stock_updates = stock_records[stock_id]
            #Here we will find if there are any current stocks that have same day updates and from there we can check and update the cost 
            #once parsed we will update the index and see if they have to be added or not
            #if there are nothing in the same day, then we will add the next remaaining stocks into our heap to then add in all of the dates and ids, 
            final_val  = curr_value[stock_id]
            while (next_index[stock_id]<len(stock_updates) and parse_date(stock_updates[next_index[stock_id]][0]) == prev_date):
                final_val = stock_updates[next_index[stock_id]][1]
                next_index[stock_id] +=1
            
            touched[stock_id] = final_val

            if next_index[stock_id] < len(stock_updates):
                heapq.heappush(heap, (parse_date(stock_updates[next_index[stock_id]][0]), stock_id))
            
        for stock_id, new_value in touched.items(): 
            portfolio += (new_value - curr_value[stock_id])
            curr_value[stock_id] = new_value
        result.append((format_date(prev_date[0], prev_date[1]), portfolio))
      
    return result             


def parse_mmdd(s):
    m, d = s.split('/')
    return (int(m), int(d))

def merge_portfolio_records_heap(stock_records):
    from collections import defaultdict
    
    # Group updates by date
    by_date = defaultdict(list)
    for company_idx, updates in enumerate(stock_records):
        for date_str, val in updates:
            by_date[date_str].append((company_idx, val))

    # Sort all distinct dates
    sorted_dates = sorted(by_date.keys(), key=parse_mmdd)

    current = [0] * len(stock_records)  # last known value per company
    total = 0                           # running portfolio total
    out = []

    for date_str in sorted_dates:
        for company_idx, new_val in by_date[date_str]:
            old_val = current[company_idx]
            total += new_val - old_val
            current[company_idx] = new_val
        out.append((date_str, total))
    return out

    
    

# # Test cases
if __name__ == "__main__":
    print("=== PORTFOLIO MERGE TEST CASES ===\n")
    
    # Test 1: Basic example from problem
    stock_records = [
        [('5/1', 100), ('5/5', 200)],  # PLTR
        [('5/5',  50), ('5/8', 100)],  # MSFT
        [('5/1', 200), ('5/8', 100)]   # AMZN
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 300), ('5/5', 450), ('5/8', 400)]
    print(f"Test 1 - Basic example:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 2: Single stock
    stock_records = [
        [('5/1', 100), ('5/3', 150), ('5/5', 200)]
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 100), ('5/3', 150), ('5/5', 200)]
    print(f"Test 2 - Single stock:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 3: Same date updates
    stock_records = [
        [('5/1', 100)],  # PLTR
        [('5/1', 200)],  # MSFT
        [('5/1', 50)]    # AMZN
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 350)]
    print(f"Test 3 - Same date updates:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 4: Empty stock list
    stock_records = [
        [('5/1', 100)],  # PLTR
        [],              # Empty stock
        [('5/1', 200)]   # MSFT
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 300)]
    print(f"Test 4 - Empty stock list:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 5: Complex timeline
    stock_records = [
        [('5/1', 100), ('5/3', 150), ('5/7', 200)],  # Stock A
        [('5/2', 50), ('5/5', 75), ('5/8', 100)],    # Stock B
        [('5/4', 200), ('5/6', 180)]                  # Stock C
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 100), ('5/2', 150), ('5/3', 200), ('5/4', 400), 
                ('5/5', 425), ('5/6', 405), ('5/7', 455), ('5/8', 480)]
    print(f"Test 5 - Complex timeline:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 6: No changes (all same value)
    stock_records = [
        [('5/1', 100), ('5/5', 100), ('5/10', 100)],  # Stock A
        [('5/1', 200), ('5/5', 200), ('5/10', 200)]   # Stock B
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 300)]  # Only first date since no changes
    print(f"Test 6 - No value changes:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 7: Stock goes to zero
    stock_records = [
        [('5/1', 100), ('5/3', 0)],    # Stock A goes to 0
        [('5/1', 200), ('5/5', 300)]   # Stock B increases
    ]
    
    result = merge_portfolio_records_heap(stock_records)
    expected = [('5/1', 300), ('5/3', 200), ('5/5', 300)]
    print(f"Test 7 - Stock goes to zero:")
    print(f"  Input: {stock_records}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    print("=== TESTING COMPLETE ===")
    
    # Helper function tests
    print("\n=== HELPER FUNCTION TESTS ===")
    test_dates = ['5/1', '12/31', '1/1', '5/15']
    parsed = [parse_mmdd(d) for d in test_dates]
    sorted_parsed = sorted(parsed)
    print(f"  Original dates: {test_dates}")
    print(f"  Parsed: {parsed}")
    print(f"  Sorted: {sorted_parsed}")
    print(f"  Back to strings: {[f'{m}/{d}' for m, d in sorted_parsed]}")
    
    # # Initialize min-heap with first record from each stock
    # heap = []
    # current_values = {}  # Track current value for each stock
    
    # # Add first record from each stock to heap
    # for stock_id, stock_list in enumerate(stock_records):
    #     if stock_list:  # Only add if stock has records
    #         date, value = stock_list[0]
    #         heapq.heappush(heap, (parse_date(date), stock_id, 0, value))
    #         current_values[stock_id] = 0  # Start with 0, will be updated
    
    # result = []
    # prev_total = None
    
    # while heap:
    #     # Process all updates for the same date together
    #     current_date = None
    #     updates_for_date = []
        
    #     # Collect all updates for the current date
    #     while heap:
    #         date_tuple, stock_id, record_idx, value = heapq.heappop(heap)
            
    #         if current_date is None:
    #             current_date = date_tuple
    #             updates_for_date.append((stock_id, record_idx, value))
    #         elif date_tuple == current_date:
    #             updates_for_date.append((stock_id, record_idx, value))
    #         else:
    #             # Different date, put it back and break
    #             heapq.heappush(heap, (date_tuple, stock_id, record_idx, value))
    #             break
        
    #     # Apply all updates for this date
    #     for stock_id, record_idx, value in updates_for_date:
    #         current_values[stock_id] = value
            
    #         # Add next record from this stock if available
    #         stock_list = stock_records[stock_id]
    #         next_idx = record_idx + 1
    #         if next_idx < len(stock_list):
    #             next_date, next_value = stock_list[next_idx]
    #             heapq.heappush(heap, (parse_date(next_date), stock_id, next_idx, next_value))
        
    #     # Calculate total portfolio value after all updates for this date
    #     total = sum(current_values.values())
        
    #     # Only add to result if total changed
    #     if prev_total is None or total != prev_total:
    #         result.append((format_date(current_date[0], current_date[1]), total))
    #         prev_total = total
    
    # return result