from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from profiles.models import Student, Teacher, Manager

class UserCreateSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    role = serializers.ChoiceField(choices=['student', 'teacher', 'manager'], write_only=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'first_name', 'last_name', 'role', 'token')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': "Пароли не совпадают."})
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return attrs

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        profile_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
        }

        if role == 'student':
            Student.objects.create(user=user, **profile_data)
        elif role == 'teacher':
            Teacher.objects.create(user=user, **profile_data)
        elif role == 'manager':
            Manager.objects.create(user=user, **profile_data)

        return user
    