from rest_framework import serializers
from core.models import Advertisement, Comment
from accounts.api.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class AdvertisementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ["id", "title", "description", "created_by", "created_at", "comments"]
