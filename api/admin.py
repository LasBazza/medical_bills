from django.contrib import admin

from .models import Bill, Client, ColumnNames, Organization


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'client_name', 'address', 'fraud_weight')


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'number',
        'sum', 'date',
        'service',
        'client_name',
        'organization',
        'service_class',
        'service_name',
        'fraud_score'
    )


@admin.register(ColumnNames)
class ColumNamesAdmin(admin.ModelAdmin):

    list_display = (
        'client',
        'client_name_column',
        'organization_column',
        'number_column',
        'sum_column',
        'date_column',
        'service_column',
    )
