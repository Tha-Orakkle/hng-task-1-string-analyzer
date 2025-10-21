from django.http import Http404
from rest_framework import status, generics
from rest_framework.exceptions import NotFound 
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import String
from .serializers import StringSerializer



class ListCreateStringView(APIView):
    def post(self, request):
        serializer = StringSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        qs = String.objects.all()
        serializers = StringSerializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    
class RetrieveDeleteView(generics.RetrieveDestroyAPIView):
    lookup_field = 'value'
    lookup_url_kwarg = 'string_value'
    serializer_class = StringSerializer
    queryset = String.objects.all()
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("String does not exist in the system")
