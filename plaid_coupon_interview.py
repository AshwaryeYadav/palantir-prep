"""
PLAID COUPON DISCOUNT INTERVIEW QUESTION (SINGLE COUPON VERSION)
===============================================================

PROBLEM DESCRIPTION:
Write a function that finds the final pay after discount is applied to a customer cart.
You are given a SINGLE coupon that can target one or more categories.

CORE REQUIREMENTS:
1. Apply a single coupon to the cart
2. Coupon can target one or more categories
3. Handle both percentage and fixed amount discounts
4. Apply minimum item/amount restrictions per category
5. Return original total if coupon is not applicable

VALIDATION RULES:
- Exactly one of percent_discount OR amount_discount must be non-null
- Minimum requirements apply to the specific category being discounted
- If discount exceeds category subtotal, apply maximum possible discount
- Return original total if coupon cannot be applied

COUPON STRUCTURE:
{
    'categories': ['clothing', 'toy'],           # Categories this coupon can apply to
    'percent_discount': None,                    # Percentage discount (0-100)
    'amount_discount': 6,                        # Fixed amount discount
    'minimum_num_items_required': None,          # Min items in category
    'minimum_amount_required': None              # Min subtotal in category
}

EXAMPLE SCENARIOS:

Example 1 - Percentage Discount:
Cart: [
    {'price': 10.00, 'category': 'fruit'},
    {'price': 5.00, 'category': 'clothing'}
]
Coupon: { 'categories': ['fruit'], 'percent_discount': 20, 'amount_discount': None, ... }
Result: $13.00 (10*0.8 + 5 = 8 + 5)

Example 2 - Fixed Amount Discount:
Cart: [
    {'price': 20.00, 'category': 'toy'},
    {'price': 5.00, 'category': 'clothing'}
]
Coupon: { 'categories': ['toy', 'clothing'], 'percent_discount': None, 'amount_discount': 6, ... }
- toy: $20 - $6 = $14 (savings: $6)
- clothing: $5 - $6 = $0 (savings: $5)
- Choose toy (better savings)
Result: $19.00 (14 + 5)

Example 3 - Minimum Requirements:
Cart: [
    {'price': 2.00, 'category': 'fruit'},
    {'price': 8.00, 'category': 'fruit'}
]
Coupon: { 'categories': ['fruit'], 'percent_discount': 15, 'amount_discount': None, 'minimum_num_items_required': 2, 'minimum_amount_required': 10.00 }
- fruit: 2 items, $10 subtotal ✓ meets requirements
- discount: $10 * 0.15 = $1.50
Result: $8.50 (10 - 1.50)

TASK:
Implement calculate_total_with_coupon(cart_items, coupon) that:
1. Validates coupon format
2. Calculates category subtotals and counts
3. Finds the best category for the coupon
4. Returns final total after discount

INTERVIEW TIPS:
- Start with validation logic (exactly one discount type)
- Calculate category subtotals and item counts
- Find the category with maximum savings
- Handle edge cases (minimum requirements, discount exceeding subtotal)
"""

def calculate_total_with_coupon(cart_items, coupon):
    """
    Calculate final cart total after applying a single coupon
    
    Args:
        cart_items: List of dicts with 'price' and 'category'
        coupon: Single coupon dict with discount rules
    
    Returns:
        float: Final total after applying the coupon discount
    """
    percent = coupon.get("percent_discount")
    amount =coupon.get("amount_discount")

    total_price = 0
    total_price += sum(item["price"] for item in cart_items)

    target_cat = coupon.get("category")

    category_items = [items for items in cart_items if items.get("category") == target_cat]

    if not category_items:
        return total_price
    
    cat_subtotal = sum(item.get("price") for item in category_items)

    min_cart_total = coupon.get("minimum_cart_total")
    min_item_price = coupon.get("minimum_item_price")

    # Condition 1: Total cart must meet minimum threshold (if defined)
    if min_cart_total is not None and total_price < min_cart_total:
        return total_price  # Coupon not applicable if total below threshold

    # Condition 2: Each item must meet minimum item price threshold (if defined)
    if min_item_price is not None:
        # If ANY item in the category is below minimum, coupon cannot apply.
        if any(item["price"] < min_item_price for item in category_items):
            return total_price


    if percent:
        discounted = cat_subtotal * (percent/100.0)
    else:
        discounted = min(amount, cat_subtotal)
    
    discounted_catsubtotal_total = max(cat_subtotal - discounted, 0)

    other_total = sum(
        item["price"]
        for item in cart_items
        if item.get("category") != target_cat and item["price"] is not None
    )

    final_total = discounted_catsubtotal_total + other_total

    return final_total





    


# Test cases
if __name__ == "__main__":
    print("=== PLAID COUPON DISCOUNT TEST CASES ===\n")
    
    # Test 1: Basic percentage discount
    print("Test 1 - Basic Percentage Discount:")
    cart1 = [
        {'price': 10.00, 'category': 'fruit'},
        {'price': 5.00, 'category': 'clothing'}
    ]
    coupon1 = { 
        'categories': ['fruit'],
        'percent_discount': 20,
        'amount_discount': None,
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    }
    result1 = calculate_total_with_coupon(cart1, coupon1)
    print(f"  Cart: {cart1}")
    print(f"  Coupon: {coupon1}")
    print(f"  Result: ${result1:.2f}")  # Expected: $13.00 (10*0.8 + 5)
    
    # Test 2: Fixed amount discount with multiple categories
    print("\nTest 2 - Fixed Amount Discount (Multiple Categories):")
    cart2 = [
        {'price': 20.00, 'category': 'toy'},
        {'price': 5.00, 'category': 'clothing'},
        {'price': 10.00, 'category': 'fruit'}
    ]
    coupon2 = { 
        'categories': ['toy', 'clothing'],
        'percent_discount': None,
        'amount_discount': 6,
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    }
    result2 = calculate_total_with_coupon(cart2, coupon2)
    print(f"  Cart: {cart2}")
    print(f"  Coupon: {coupon2}")
    print(f"  Result: ${result2:.2f}")  # Expected: $29.00 (choose toy: 20-6=14, clothing: 5, fruit: 10)
    
    # Test 3: Invalid coupon (both discount types)
    print("\nTest 3 - Invalid Coupon (Both Discount Types):")
    cart3 = [
        {'price': 10.00, 'category': 'fruit'}
    ]
    coupon3 = { 
        'categories': ['fruit'],
        'percent_discount': 20,
        'amount_discount': 5,  # Both populated - ERROR!
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    }
    try:
        result3 = calculate_total_with_coupon(cart3, coupon3)
        print(f"  Result: ${result3:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")  # Expected: "Coupon must have exactly one..."
    
    # Test 4: Invalid coupon (both discount types)
    print("\nTest 4 - Invalid Coupon (Both Discount Types):")
    cart4 = [
        {'price': 10.00, 'category': 'fruit'}
    ]
    coupon4 = [
        { 'categories': ['fruit'],
          'percent_discount': 20,
          'amount_discount': 5,  # Both populated - ERROR!
          'minimum_num_items_required': None,
          'minimum_amount_required': None
        }
    ]
    try:
        result4 = calculate_total_with_coupon(cart4, coupon4)
        print(f"  Result: ${result4:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")  # Expected: "Coupon must have exactly one..."
    
    # Test 5: Minimum requirements not met
    print("\nTest 5 - Minimum Requirements Not Met:")
    cart5 = [
        {'price': 5.00, 'category': 'fruit'},  # Only 1 item, $5 total
        {'price': 10.00, 'category': 'toy'}
    ]
    coupon5 = [
        { 'categories': ['fruit'],
          'percent_discount': 20,
          'amount_discount': None,
          'minimum_num_items_required': 2,  # Need 2 items
          'minimum_amount_required': 10.00  # Need $10
        }
    ]
    result5 = calculate_total_with_coupon(cart5, coupon5)
    print(f"  Cart: {cart5}")
    print(f"  Coupon: {coupon5}")
    print(f"  Result: ${result5:.2f}")  # Expected: $15.00 (no discount applied)
    
    # Test 6: Discount exceeds category subtotal
    print("\nTest 6 - Discount Exceeds Subtotal:")
    cart6 = [
        {'price': 3.00, 'category': 'clothing'},
        {'price': 10.00, 'category': 'toy'}
    ]
    coupon6 = [
        { 'categories': ['clothing'],
          'percent_discount': None,
          'amount_discount': 10,  # $10 off $3 = $0 (max discount)
          'minimum_num_items_required': None,
          'minimum_amount_required': None
        }
    ]
    result6 = calculate_total_with_coupon(cart6, coupon6)
    print(f"  Cart: {cart6}")
    print(f"  Coupon: {coupon6}")
    print(f"  Result: ${result6:.2f}")  # Expected: $10.00 (3-3 + 10)

