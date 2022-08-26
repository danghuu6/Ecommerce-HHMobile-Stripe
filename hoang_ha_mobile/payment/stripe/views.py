from rest_framework import generics, permissions, response, status, viewsets
from rest_framework_simplejwt import authentication
from rest_framework.decorators import action

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key=settings.STRIPE_SECRET_KEY


class ListCreateSetupIntentViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post', 'get'], detail=False, url_path="payment-method")
    def setup_intent(self, request):
        if request.method == "POST":
            try:
                cus = stripe.Customer.search(
                    query="email~'%s'" % str(self.request.user.email),
                )
                if len(cus['data']) <= 0:
                    cus = stripe.Customer.create(
                        email = self.request.user.email
                    )
                elif len(cus['data']) >= 1:
                    cus = cus['data'][0]

                setup_intent = stripe.SetupIntent.create(
                    customer = cus['id'],
                    payment_method_types = ['card']
                )

                return response.Response({'SetupIntent_id': setup_intent['id'],
                                        'client_secret': setup_intent['client_secret'],
                                        'customer': setup_intent['customer']},
                                        status=status.HTTP_201_CREATED)
            except Exception as e:
                return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "GET":
            try:
                cus = stripe.Customer.search(
                    query="email~'%s'" % str(self.request.user.email),
                )

                setup_intent = stripe.SetupIntent.list(
                    customer = cus['data'][0]['id']
                )

                return response.Response({'SetupIntent_id': setup_intent['data'][0]['id'],
                                        'client_secret': setup_intent['data'][0]['client_secret']},
                                        status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True, url_path="checkout")
    def checkout(self, request, pk):
        try:
            search_pi = stripe.PaymentIntent.search(
                query = "metadata['order_id']: '%s'" % pk,
            )
            
            search_pm = stripe.Customer.list_payment_methods(
                search_pi['data'][0]['customer'],
                type = "card",
            )
            
            checkout_intent = stripe.PaymentIntent.confirm(
                search_pi['data'][0]['id'],
                payment_method = search_pm['data'][0]['id'],
            )

            return response.Response({'client_secret': checkout_intent['client_secret']},
                                    status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path="refund")
    def refund(self, request, pk):
        try:
            search_pi = stripe.PaymentIntent.search(
                query = "metadata['order_id']: '%s'" % pk,
            )

            refund = stripe.Refund.create(
                payment_intent = search_pi['data'][0]['id'],
            )

            return response.Response({'status': refund['status']},
                                    status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def webhook(request):
    payload = request.body
    signature = request.META['HTTP_STRIPE_SIGNATURE']
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

    if event.type == 'charge.created':
        charge = event.data.object
        print(charge)
        
    return HttpResponse(status=200)