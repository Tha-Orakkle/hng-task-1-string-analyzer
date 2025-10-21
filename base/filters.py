import django_filters

from .exceptions import InvalidQueryParamsException
from .models import String


class StringsFilter(django_filters.FilterSet):
    is_palindrome = django_filters.Filter(method='filter_is_palindrome')
    min_length = django_filters.NumberFilter(
        field_name='length', lookup_expr='gte')
    max_length = django_filters.NumberFilter(
        field_name='length', lookup_expr='lte')
    word_count = django_filters.NumberFilter(
        field_name='word_count', lookup_expr='exact')
    contains_character = django_filters.CharFilter(
        field_name='value', lookup_expr='icontains')

    class Meta:
        model = String
        fields = [
            'is_palindrome',
            'min_length',
            'max_length',
            'word_count',
            'contains_character'
        ]

    def filter_is_palindrome(self, queryset, name, value):
        if value is None:
            return queryset
        val = str(value).lower()
        if val in ('true', '1', 'yes'):
            return queryset.filter(is_palindrome=True)
        elif val in ('false', '0', 'no'):
            return queryset.filter(is_palindrome=False)
        else:
            raise InvalidQueryParamsException()
