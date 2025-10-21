from django.urls import path

from base.views import ListCreateStringView, NaturalLanguageFilterView, RetrieveDeleteView


urlpatterns = [
    path('strings/', ListCreateStringView.as_view(), name='list-create-strings'),
    path('strings/filter-by-natural-language/', NaturalLanguageFilterView.as_view(), name='natural-language-filter-strings-search'),
    path('strings/<str:string_value>/', RetrieveDeleteView.as_view(), name='retrieve-delete-string')
]
