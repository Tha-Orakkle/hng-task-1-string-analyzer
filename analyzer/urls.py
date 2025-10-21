from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from base.views import ListCreateStringView, NaturalLanguageFilterView, RetrieveDeleteView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='spectacular-doc'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='spectacular-doc'),
    path('strings/', ListCreateStringView.as_view(), name='list-create-strings'),
    path('strings/filter-by-natural-language/', NaturalLanguageFilterView.as_view(), name='natural-language-filter-strings-search'),
    path('strings/<str:string_value>/', RetrieveDeleteView.as_view(), name='retrieve-delete-string')
]
