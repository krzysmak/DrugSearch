from rest_framework import serializers
from DrugSearch.models import Lek, SzczegolyRefundacji


class SzczegolyRefundacjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SzczegolyRefundacji
        fields = "__all__"


class LekSerializer(serializers.ModelSerializer):
    refundacje = SzczegolyRefundacjiSerializer(many='True')
    class Meta:
        model = Lek
        fields = "__all__"


