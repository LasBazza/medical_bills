from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .utils import ExcelParser

parser = ExcelParser()


class BillsUploadView(APIView):

    def post(self, request):
        file = request.data['file']

        file_name = default_storage.save(file.name, file)
        file_path = settings.MEDIA_ROOT / file_name

        sheets = parser.parse_excel(file_path, 'organization')

        return Response(data={'message': sheets})
