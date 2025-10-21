
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from rest_framework import serializers


# REQUEST
class StringRequestData(serializers.Serializer):
    value = serializers.CharField()
    
    
# RESPONSE
class PropertySerializer(serializers.Serializer):
    length = serializers.IntegerField(default=17)
    is_palindrome = serializers.BooleanField(default=False)
    unique_characters = serializers.IntegerField(default=12)
    word_count = serializers.IntegerField(default=3)
    sha256_hash = serializers.CharField(default="sha256_hash_value")
    character_frequency_map = serializers.DictField(default={
        's': 2,
        't': 3,
        'r': 2,
    })

    
class StringResponseData(serializers.Serializer):
      id = serializers.CharField(default="sha256_hash_value")
      value = serializers.CharField(default="string to analyze")
      properties = PropertySerializer()
      created_at = serializers.DateTimeField()


class StringListResponseData(serializers.Serializer):
    data = StringResponseData(many=True)
    count = serializers.IntegerField(default=1)
    filters_applied = serializers.DictField(default={
        'contains_character': 'a',
        'word_count': 3,
        'is_palindrome': False
    })


class NaturalLanguageStringResponseData(serializers.Serializer):
    data = StringResponseData(many=True)
    count = serializers.IntegerField(default=1)
    interpreted_query = serializers.DictField(default={
        'original': 'strings longer than 10 characters',
        'parsed_filters': {
            'min_length': 11
        }
    })


# ERRORS
# 400
class InvalidQuerySerializer(serializers.Serializer):
    detail = serializers.CharField(default="Invalid query parameter values or types")


class InvalidQueryNLSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Unable to parse natural language query")


class MissingValueSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Invalid request body or missing 'value' field")


# 404
class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="String does not exist in the system")


# 409
class DuplicateEntrySerializer(serializers.Serializer):
    detail = serializers.CharField(default="String already exists in the system")


# 422 
class UnprocessableEntitySerializer(serializers.Serializer):
    detail = serializers.CharField(default="Invalid data type for 'value' (must be string)")


class UnprocessableEntityNLSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Query parsed but resulted in conflicting filters")


# 429
class TooManyRequestsSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Too many requests.")



# SCHEMAS
create_string_schema = {
    'summary': 'Create a string',
    'description': 'Take a value in request body and analyze the value.',
    'operation_id': 'create_string',
    'tags': ['String'],
    'request': StringRequestData,
    'responses': {
        201: StringResponseData,
        400: MissingValueSerializer,
        409: DuplicateEntrySerializer,
        422: UnprocessableEntitySerializer,
        429: TooManyRequestsSerializer
    }
}

get_strings_list_schema = {
    'summary': 'Get lists of strings',
    'description': 'Returns a list of string data. It takes filtering parameters. \
        Parameters may include `is_palindrome`, `min_length`, `max_length`, `word_count` and `contains_character`',
    'operation_id': 'get_string_list',
    'tags': ['String'],
    'parameters': [
        OpenApiParameter(
            name='is_palindrome',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            required=False
        ),
        OpenApiParameter(
            name='min_length',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False
        ),
        OpenApiParameter(
            name='max_length',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False
        ),
        OpenApiParameter(
            name='word_count',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False
        ),
        OpenApiParameter(
            name='contains_character',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False
        )
    ],
    'request': None,
    'responses': {
        200: StringListResponseData,
        400: InvalidQuerySerializer
    }
}

get_string_list_natural_language = {
    'summary': 'Get list of strings based on natual language query string.',
    'description': 'Returns a list of strings based on the query string that is passed. \
        Parameter string is parsed to retrieve the filtering fields.',
    'operation_id': 'get_string_list_natural_language',
    'tags': ['String'],
    'parameters': [
        OpenApiParameter(
            name='query',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY
        )
    ],
    'request': None,
    'responses': {
        200: NaturalLanguageStringResponseData,
        400: InvalidQueryNLSerializer,
        422: UnprocessableEntityNLSerializer,
        429: TooManyRequestsSerializer
    }
}

get_string_schema = {
    'summary': 'Get a specific string',
    'description': 'Get a string matching the value passed to path.',
    'operation_id': 'get_string',
    'tags': ['String'],
    'request': None,
    'responses': {
        200: StringResponseData,
        404: NotFoundSerializer,
        429: TooManyRequestsSerializer
    }
}

delete_string_schema = {
    'summary': 'Delete a specific string',
    'description': 'Delete a string matching the value passed to path.',
    'operation_id': 'delete_string',
    'tags': ['String'],
    'request': None,
    'responses': {
        204: {},
        404: NotFoundSerializer,
        429: TooManyRequestsSerializer
    }
}
