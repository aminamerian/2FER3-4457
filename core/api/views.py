from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import Advertisement
from core.api.serializers import AdvertisementSerializer, CommentSerializer
from core.api.permissions import AdvertisementPermission


class AdvertisementViewSet(viewsets.ModelViewSet):
    permission_classes = [AdvertisementPermission]
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return self.queryset.select_related("created_by").prefetch_related(
                "comments"
            )
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
