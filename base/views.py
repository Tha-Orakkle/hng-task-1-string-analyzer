from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from decimal import Decimal
from django.http import Http404, JsonResponse
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

import re

from .exceptions import InvalidQueryParamsException, UnprocessableEntityException
from .filters import StringsFilter
from .models import String
from .serializers import StringSerializer

VOWELS = {
    'first': 'a',
    'second': 'e',
    'third': 'i',
    'fourth': 'o',
    'fifth': 'u'
}


@method_decorator(ratelimit(key='ip', rate='50/h', block=False), name='dispatch')
class ListCreateStringView(APIView):
    filterset_class = StringsFilter
    
    def dispatch(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return JsonResponse({
                'detail': 'Too many requests.'
            }, status=429)
        return super().dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        queryset = String.objects.all().order_by('-created_at')
        filterset = self.filterset_class(self.request.GET, queryset=queryset)

        if filterset.is_valid():
            queryset = filterset.qs
            self.applied_filters = {
                k: int(v) if type(v) in [float, Decimal] else v 
                for k, v in filterset.form.cleaned_data.items()
                if v not in [None, '']
            }
            print(f"APLLIED FILTERS: {self.applied_filters}")
        else:
            raise InvalidQueryParamsException()
            
        return queryset

    def post(self, request):
        serializer = StringSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        qs = self.get_queryset()
        serializers = StringSerializer(qs, many=True)
        return Response({
            'data': serializers.data,
            'count': qs.count(),
            'filters_applied': self.applied_filters    
        }, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='50/h', block=False), name='dispatch')
class RetrieveDeleteView(generics.RetrieveDestroyAPIView):
    lookup_field = 'value'
    lookup_url_kwarg = 'string_value'
    serializer_class = StringSerializer
    queryset = String.objects.all()
    
    def dispatch(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return JsonResponse({
                'detail': 'Too many requests.'
            }, status=429)
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("String does not exist in the system")


@method_decorator(ratelimit(key='ip', rate='50/h', block=False), name='dispatch')
class NaturalLanguageFilterView(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return JsonResponse({
                'detail': 'Too many requests.'
            }, status=429)
        return super().dispatch(request, *args, **kwargs)

    def parse_query(self, query):
        """
        Simple rule-based parser for natural language queries.
        Raise ValueError if unable to parse.
        """
        
        filters = {}
        if 'palindrom' in query:
            filters['is_palindrome'] = True
            
        if 'single word' in query or 'one word' in query:
            filters['word_count'] = 1

        match = re.search(r"longer than (\d+)", query)
        if match:
            filters['min_length'] = int(match.group(1)) + 1
        
        match = re.search(r"shorter than (\d+)", query)
        if match:
            v = int(match.group(1)) - 1
            filters['max_length'] = v if v > 0 else 1 
            
        if "containing the letter" in query or "contains letter" in query:
            match = re.search(r"letter (\w)", query)
            if match:
                filters['contains_character'] = match.group(1).lower()
                
        for k, v in VOWELS.items():
            if f"{k} vowel" in query:
                filters['contains_character'] = v
                break

        if not filters:
            raise InvalidQueryParamsException("Unable to parse natural language query")
        
        if (
            'min_length' in filters and 'max_length' in filters
            and filters['min_length'] > filters['max_length']
        ):
            raise UnprocessableEntityException("Query parsed but resulted in conflicting filters")
        
        return filters
    
    def get(self, request):
        query = request.query_params.get('query', '').strip().lower()
        if not query:
            raise InvalidQueryParamsException("Query parameter 'query' is required")

        parsed_filters = self.parse_query(query)
        queryset = StringsFilter(parsed_filters, String.objects.all()).qs
        serializers = StringSerializer(queryset, many=True)
        return Response({
            'data': serializers.data,
            'count': queryset.count(),
            'interpreted_query': {
                'original': query,
                'parsed_filters': parsed_filters
            }
        })
        