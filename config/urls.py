from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_data/', views.DataUploadView.as_view()),
    path('clients/', views.ClientViewSet.as_view({'get': 'list'})),
    path('bills/', views.BillViewSet.as_view({'get': 'list'}))
]
