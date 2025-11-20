"""
PAYMENT RECONCILIATION INTERVIEW QUESTION
=========================================

You are working on Stripe's Invoicing product and need to reconcile payments with invoices.

Write a program that matches incoming payments to their corresponding invoices based on the 
"memo line" of the payment.

INPUT FORMAT:
The input is a single comma-separated string where:
- First 3 values: payment_id, amount, memo
- Remaining values: invoice data in groups of 3 (invoice_id, due_date, amount_due)

PAYMENT FORMAT:
1. Payment ID (e.g., "payment123")
2. Payment Amount in USD minor units (e.g., $1.00 = 100)
3. Memo Line: Always follows the format "Paying off: {INVOICE}" where {INVOICE} is the invoice ID

INVOICE FORMAT (in groups of 3):
1. Invoice ID
2. Due Date (e.g., "2024-01-01")
3. Amount Due in USD minor units (e.g., $1.00 = 100)

EXAMPLE INPUT:
input_str = "payment5, 1000, Paying off: invoiceC, invoiceA, 2024-01-01, 100, invoiceB, 2024-02-01, 200, invoiceC, 2023-01-30, 1000"

EXPECTED OUTPUT:
"payment5 pays off 1000 for invoiceC due on 2023-01-30"

TASK:
Implement the process_payment function that takes a single comma-separated string input and returns the formatted output string.

CONSTRAINTS:
- Payment memo always follows the pattern "Paying off: {invoice_id}"
- Amounts are in USD minor units (cents)
- There will be exactly one matching invoice (or none if not found)
"""


def process_payment(input_str):
    """
    Process a payment and match it to the corresponding invoice.
    
    Args:
        input_str (str): Single comma-separated string with payment data first, then invoice data
        
    Returns:
        str: Formatted output string indicating which invoice was paid
    """
    # Step 1: Split the input string by commas
    parts = [part.strip() for part in input_str.split(',')]
    
    # Step 2: Extract payment information (first 3 parts)
    payment_id = parts[0]
    payment_amount = int(parts[1])
    memo = parts[2]
    
    # Step 3: Extract invoice ID from memo
    # The memo follows the pattern "Paying off: <invoice_id>"
    invoice_id_from_memo = memo.split(": ")[1].strip()
    
    # Step 4: Parse invoice data (remaining parts, grouped by 3)
    invoice_data = []
    for i in range(3, len(parts), 3):
        if i + 2 < len(parts):  # Make sure we have all 3 parts
            invoice_id = parts[i]
            due_date = parts[i + 1]
            amount_due = int(parts[i + 2])
            invoice_data.append((invoice_id, due_date, amount_due))
    
    # Step 5: Match the payment to the invoice
    matched_invoice = None
    for invoice in invoice_data:
        if invoice[0] == invoice_id_from_memo:
            matched_invoice = invoice
            break
    
    # Step 6: Generate the output string
    if matched_invoice:
        invoice_id = matched_invoice[0]
        due_date = matched_invoice[1]
        output = f"{payment_id} pays off {payment_amount} for {invoice_id} due on {due_date}"
    else:
        output = f"{payment_id} does not match any invoice"
    
    return output


# Test cases
if __name__ == "__main__":
    # Test case 1: Basic example from problem description
    print("Test 1 - Basic example:")
    input_str = "payment5,1000,Paying off: invoiceC,invoiceA,2024-01-01,100,invoiceB,2024-02-01,200,invoiceC,2023-01-30,1000"
    result = process_payment(input_str)
    print(f"Output: {result}")
    print(f"Expected: payment5 pays off 1000 for invoiceC due on 2023-01-30")
    print(f"✓ Match: {result == 'payment5 pays off 1000 for invoiceC due on 2023-01-30'}\n")
    
    # Test case 2: With spaces after commas (as shown in problem description)
    print("Test 2 - With spaces after commas:")
    input_str = "paymentABC, 500, Paying off: invoiceZ, invoiceA, 2024-01-01, 100, invoiceB, 2024-02-01, 200, invoiceZ, 2023-01-30, 500"
    result = process_payment(input_str)
    print(f"Output: {result}")
    print(f"Expected: paymentABC pays off 500 for invoiceZ due on 2023-01-30")
    print(f"✓ Match: {result == 'paymentABC pays off 500 for invoiceZ due on 2023-01-30'}\n")
    
    # Test case 3: No matching invoice
    print("Test 3 - No matching invoice:")
    input_str = "paymentX,1000,Paying off: invoiceNotFound,invoiceA,2024-01-01,100,invoiceB,2024-02-01,200"
    result = process_payment(input_str)
    print(f"Output: {result}")
    print(f"Expected: paymentX does not match any invoice")
    print(f"✓ Match: {result == 'paymentX does not match any invoice'}\n")

