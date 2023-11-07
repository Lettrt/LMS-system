from django.db.models import Avg
from rest_framework import serializers
from courses.models import Course, Comment, Rating, CourseApplication 


class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(course=obj)
        if ratings.exists():
            average = ratings.aggregate(Avg('rating')).get('rating__avg')
            return round(average, 1)
        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CourseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseApplication
        fields = '__all__'



    

    