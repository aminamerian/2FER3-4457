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