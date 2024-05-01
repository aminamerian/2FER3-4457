from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db import IntegrityError

from core.models import Advertisement, Comment
from accounts.api.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    advertisement_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "created_by", "created_at", "advertisement_id"]

    def create(self, validated_data):
        try:
            advertisement_id = validated_data.pop("advertisement_id")
            advertisement = Advertisement.objects.get(id=advertisement_id)
            return Comment.objects.create(advertisement=advertisement, **validated_data)
        except Advertisement.DoesNotExist:
            raise ValidationError("Advertisement does not exist.")
        except IntegrityError:
            raise ValidationError("You have already commented on this advertisement.")


class AdvertisementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ["id", "title", "description", "created_by", "created_at", "comments"]
