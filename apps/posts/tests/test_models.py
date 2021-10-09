from django.test import TestCase
from django.utils import timezone
from posts.tests.factory import LikeFactory, PostFactory


class TestPostModel(TestCase):
    def setUp(self) -> None:
        self.post = PostFactory.create()

    def test_defaults(self):
        self.assertGreater(timezone.now(), self.post.datetime_created)


class TestLikeModel(TestCase):
    def setUp(self) -> None:
        self.like = LikeFactory.create()

    def test_defaults(self):
        self.assertGreater(timezone.now(), self.like.date_created)
