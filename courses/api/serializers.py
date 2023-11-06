from rest_framework import serializers
from courses.models import Course, Comment, Rating, CourseApplication 




class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


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



    

    