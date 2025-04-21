from django.urls import path, include
from Ocr_service import views
 
urlpatterns = [ 
    # path('vendors', views.vendor_list, name='vednorlist'),
    # path('vendors/<int:pk>/', views.vendor_detail, name='vednordetail'),
    path('DocFormat', views.DocFormat_list, name='vednorlist'),
    path('DocFormat/<int:pk>/', views.DocFormat_detail),
    path('OCR', views.OCR),


]