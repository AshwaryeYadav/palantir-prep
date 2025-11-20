#!/usr/bin/env python3
"""
FRAUD DETECTION INTERVIEW PROBLEM
================================

Company: Stripe
Role: Software Engineer / Data Engineer
Difficulty: Medium-Hard

PROBLEM DESCRIPTION:
===================

You are working on Stripe's fraud detection team. The team wants to reduce merchant 
fraud risk with minimal impact on good merchants using machine learning. You need to 
develop a system to assess fraud risk for transactions.

The system assigns each merchant a fraud score based on their transactions and a set 
of predefined rules. Each transaction can have different risk factors (e.g., 
transaction amount, frequency of similar transactions, user activity).

SCORING LOGIC:
==============

For each merchant, you need to calculate their fraud score using the following steps:

1. INITIALIZATION:
   - Initialize a merchant's current_score as their base_score

2. TRANSACTION PROCESSING (3 separate passes over the entire transaction list):
   
   STEP 1 - Multiplicative Factor:
   - If transaction amount > corresponding rule's min_transaction_amount
   - Multiply current_score by corresponding rule's multiplicative_factor
   
   STEP 2 - Additive Factors (Cumulative):
   - If same customer_id has made 3+ transactions to that merchant_id (including current)
   - Add ALL corresponding rules' additive_factors to current_score, cumulatively
   - Example: If merchant's score at 3rd transaction is X (includes 1st, 2nd, 3rd additive_factors),
     then 4th transaction should be X + 4th transaction's additive_factor
   
   STEP 3 - Penalty/Bonus based on Hour:
   - If transaction is 3rd+ from same customer_id in same hour for same merchant_id
   - Penalty (Add): If hour is 12-17 (inclusive), add penalty each time
   - Bonus (Subtract): If hour is 9-11 or 18-21 (inclusive), subtract penalty each time
   - No action: If hour falls outside above ranges

INPUT FORMAT:
=============

transactions_list: List of length n (1 ≤ n ≤ 1000)
- Each transaction: "merchant_id,amount,customer_id,hour"
- merchant_id: string (length > 0)
- amount: integer payment amount
- customer_id: string (length > 0) 
- hour: integer (0 ≤ hour ≤ 23)

rules_list: List of length n (1 ≤ n ≤ 1000)
- Each rule: "min_transaction_amount,multiplicative_factor,additive_factor,penalty"
- min_transaction_amount: integer
- multiplicative_factor: integer
- additive_factor: integer
- penalty: integer

merchants_list: List of length m (1 ≤ m ≤ 1000)
- Each merchant: "merchant_id,base_score"
- merchant_id: string (length > 0)
- base_score: integer (1 ≤ base_score ≤ 50)

OUTPUT FORMAT:
==============

Return a list of comma-separated strings denoting the merchants (in lexicographical order) 
and their fraud scores.

EXAMPLE:
========

Input:
transactions_list = [
    "merchant1,1200,customer1,10",
    "merchant1,500,customer1,10", 
    "merchant2,2400,customer1,15",
    "merchant1,800,customer1,16",
    "merchant1,1000,customer2,17",
    "merchant1,1400,customer1,10"
]

rules_list = [
    "1000,2,8,15",
    "1400,5,3,19", 
    "2300,3,17,3",
    "1800,2,9,6",
    "1000,4,8,2",
    "1200,3,11,7"
]

merchants_list = [
    "merchant1,10",
    "merchant2,20"
]

Output:
[
    "merchant1,50",  # 10 -> 10*2=20 -> 20*3=60 -> 60+8+3+9+11=91 -> 91-15-19-7=50
    "merchant2,60"   # 20 -> 20*3=60
]

CONSTRAINTS:
============
- You may assume there won't be any integer overflows
- All merchant_ids and customer_ids are non-empty strings
- Hours are valid integers between 0-23
- Base scores are between 1-50

IMPLEMENTATION TIPS:
===================

1. Parse the input strings carefully - they're comma-separated
2. Keep track of customer transaction counts per merchant
3. Keep track of customer transaction counts per merchant per hour
4. Process transactions in 3 separate passes as specified
5. Sort the final results lexicographically by merchant_id
6. Be careful with the cumulative additive factors logic
7. The penalty/bonus logic applies to ALL transactions from the 3rd onwards, not just the current one

FUNCTION SIGNATURE:
==================
"""

def calculate_merchant_fraud_score(transactions_list, rules_list, merchants_list):
    """
    Calculate fraud scores for merchants based on transaction patterns and rules.
    
    Args:
        transactions_list: List of transaction strings in format "merchant_id,amount,customer_id,hour"
        rules_list: List of rule strings in format "min_amount,mult_factor,add_factor,penalty"
        merchants_list: List of merchant strings in format "merchant_id,base_score"
    
    Returns:
        List of strings in format "merchant_id,score" sorted lexicographically
    """
    # Parse merchants and initialize scores
    merchant_scores = {}
    for merchant_str in merchants_list:
        merchant_id, base_score = merchant_str.split(',')
        merchant_scores[merchant_id] = int(base_score)
    
    # Parse transactions and rules
    transactions = []
    rules = []
    
    for i, transaction_str in enumerate(transactions_list):
        merchant_id, amount, customer_id, hour = transaction_str.split(',')
        transactions.append({
            'merchant_id': merchant_id,
            'amount': int(amount),
            'customer_id': customer_id,
            'hour': int(hour)
        })
    
    for rule_str in rules_list:
        min_amount, mult_factor, add_factor, penalty = rule_str.split(',')
        rules.append({
            'min_amount': int(min_amount),
            'mult_factor': int(mult_factor),
            'add_factor': int(add_factor),
            'penalty': int(penalty)
        })
    
    # Track customer transaction counts per merchant
    customer_merchant_counts = {}  # (customer_id, merchant_id) -> count
    customer_merchant_hour_counts = {}  # (customer_id, merchant_id, hour) -> count
    
    # STEP 1: Apply multiplicative factors
    for i, transaction in enumerate(transactions):
        merchant_id = transaction['merchant_id']
        amount = transaction['amount']
        rule = rules[i]
        
        if amount > rule['min_amount']:
            merchant_scores[merchant_id] *= rule['mult_factor']
    
    # STEP 2: Apply cumulative additive factors
    # For each merchant, find all transactions where customer has 3+ transactions to that merchant
    for merchant_id in merchant_scores.keys():
        # Find all transactions for this merchant
        merchant_transactions = []
        for i, transaction in enumerate(transactions):
            if transaction['merchant_id'] == merchant_id:
                merchant_transactions.append(i)
        
        # For each customer-merchant pair, check if customer has 3+ transactions
        customer_counts = {}
        for i in merchant_transactions:
            customer_id = transactions[i]['customer_id']
            customer_counts[customer_id] = customer_counts.get(customer_id, 0) + 1
        
        # Apply additive factors for customers with 3+ transactions
        for customer_id, count in customer_counts.items():
            if count >= 3:
                # Add additive factors for ALL transactions from this customer to this merchant
                for i in merchant_transactions:
                    if transactions[i]['customer_id'] == customer_id:
                        merchant_scores[merchant_id] += rules[i]['add_factor']
    
    # STEP 3: Apply penalty/bonus based on hour patterns
    # For each merchant, find all transactions where customer has 3+ transactions in same hour
    for merchant_id in merchant_scores.keys():
        # Find all transactions for this merchant
        merchant_transactions = []
        for i, transaction in enumerate(transactions):
            if transaction['merchant_id'] == merchant_id:
                merchant_transactions.append(i)
        
        # Group by (customer_id, hour) and check counts
        customer_hour_counts = {}
        for i in merchant_transactions:
            customer_id = transactions[i]['customer_id']
            hour = transactions[i]['hour']
            key = (customer_id, hour)
            customer_hour_counts[key] = customer_hour_counts.get(key, 0) + 1
        
        # Apply penalty/bonus for customers with 3+ transactions in same hour
        for (customer_id, hour), count in customer_hour_counts.items():
            if count >= 3:
                # Apply penalty/bonus for ALL transactions from this customer in this hour
                for i in merchant_transactions:
                    if (transactions[i]['customer_id'] == customer_id and 
                        transactions[i]['hour'] == hour):
                        rule = rules[i]
                        if 12 <= hour <= 17:  # Penalty: Add penalty
                            merchant_scores[merchant_id] += rule['penalty']
                        elif (9 <= hour <= 11) or (18 <= hour <= 21):  # Bonus: Subtract penalty
                            merchant_scores[merchant_id] -= rule['penalty']
    
    # Format results and sort lexicographically
    result = []
    for merchant_id in sorted(merchant_scores.keys()):
        result.append(f"{merchant_id},{merchant_scores[merchant_id]}")
    
    return result


def test_calculate_merchant_fraud_score():
    """Test cases for the fraud detection function."""
    
    # Test Case 1: Example from problem description
    transactions1 = [
        "merchant1,1200,customer1,10",
        "merchant1,500,customer1,10", 
        "merchant2,2400,customer1,15",
        "merchant1,800,customer1,16",
        "merchant1,1000,customer2,17",
        "merchant1,1400,customer1,10"
    ]
    
    rules1 = [
        "1000,2,8,15",
        "1400,5,3,19", 
        "2300,3,17,3",
        "1800,2,9,6",
        "1000,4,8,2",
        "1200,3,11,7"
    ]
    
    merchants1 = [
        "merchant1,10",
        "merchant2,20"
    ]
    
    expected1 = [
        "merchant1,50",
        "merchant2,60"
    ]
    
    
    result1 = calculate_merchant_fraud_score(transactions1, rules1, merchants1)
    print(f"Test 1 - Expected: {expected1}")
    print(f"Test 1 - Got: {result1}")
    print(f"Test 1 - Passed: {result1 == expected1}")
    print()
    
    # Test Case 2: Single transaction
    transactions2 = ["merchant1,500,customer1,10"]
    rules2 = ["1000,2,5,10"]
    merchants2 = ["merchant1,20"]
    expected2 = ["merchant1,20"]  # No multiplicative factor applied, no additive factors
    
    result2 = calculate_merchant_fraud_score(transactions2, rules2, merchants2)
    print(f"Test 2 - Expected: {expected2}")
    print(f"Test 2 - Got: {result2}")
    print(f"Test 2 - Passed: {result2 == expected2}")
    print()
    
    # Test Case 3: Multiple customers, same merchant
    transactions3 = [
        "merchant1,1500,customer1,10",
        "merchant1,1500,customer2,10",
        "merchant1,1500,customer1,10"
    ]
    rules3 = [
        "1000,2,5,10",
        "1000,2,5,10", 
        "1000,2,5,10"
    ]
    merchants3 = ["merchant1,10"]
    # Expected: 10 -> 10*2=20 -> 20*2=40 -> 40*2=80 -> 80+5+5+5=95 (3rd transaction triggers additive)
    
    result3 = calculate_merchant_fraud_score(transactions3, rules3, merchants3)
    print(f"Test 3 - Got: {result3}")
    print()


if __name__ == "__main__":
    print("FRAUD DETECTION INTERVIEW PROBLEM")
    print("=" * 40)
    print()
    print("This is an interview-style problem. Implement the function")
    print("calculate_merchant_fraud_score() above.")
    print()
    print("Run the test cases to verify your implementation:")
    print()
    test_calculate_merchant_fraud_score()
