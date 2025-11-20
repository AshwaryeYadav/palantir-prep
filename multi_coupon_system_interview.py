"""
MULTI-COUPON SYSTEM INTERVIEW QUESTION
=====================================

PROBLEM DESCRIPTION:
Implement a coupon system that allows customers to apply multiple coupons to their cart.
Each coupon can target one or more product categories, but categories must be unique
across all applied coupons to prevent conflicts.

CORE REQUIREMENTS:
1. Apply multiple coupons to the cart simultaneously
2. Each coupon can target one or more categories
3. Categories must be unique across all coupons (no overlap)
4. Find the coupon that gives maximum discount for each item
5. Handle both percentage and fixed amount discounts
6. Apply minimum item/amount restrictions per category
7. Return total discount amount

VALIDATION RULES:
- Exactly one of percent_discount OR amount_discount must be non-null per coupon
- No category can appear in multiple coupons (unique category constraint)
- Minimum requirements apply to the specific category being discounted
- If discount exceeds category subtotal, apply maximum possible discount
- Raise ValueError if coupon stack is invalid

COUPON STRUCTURE:
{
    'categories': ['clothing', 'toy'],           # Categories this coupon can apply to
    'percent_discount': None,                    # Percentage discount (0-100)
    'amount_discount': 6,                        # Fixed amount discount
    'minimum_num_items_required': None,          # Min items in category
    'minimum_amount_required': None              # Min subtotal in category
}

ITEM STRUCTURE:
{
    'category': 'clothing',                      # Item category
    'price': 20.00,                             # Item price
    'quantity': 2                               # Item quantity
}

EXAMPLE SCENARIOS:

Example 1 - Valid Multi-Coupon Stack:
Coupons: [
    {
        'categories': ['clothing', 'toy'],
        'percent_discount': None,
        'amount_discount': 6,
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    },
    {
        'categories': ['fruit'],
        'percent_discount': 15,
        'amount_discount': None,
        'minimum_num_items_required': 2,
        'minimum_amount_required': 10.00
    }
]
Cart: [
    {'category': 'clothing', 'price': 20.00, 'quantity': 1},
    {'category': 'toy', 'price': 15.00, 'quantity': 2},
    {'category': 'fruit', 'price': 5.00, 'quantity': 3}
]
Result: $20.25 discount
- clothing: $6 discount (amount_discount)
- toy: $12 discount (amount_discount * 2 items)
- fruit: $2.25 discount (15% of $15, meets min requirements)

Example 2 - Invalid Coupon Stack (Category Overlap):
Coupons: [
    {'categories': ['clothing', 'toy'], ...},
    {'categories': ['toy'], ...}  # ERROR: 'toy' appears in both coupons
]
Result: ValueError("Duplicate category 'toy' found in coupons")

Example 3 - No Applicable Coupons:
Coupons: [{'categories': ['electronics'], ...}]
Cart: [{'category': 'clothing', 'price': 20.00, 'quantity': 1}]
Result: $0.00 discount (no applicable coupons)

TASK:
Implement calculate_total_discount(coupons, items) that:
1. Validates coupon stack for unique categories
2. For each item, finds the applicable coupon with maximum discount
3. Checks minimum requirements before applying discounts
4. Returns total discount amount

INTERVIEW TIPS:
- Start with validation logic (unique categories across coupons)
- Create a mapping from category to best coupon
- Calculate discount per item considering quantity
- Handle edge cases (no applicable coupons, minimum requirements)
- Consider both percentage and fixed amount discounts
"""

from collections import defaultdict


def calculate_total_discount(coupons, items):
    """
    Calculate total discount for items using multiple coupons.
    
    Args:
        coupons: List of coupon dictionaries
        items: List of item dictionaries with 'category', 'price', 'quantity'
    
    Returns:
        float: Total discount amount
    
    Raises:
        ValueError: If coupon stack is invalid (duplicate categories)
    """
    all_cat = []

    for c in coupons:
        percent = c.get("percent_discount")
        amount = c.get("amount_discount")

        if (percent is None and amount is None) or (percent is not None and amount is not None):
            raise ValueError("Each coupon must have exactly one discount type")
        all_cat.extend(c.get("categories", []))

    # Check for duplicate categories across coupons
    if len(all_cat) != len(set(all_cat)):
        duplicates = [cat for cat in set(all_cat) if all_cat.count(cat) > 1]
        raise ValueError(f"Duplicate category '{duplicates[0]}' found in coupons")
    cat_summary = defaultdict(lambda: {"subtotal": 0.0, "count":0})

    for item in items:
        cat = item.get("category")
        price = item.get("price")
        cat_summary[cat]["subtotal"] += price
        cat_summary[cat]["count"] += 1

    tot_discount = 0.0

    discount_cat = set()

    for coupon in coupons:
        cats = coupon.get("categories", [])
        percent = coupon.get("percent_discount")
        amount = coupon.get("amount_discount")
        min_items = coupon.get("minimum_num_items_required")
        min_amount = coupon.get("minimum_amount_required")

        best = 0.0
        best_c = None

        for cat in cats:
            if cat not in cat_summary:
                continue
            
            sub = cat_summary[cat]["subtotal"]
            count= cat_summary[cat]["count"]

            if min_items is not None and count < min_items:
                continue
            if min_amount is not None and sub < min_amount:
                continue

            if percent is not None:
                discount = sub * (percent/100.0)
            else:
                discount = min(sub, amount)
            if discount > best:
                best = discount
                best_c = cat
            
        if best_c:
            cat_summary[best_c]["subtotal"] -= best
            tot_discount += best
            discount_cat.add(best_c)

    final = sum(cat["subtotal"] for cat in cat_summary.values())
    return final 
        
        
        
        
        # Test cases
if __name__ == "__main__":
    print("=== MULTI-COUPON SYSTEM TEST CASES ===\n")
    
    # Test 1: Valid multi-coupon stack
    print("Test 1 - Valid Multi-Coupon Stack:")
    coupons1 = [
        {
            'categories': ['clothing', 'toy'],
            'percent_discount': None,
            'amount_discount': 6,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        },
        {
            'categories': ['fruit'],
            'percent_discount': 15,
            'amount_discount': None,
            'minimum_num_items_required': 2,
            'minimum_amount_required': 10.00
        }
    ]
    items1 = [
        {'category': 'clothing', 'price': 20.00},
        {'category': 'toy', 'price': 15.00},
        {'category': 'toy', 'price': 15.00},
        {'category': 'fruit', 'price': 5.00},
        {'category': 'fruit', 'price': 5.00},
        {'category': 'fruit', 'price': 5.00}
    ]
    try:
        result1 = calculate_total_discount(coupons1, items1)
        print(f"  Coupons: {len(coupons1)} coupons")
        print(f"  Items: {items1}")
        print(f"  Final Total: ${result1:.2f}")  # Expected: $44.75 (65 - 20.25)
    except ValueError as e:
        print(f"  Error: {e}")
    
    # Test 2: Invalid coupon stack (duplicate categories)
    print("\nTest 2 - Invalid Coupon Stack (Duplicate Categories):")
    coupons2 = [
        {
            'categories': ['clothing', 'toy'],
            'percent_discount': None,
            'amount_discount': 6,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        },
        {
            'categories': ['toy'],
            'percent_discount': 15,
            'amount_discount': None,
            'minimum_num_items_required': 2,
            'minimum_amount_required': 10.00
        }
    ]
    items2 = [
        {'category': 'toy', 'price': 20.00}
    ]
    try:
        result2 = calculate_total_discount(coupons2, items2)
        print(f"  Result: ${result2:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")  # Expected: "Duplicate category 'toy' found in coupons"
    
    # Test 3: No applicable coupons
    print("\nTest 3 - No Applicable Coupons:")
    coupons3 = [
        {
            'categories': ['electronics'],
            'percent_discount': 10,
            'amount_discount': None,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        }
    ]
    items3 = [
        {'category': 'clothing', 'price': 20.00},
        {'category': 'toy', 'price': 15.00}
    ]
    try:
        result3 = calculate_total_discount(coupons3, items3)
        print(f"  Coupons: {coupons3}")
        print(f"  Items: {items3}")
        print(f"  Final Total: ${result3:.2f}")  # Expected: $35.00 (no discount)
    except ValueError as e:
        print(f"  Error: {e}")
    
    # Test 4: Minimum requirements not met
    print("\nTest 4 - Minimum Requirements Not Met:")
    coupons4 = [
        {
            'categories': ['fruit'],
            'percent_discount': 20,
            'amount_discount': None,
            'minimum_num_items_required': 3,  # Need 3 items
            'minimum_amount_required': 20.00  # Need $20
        }
    ]
    items4 = [
        {'category': 'fruit', 'price': 5.00},
        {'category': 'fruit', 'price': 5.00}  # Only 2 items, $10 total
    ]
    try:
        result4 = calculate_total_discount(coupons4, items4)
        print(f"  Coupons: {coupons4}")
        print(f"  Items: {items4}")
        print(f"  Final Total: ${result4:.2f}")  # Expected: $10.00 (no discount applied)
    except ValueError as e:
        print(f"  Error: {e}")
    
    # Test 5: Mixed discount types
    print("\nTest 5 - Mixed Discount Types:")
    coupons5 = [
        {
            'categories': ['clothing'],
            'percent_discount': 25,
            'amount_discount': None,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        },
        {
            'categories': ['toy'],
            'percent_discount': None,
            'amount_discount': 8,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        }
    ]
    items5 = [
        {'category': 'clothing', 'price': 40.00},  # 25% of $40 = $10
        {'category': 'toy', 'price': 15.00}       # $8 discount
    ]
    try:
        result5 = calculate_total_discount(coupons5, items5)
        print(f"  Coupons: {coupons5}")
        print(f"  Items: {items5}")
        print(f"  Final Total: ${result5:.2f}")  # Expected: $37.00 (55 - 18)
    except ValueError as e:
        print(f"  Error: {e}")
    
    # Test 6: Discount exceeds item value
    print("\nTest 6 - Discount Exceeds Item Value:")
    coupons6 = [
        {
            'categories': ['clothing'],
            'percent_discount': None,
            'amount_discount': 15,  # $15 off
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        }
    ]
    items6 = [
        {'category': 'clothing', 'price': 10.00}  # $10 item, $15 discount
    ]
    try:
        result6 = calculate_total_discount(coupons6, items6)
        print(f"  Coupons: {coupons6}")
        print(f"  Items: {items6}")
        print(f"  Final Total: ${result6:.2f}")  # Expected: $0.00 (10 - 10)
    except ValueError as e:
        print(f"  Error: {e}")
