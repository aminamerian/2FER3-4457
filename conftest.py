import pytest
from rest_framework.test import APIRequestFactory
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model


@pytest.fixture(scope="module")
def factory():
    return APIRequestFactory()


@pytest.fixture()
def user(db):
    return mixer.blend(get_user_model())


@pytest.fixture()
def user2(db):
    return mixer.blend(get_user_model())


@pytest.fixture()
def users(db):
    return mixer.cycle(10).blend(get_user_model())
