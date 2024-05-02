import pytest
from mixer.backend.django import mixer
import random


@pytest.fixture()
def advertisement(db, user):
    return mixer.blend("core.Advertisement", created_by=user)


@pytest.fixture()
def advertisements(db, users):
    return mixer.cycle(50).blend("core.Advertisement", created_by=mixer.SELECT)


@pytest.fixture()
def comments(db, users, advertisements):
    """
    As advertisement and user should be unique in a comment, we need to create
    comments for each advertisement with unique users.
    """
    comments_list = []
    for advertisement in advertisements:
        for user in random.sample(users, random.randint(1, len(users))):
            text = f"Comment {advertisement.pk}-{user.pk}"
            comment = mixer.blend(
                "core.Comment", advertisement=advertisement, created_by=user, text=text
            )
            comments_list.append(comment)
    return comments_list
