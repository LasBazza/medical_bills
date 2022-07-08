from django.conf import settings
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .data_handlers import (bills_annotate, evaluate_fraud_weight,
                            format_address)
from .models import Bill, Client, ColumnNames, Organization
from .serializers import BillSerializer, ClientSerializer, ColumnNamesSerializer
from .utils import ClientOrganizationExcelParser

parser = ClientOrganizationExcelParser()


class BaseUploadView(APIView):
    """Base viewset with implementation fetching file from request and saving to storage"""

    def _upload_file(self, request):
        """Save file to storage"""

        file = request.data['file']
        if not file:
            raise ParseError('file is missing')
        file_name = default_storage.save(file.name, file)
        return settings.MEDIA_ROOT / file_name


class DataUploadView(BaseUploadView):
    """Viewset for uploading and parsing data"""

    def post(self, request):
        data_type = request.query_params.get('data_type')
        if data_type not in ['clients', 'organizations', 'bills']:
            return Response(data={'message': 'data_type is wrong or not specified '},
                            status=status.HTTP_400_BAD_REQUEST)

        file_path = self._upload_file(request)

        if data_type == 'clients':
            self._upload_clients(file_path)
        if data_type == 'organizations':
            self._upload_organizations(file_path)
        if data_type == 'bills':
            self._upload_biils(file_path)

        return Response(data={'message': f'{data_type} data is uploaded'})

    def _upload_clients(self, file):
        """Parsing and saving clients data"""
        try:
            client_dicts = parser.parse_excel(file, 'client')
        except KeyError:
            raise ParseError('wrong file or sheet')

        client_list = []
        for client in client_dicts:
            client_list.append(Client(**client))

        try:
            Client.objects.bulk_create(client_list)
        except IntegrityError:
            raise ValidationError('client names are not unique or clients already exist in base')

    def _upload_organizations(self, file):
        """Parsing and saving organizations data"""
        try:
            organization_dicts = parser.parse_excel(file, 'organization')
        except KeyError:
            raise ParseError('wrong file or sheet')

        format_address(organization_dicts)

        # for mapping client FK field in below organization bulk_create
        client_queryset = Client.objects.all()
        client_map = dict((client.name, client) for client in client_queryset)

        organization_list = []
        for organization in organization_dicts:
            # replace client_name to client object
            organization['client_name'] = client_map[organization['client_name']]
            organization_list.append(Organization(**organization))

        try:
            Organization.objects.bulk_create(organization_list)
        except IntegrityError:
            raise ValidationError('client and organization names are not unique together')

    def _upload_biils(self, file):
        """Parsing and saving bills data"""

        # not implemented


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for getting clients list"""

    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for getting bills list"""

    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('client_name', 'organization')


class ColumnNamesViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD ColumnNames"""

    serializer_class = ColumnNamesSerializer
    queryset = ColumnNames.objects.all()
