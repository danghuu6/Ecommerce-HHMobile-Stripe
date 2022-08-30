import stripe
from django.conf import settings
from django.http import HttpResponse

stripe.api_key=settings.STRIPE_SECRET_KEY

def search_and_create_customer(email):
    customer = stripe.Customer.search(
        query="email~'%s'" % str(email),
    )
    if len(customer['data']) <= 0:
        customer = stripe.Customer.create(
            email = email
        )
    return customer['data'][0]

def payment_intent_create(amount, currency, order_id, **customer):
    
    if len(customer) == 0:
        intent = stripe.PaymentIntent.create(
            amount = int(amount),
            currency = currency,
            payment_method_types=["card"],
            metadata = {
                'order_id': order_id
            },
            confirmation_method = 'manual'
        )
    else:
        intent = stripe.PaymentIntent.create(
            customer = customer['customer'],
            amount = int(amount),
            currency = currency,
            payment_method_types=["card"],
            metadata = {
                'order_id': order_id
            },
            confirmation_method = 'manual'
        )

    return intent

def payment_intent_confirm(payment_method_id, payment_intent_id):
    confirm = stripe.PaymentIntent.confirm(
        payment_intent_id,
        payment_method = payment_method_id,
    )

    return confirm


def setup_intent_create(email):
    customer = search_and_create_customer(email)

    setup_intent = stripe.SetupIntent.create(
        customer = customer['id'],
        payment_method_types = ['card']
    )

    return setup_intent

# List Customer's setupintent
def setup_intent_list(email):
    cus = stripe.Customer.search(
        query="email~'%s'" % str(email),
    )

    setup_intent = stripe.SetupIntent.list(
        customer = cus['data'][0]['id']
    )

    return setup_intent

def checkout_intent(order_id):
    search_pi = stripe.PaymentIntent.search(
        query = "metadata['order_id']: '%s'" % order_id,
    )
            
    search_pm = stripe.Customer.list_payment_methods(
        search_pi['data'][0]['customer'],
        type = "card",
    )
    
    checkout_intent = stripe.PaymentIntent.confirm(
        search_pi['data'][0]['id'],
        payment_method = search_pm['data'][0]['id'],
    )

    return checkout_intent

def refund(order_id):
    search_pi = stripe.PaymentIntent.search(
        query = "metadata['order_id']: '%s'" % order_id,
    )

    refund = stripe.Refund.create(
        payment_intent = search_pi['data'][0]['id'],
    )

    return refund

def webhook(payload, signature):
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, 
            sig_header=signature, 
            secret=settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    return event