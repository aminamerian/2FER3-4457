from django.urls import path, include
from rest_framework.routers import SimpleRouter

from core.api.views import AdvertisementViewSet, CommentCreateAPIView

app_name = "core"

router = SimpleRouter()
router.register("advertisement", AdvertisementViewSet, basename="advertisement")

urlpatterns = [
    path("", include(router.urls)),
    path("comment/", CommentCreateAPIView.as_view(), name="comment-create"),
]
