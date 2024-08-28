import stripe # type: ignore

# Set your secret key here
stripe.api_key = "sk_test_51PrZCB00YaJGfbxsi3aqzEyBDcsbJHfIzQLeq49RIwYjEk1UI0V4VlLZmppsMRUCYci41R7Ccrqzqh0Jh8Ui7IBc00j9Rxg52v"

# Function to retrieve a charge (transaction) by its ID
def get_transaction_details(transaction_id):
    try:
        charge = stripe.Charge.retrieve(transaction_id)
        print(charge["amount"]/100)
        return charge["amount"]/100
    except stripe.error.StripeError as e:
        print(f"Error retrieving transaction details: {e}")
        return "Error retrieving transaction details"

def get_subscription_amount(charge_id):
    
    # Replace this with your actual test charge ID
    charge = stripe.Charge.retrieve(charge_id)

    # Step 2: Get the customer ID from the charge
    customer_id = charge.customer

    # Step 3: Get the customer's subscription schedule
    schedules = stripe.SubscriptionSchedule.list(customer=customer_id)

    # Assume there's only one upcoming subscription schedule per customer
    schedule = schedules.data[0]
    subscription_id = schedule.subscription

    upcoming_invoice = stripe.Invoice.upcoming(
    customer=customer_id,
    subscription=subscription_id
)
    amount_due = upcoming_invoice['amount_due']
    
    amount = amount_due/100
    print(f"Amount Due: {amount_due/100} {upcoming_invoice['currency'].upper()}")  # Amount is in cents

    # Step 4: Get the details of the first phase (upcoming phase)
    subscription_id = schedule.subscription
    return amount

get_subscription_amount("ch_3PsoDW00YaJGfbxs0yUfTLkc")