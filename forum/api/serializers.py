from rest_framework import serializers
from forum.models import Topic, Subtopic, Post

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
