from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["name", "email", "password"]

        extra_kwargs = {
            "password": {"write_only": True, "validators": [validate_password]},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
