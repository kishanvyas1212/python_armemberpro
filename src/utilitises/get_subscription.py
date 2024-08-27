import stripe

# Replace 'your_stripe_secret_key' with your actual secret key
stripe.api_key = 'sk_test_51PrZCB00YaJGfbxsi3aqzEyBDcsbJHfIzQLeq49RIwYjEk1UI0V4VlLZmppsMRUCYci41R7Ccrqzqh0Jh8Ui7IBc00j9Rxg52v'

def get_scheduled_subscription_details(subscription_schedule_id):
    
    try:
        subscription_schedule = stripe.SubscriptionSchedule.retrieve(subscription_schedule_id)
        return subscription_schedule
    except stripe.error.InvalidRequestError:
        print("Invalid subscription schedule ID.")
        return None
    except stripe.error.StripeError as e:
        print("Error: %s" % e.error.message)
        return None

# Example usage:
subscription_schedule_id = 'sub_sched_1PrZEX00YaJGfbxsVdcB6RA5'  # Replace with your actual schedule ID
subscription_schedule_details = get_scheduled_subscription_details(subscription_schedule_id)

if subscription_schedule_details:
    # Extract amount and duration information
    phase = subscription_schedule_details.get("phases", [{}])[0]
    item = phase.get("items", [{}])[0]
    price = item.get("price", {})
    print(price)
    
    amount = price.get("unit_amount")
    currency = price.get("currency")
    duration = phase.get("iterations")
    interval = price.get("recurring", {}).get("interval")

    print("Amount:", amount, currency)
    print("Duration:", duration, interval)
else:
    print("Subscription schedule not found or an error occurred.")