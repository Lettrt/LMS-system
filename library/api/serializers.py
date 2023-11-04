from rest_framework import serializers
from library.models import Library

class LibrarySerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Library
        fields = ('id', 'title', 'course', 'course_title', 'author', 'year', 'descriptions', 'logo', 'file')
