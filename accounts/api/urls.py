from django.urls import path
from accounts.api.views import UserRegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
]
