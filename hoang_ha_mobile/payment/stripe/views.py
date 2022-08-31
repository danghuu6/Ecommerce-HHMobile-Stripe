from ast import Or
from rest_framework import generics, permissions, response, status, viewsets
from rest_framework_simplejwt import authentication
from rest_framework.decorators import action

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from hoang_ha_mobile.base import stripe_base
from orders.serializers import UpdateChargeStatusSerializer
from orders.models import Order


class ListCreateSetupIntentViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post', 'get'], detail=False, url_path="payment-method")
    def setup_intent(self, request):
        if request.method == "POST":
            try:

                setup_intent = stripe_base
                return response.Response({'SetupIntent_id': setup_intent['id'],
                                        'client_secret': setup_intent['client_secret'],
                                        'customer': setup_intent['customer']},
                                        status=status.HTTP_201_CREATED)
            except Exception as e:
                return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "GET":
            try:
                setup_intent = stripe_base.setup_intent_list(self.request.user.email)

                return response.Response({'payment_method': setup_intent['data'][0]['payment_method'],
                                        'client_secret': setup_intent['data'][0]['client_secret']},
                                        status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True, url_path="checkout")
    def checkout(self, request, pk):
        try:
            checkout_intent = stripe_base.checkout_intent(pk)

            return response.Response({'client_secret': checkout_intent['client_secret']},
                                    status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path="refund")
    def refund(self, request, pk):
        try:
            refund = stripe_base.refund(pk)

            return response.Response({'status': refund['status']},
                                    status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def webhook(request):
    payload = request.body
    signature = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    event = stripe_base.webhook(payload, signature)

    if event.type == 'charge.succeeded':
        charge = event.data.object
        order = Order.objects.get(id=charge.metadata.order_id)
        serializer = UpdateChargeStatusSerializer(order, data={"charge_status": "succeeded"})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    if event.type == 'charge.failed':
        charge = event.data.object
        order = Order.objects.get(id=charge.metadata.order_id)
        serializer = UpdateChargeStatusSerializer(order, data={"charge_status": "failed"})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    return HttpResponse(status=200)