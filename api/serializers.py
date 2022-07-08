from django.db.models import Sum
from rest_framework import serializers

from .models import Bill, Client, ColumnNames


class ClientSerializer(serializers.ModelSerializer):
    organizations_count = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('name', 'organizations_count', 'total_income')

    def get_organizations_count(self, obj):
        return obj.organizations.count()

    def get_total_income(self, obj):
        return obj.bills.aggregate(Sum('sum'))['sum__sum']


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'


class ColumnNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColumnNames
        fields = '__all__'
