from rest_framework import generics,status
from rest_framework.response import Response
from .models import new_payment,Settlement
from .serializers import PaymentSerializer,SettlementSerializer
from .kafka_utils import get_kafka_producer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
import json

from django.core.cache import cache


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = new_payment.objects.all()
    serializer_class = PaymentSerializer


    @method_decorator(cache_page(60 * 5))  # Cache GET requests for 5 minutes
    def get(self, request, *args, **kwargs):
        try:
            response=super().get(request, *args, **kwargs)
        
            cache_timeout = 60 * 5  # 5 minutes
            cache_expiration_time = timezone.now() + timezone.timedelta(seconds=cache_timeout)
        
        # Set cache-related headers
            response['Cache-Control'] = f'max-age={cache_timeout}'
            response['Expires'] = cache_expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
            return response
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                payment = serializer.save()

                # Notify the new payment-creation event to the topic
                kafka_producer = get_kafka_producer()
                payment_data = {
                    "sender_id": payment.sender_id,
                    "recipient_id": payment.recipient_id,
                    "amount": float(payment.amount),
                }
                kafka_producer.produce('payment_topic', key="payment_capture", value=json.dumps(payment_data))
                kafka_producer.flush()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR),
       
class PaymentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = new_payment.objects.all()
    serializer_class = PaymentSerializer

    @method_decorator(cache_page(60 * 5))  
    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            cache_timeout = 60 * 5  # 5 minutes
            cache_expiration_time = timezone.now() + timezone.timedelta(seconds=cache_timeout)
            response['Cache-Control'] = f'max-age={cache_timeout}'
            response['Expires'] = cache_expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        try:
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Save the payment to the database
                serializer.save()

                # Return a response with the serialized payment data
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return a response with the validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, *args, **kwargs):
        try:
            # Your view logic for DELETE requests here
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except new_payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    

class SettlementListCreateView(generics.ListCreateAPIView):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer

    @method_decorator(cache_page(60 * 15))  # Cache GET requests for 15 minutes
    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            
            # Calculate cache expiration time
            cache_timeout = 60 * 15  # 15 minutes
            cache_expiration_time = timezone.now() + timezone.timedelta(seconds=cache_timeout)
            
            # Set cache-related headers
            response['Cache-Control'] = f'max-age={cache_timeout}'
            response['Expires'] = cache_expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        try:
            # Get the serializer from the request
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Save the settlement to the database
                serializer.save()

                # Send a Kafka event
                kafka_producer = get_kafka_producer()
                settlement_event = {
                    "event_type": "settlement_created",
                    "settlement_id": serializer.data['id'],
                    "settled_amount": serializer.data['settled_amount'],
                }
                kafka_producer.produce('settlements_topic', key=str(serializer.data['id']), value=json.dumps(settlement_event))
                kafka_producer.flush()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return a response with the validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SettlementRetrieveView(generics.RetrieveAPIView):
    queryset = Settlement.objects.using('new').all()
    serializer_class = SettlementSerializer

    @method_decorator(cache_page(60 * 5))  # Cache GET requests for 5 minutes
    def get(self, request, *args, **kwargs):
        try:
            
            response = super().get(request, *args, **kwargs)
            cache_timeout = 60 * 5  # 5 minutes
            cache_expiration_time = timezone.now() + timezone.timedelta(seconds=cache_timeout)
            response['Cache-Control'] = f'max-age={cache_timeout}'
            response['Expires'] = cache_expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            return response
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
         
    def post(self, request, *args, **kwargs):
        try:
            # Get the serializer from the request
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Save the settlement to the database
                serializer.save()
                
                show_data = {
                    "settlement_type": "final_settlement_created",
                    "settlement_id": serializer.data['id'],
                    "payment_id": serializer.data['sender_id'],
                    "settled_amount": serializer.data['settled_amount'],
                }

                
                
                return (show_data)
            else:
                # Return a response with the validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def logout_users(request):
    logout(request)
    messages.success(request,"You have logged out..")
    return redirect('home')        