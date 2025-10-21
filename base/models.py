from django.db import models

import hashlib


class String(models.Model):
    id = models.CharField(primary_key=True, max_length=64, editable=False)
    value = models.CharField(max_length=64, null=False, unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField(default=False)
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        String representation.
        """
        return (
            f"<{self.value}> : {self.id} \n"
            f"  hash: {self.id} \n"
            f"  is_palindrome: {self.is_palindrome} \n"
            f"  length: {self.length} \n"
            f"  unique_characters: {self.unique_characters} \n"
            f"  word_count: {self.word_count}"
        )

    def _set_length(self):
        """
        Get string length.
        """
        self.length = len(self.value)
    
    def _set_hash(self):
        """
        Get string hash using SHA256 algo.
        """
        self.id = hashlib.sha256(self.value.encode()).hexdigest()
        
    def _check_palindrome(self):
        s = self.value
        return s == s[::-1]
        
    def _set_unique_chars(self):
        """
        Set the number of unique chars.
        """
        chars = [ch for ch in self.value if ch.isalnum()]
        self.unique_characters = len(set(chars))

    def _set_word_count(self):
        """
        Set the word count in the string.
        """
        self.word_count = len(self.value.split(' '))

    def _set_string_details(self):
        self._set_hash()
        self._set_length()
        self.is_palindrome = self._check_palindrome()
        self._set_unique_chars()
        self._set_word_count()
        
    def save(self, *args, **kwargs):
        if not self.value:
            raise ValueError("<String> Value cannot be null.")
        self._set_string_details()
        super().save(*args, **kwargs)
        return self
