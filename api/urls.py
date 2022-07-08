from django.urls import include, path

from api import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('columns', views.ColumnNamesViewSet)

urlpatterns = [
    path('upload_data/', views.DataUploadView.as_view()),
    path('clients/', views.ClientViewSet.as_view({'get': 'list'})),
    path('bills/', views.BillViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
