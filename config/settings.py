from datetime import timedelta
import os

import environ

# Import the original settings
from .basesettings import *

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    env.read_env(env_file)
else:
    raise Exception("No local environment variable file detected.")


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
