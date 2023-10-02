from rest_framework import serializers
from .models import new_payment,Settlement

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = new_payment
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'



