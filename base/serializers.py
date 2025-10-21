from rest_framework import serializers
from collections import Counter

from .exceptions import (
    MissingValueException,
    DuplicateEntryException, 
    UnprocessableEntityException
)
from .models import String


class StringSerializer(serializers.ModelSerializer):
    value = serializers.JSONField(
        required=False,
        allow_null=True,
        validators=[])
    properties = serializers.SerializerMethodField()
    
    
    class Meta:
        model = String
        fields = [
            'id',
            'value',
            'properties',
            'created_at'
        ]
        read_only_fields = ['id', 'properties', 'created_at']
    
    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash': obj.id,
            'character_frequency_map': Counter(obj.value)
        }
    
    def _check_duplicity(self, value):
        """
        Ensures the string does not already exist in the db.
        """
        if String.objects.filter(value=value).exists():
            raise DuplicateEntryException()

    def validate_value(self, value):
        """
        Validate the value input.
        """
        if not isinstance(value, str):
            raise UnprocessableEntityException()
        value = value.strip()
        if not value:
            raise MissingValueException()
        self._check_duplicity(value)
        return value

    def validate(self, attrs):
        value = attrs.get('value', None)
        if not value:
            raise MissingValueException()
        return attrs
    
    def create(self, validated_data):
        value = validated_data.get('value')
        return String.objects.create(value=value)
