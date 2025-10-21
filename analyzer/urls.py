from django.urls import path

from base.views import ListCreateStringView, RetrieveDeleteView


urlpatterns = [
    path('strings/', ListCreateStringView.as_view(), name='list-create-strings'),
    path('strings/<str:string_value>/', RetrieveDeleteView.as_view(), name='retrieve-delete-string')
]
