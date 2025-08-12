from rest_framework import serializers
from .models import Book, Author
from datetime import datetime
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    class meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        
    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class meta:
        model = Author
        fields = '__all__'