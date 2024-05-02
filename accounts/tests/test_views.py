from django.urls import reverse
from accounts.api.views import UserRegisterView


def register_user(factory, data):
    url = reverse("accounts:register")
    view = UserRegisterView.as_view()
    request = factory.post(url, data=data)
    return view(request)


def test_user_registration_password_too_common(factory, db):
    data = {
        "email": "john.doe@gmail.com",
        "name": "John Doe",
        "password": "password",
    }
    response = register_user(factory, data)
    assert response.status_code == 400
    assert response.data["password"][0].code == "password_too_common"


def test_user_registration_password_too_short(factory, db):
    data = {
        "email": "john.doe@gmail.com",
        "name": "John Doe",
        "password": "pass",
    }
    response = register_user(factory, data)
    assert response.status_code == 400
    assert response.data["password"][0].code == "password_too_short"


def test_user_registration_duplicate_email(factory, user):
    data = {
        "email": user.email,
        "name": "John Doe",
        "password": "P32#Dsc&GD",
    }
    response = register_user(factory, data)
    assert response.status_code == 400
    assert response.data["email"][0].code == "unique"


def test_user_registration_missing_email(factory, db):
    data = {
        "name": "John Doe",
        "password": "P32#Dsc&GD",
    }
    response = register_user(factory, data)
    assert response.status_code == 400
    assert response.data["email"][0].code == "required"


def test_user_registration_missing_password(factory, db):
    data = {
        "email": "john.doe@gmail.com",
        "name": "John Doe",
    }
    response = register_user(factory, data)
    assert response.status_code == 400
    assert response.data["password"][0].code == "required"


def test_user_registration_successfully(factory, db):
    data = {
        "email": "john.doe@gmail.com",
        "password": "P32#Dsc&GD",
    }
    response = register_user(factory, data)
    assert response.status_code == 201
    assert response.data["email"] == data["email"]
