from rest_framework.test import force_authenticate
from django.urls import reverse
import random
from core.api.views import AdvertisementViewSet, CommentCreateAPIView


def test_advertisement_empty_list_unauthenticated(factory, db):
    url = reverse("core:advertisement-list")
    view = AdvertisementViewSet.as_view({"get": "list"})
    request = factory.get(url)
    response = view(request)
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


def test_advertisement_list_unathenticated(factory, db, advertisements, comments):
    url = reverse("core:advertisement-list")
    view = AdvertisementViewSet.as_view({"get": "list"})
    request = factory.get(url)
    response = view(request)
    assert response.status_code == 200
    assert response.data["count"] == len(advertisements)
    assert len(response.data["results"]) == len(advertisements)
    for advertisement in advertisements:
        assert (
            advertisement.title
            == [
                result["title"]
                for result in response.data["results"]
                if result["id"] == advertisement.id
            ][0]
        )

        assert (
            advertisement.created_by.email
            == [
                result["created_by"]["email"]
                for result in response.data["results"]
                if result["id"] == advertisement.id
            ][0]
        )
        assert advertisement.comments.count() == len(
            [
                result["comments"]
                for result in response.data["results"]
                if result["id"] == advertisement.id
            ][0]
        )


def test_advertisement_create_unauthorized(factory, db):
    url = reverse("core:advertisement-list")
    view = AdvertisementViewSet.as_view({"post": "create"})
    data = {"title": "Test Advertisement"}
    request = factory.post(url, data)
    response = view(request)
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


def test_advertisement_create_authenticated(factory, db, user):
    url = reverse("core:advertisement-list")
    view = AdvertisementViewSet.as_view({"post": "create"})
    data = {"title": "Test Advertisement"}
    request = factory.post(url, data)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 201
    assert response.data["title"] == "Test Advertisement"
    assert response.data["created_by"]["email"] == user.email
    assert AdvertisementViewSet.queryset.count() == len(data)
    assert AdvertisementViewSet.queryset.first().title == data["title"]


def test_advertisement_update_unauthenticated(factory, db, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"put": "update"})
    data = {"title": "Updated Advertisement"}
    request = factory.put(url, data)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


def test_advertisement_update_does_not_exist(factory, db, user):
    url = reverse("core:advertisement-detail", args=[1])
    view = AdvertisementViewSet.as_view({"put": "update"})
    data = {"title": "Updated Advertisement"}
    request = factory.put(url, data)
    force_authenticate(request, user=user)
    response = view(request, pk=1)
    assert response.status_code == 404
    assert response.data["detail"] == "No Advertisement matches the given query."


def test_advertisement_update_unauthorized(factory, db, user2, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"put": "update"})
    data = {"title": "Updated Advertisement"}
    request = factory.put(url, data)
    force_authenticate(request, user=user2)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 403
    assert (
        response.data["detail"] == "You do not have permission to perform this action."
    )


def test_advertisement_update_successfully(factory, db, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"put": "update"})
    data = {"title": "Updated Advertisement"}
    request = factory.put(url, data)
    force_authenticate(request, user=advertisement.created_by)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
    assert response.data["created_by"]["email"] == advertisement.created_by.email
    assert AdvertisementViewSet.queryset.count() == 1
    assert AdvertisementViewSet.queryset.first().title == data["title"]


def test_advertisement_delete_unauthenticated(factory, db, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"delete": "destroy"})
    request = factory.delete(url)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


def test_advertisement_delete_does_not_exist(factory, db, user):
    url = reverse("core:advertisement-detail", args=[1])
    view = AdvertisementViewSet.as_view({"delete": "destroy"})
    request = factory.delete(url)
    force_authenticate(request, user=user)
    response = view(request, pk=1)
    assert response.status_code == 404
    assert response.data["detail"] == "No Advertisement matches the given query."


def test_advertisement_delete_unauthorized(factory, db, user2, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"delete": "destroy"})
    request = factory.delete(url)
    force_authenticate(request, user=user2)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 403
    assert (
        response.data["detail"] == "You do not have permission to perform this action."
    )


def test_advertisement_delete_successfully(factory, db, advertisement):
    url = reverse("core:advertisement-detail", args=[advertisement.id])
    view = AdvertisementViewSet.as_view({"delete": "destroy"})
    request = factory.delete(url)
    force_authenticate(request, user=advertisement.created_by)
    response = view(request, pk=advertisement.id)
    assert response.status_code == 204
    assert AdvertisementViewSet.queryset.count() == 0


def test_comment_create_unauthorized(factory, db):
    url = reverse("core:comment-create")
    view = CommentCreateAPIView.as_view()
    data = {"text": "Test Comment"}
    request = factory.post(url, data)
    response = view(request)
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


def test_comment_create_advertisement_does_not_exits(factory, db, user):
    url = reverse("core:comment-create")
    view = CommentCreateAPIView.as_view()
    data = {"text": "Test Comment", "advertisement_id": 1}
    request = factory.post(url, data)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 400
    assert str(response.data[0]) == "Advertisement does not exist."


def test_comment_create_duplicate_comment(factory, db, comments):
    comment = random.choice(comments)
    url = reverse("core:comment-create")
    view = CommentCreateAPIView.as_view()
    data = {"text": "Test Comment", "advertisement_id": comment.advertisement.id}
    request = factory.post(url, data)
    force_authenticate(request, user=comment.created_by)
    response = view(request)
    assert response.status_code == 400
    assert str(response.data[0]) == "You have already commented on this advertisement."


def test_comment_create_authenticated(factory, db, user, advertisement):
    url = reverse("core:comment-create")
    view = CommentCreateAPIView.as_view()
    data = {"text": "Test Comment", "advertisement_id": advertisement.id}
    request = factory.post(url, data)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 201
    assert response.data["text"] == data["text"]
    assert response.data["created_by"]["email"] == user.email
