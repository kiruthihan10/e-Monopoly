from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'password')
        extra_kwargs = {'password': {'write_only': True}}

