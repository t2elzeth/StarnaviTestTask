from datetime import datetime, timedelta

from authorization.models import User
from authorization.tests.factory import UserFactory
from django.conf import settings
from django.utils import timezone
from posts.models import Like, Post
from posts.tests.factory import LikeFactory, PostFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests.mixins import SetAuthCredentialsMixin


class TestPostCreate(SetAuthCredentialsMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.token = self.user.login()
        self.url = reverse("post_create")
        self.valid_payload = {"title": "My test title", "body": "My test Post body"}

    def test_create_with_valid_payload(self):
        """Test post creation with valid payload"""
        self.set_credentials(self.token)

        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_empty_payload(self):
        """Test post creation with empty payload"""
        self.set_credentials(self.token)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_auth_header_provided(self):
        """Test post creation without authtoken"""
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestLike(SetAuthCredentialsMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.superuser = User.objects.create_superuser(
            email="superuser@gmail.com", password="admin12345"
        )
        self.token = self.user.login()
        self.post = PostFactory.create(owner=self.superuser)

    def _get_url(self, pk=1):
        return reverse("post-rate-like", kwargs={"pk": pk})

    def test_successfull_like_post(self):
        """Test successfull like post case"""
        self.set_credentials(self.token)

        response = self.client.post(self._get_url(self.post.id))

        post_likes = Post.objects.get(id=self.post.id).likes.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_likes.count(), 1)

    def test_like_post_without_auth_header(self):
        """Test like post without providing authtoken case"""
        response = self.client.post(self._get_url())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_not_existing_post(self):
        """Test like post that doesn't exist case"""
        self.set_credentials(self.token)

        response = self.client.post(self._get_url(2000))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPostDislike(SetAuthCredentialsMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.superuser = User.objects.create_superuser(
            email="superuser@gmail.com", password="admin12345"
        )
        self.token = self.user.login()
        self.supertoken = self.superuser.login()
        self.post = PostFactory.create()
        self.post_like_kwargs = {"liked_by": self.superuser, "post": self.post}
        self.post_like = LikeFactory.create(**self.post_like_kwargs)

    def _get_url(self, pk=1):
        return reverse("post-rate-unlike", kwargs={"pk": pk})

    def test_successfull_unlike_post(self):
        """Test successfull unlike post case"""
        self.set_credentials(self.supertoken)

        response = self.client.post(self._get_url(self.post.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(**self.post_like_kwargs).exists())

    def test_unlike_post_without_auth_header(self):
        """Test unlike post without providing authtoken"""

        response = self.client.post(self._get_url())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPostGetAnalytics(SetAuthCredentialsMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.superuser = User.objects.create_superuser(
            email="superuser@gmail.com", password="admin12345"
        )
        self.token = self.user.login()
        self.post = PostFactory.create(owner=self.superuser)
        self.url = reverse("post_analytics", kwargs={"pk": self.post.id})
        self.initial_time = timezone.now()

        common_like_data = {"liked_by": self.superuser, "post": self.post}

        self.likes = [
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=7),
            ),
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=6),
            ),
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=6),
            ),
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=6),
            ),
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=10),
            ),
            LikeFactory.create(
                **common_like_data,
                date_created=self.initial_time - timedelta(days=20),
            ),
        ]

    def _get_date_query_param(self, days, date_format=settings.DATE_FORMAT):
        date = self.initial_time - timedelta(days=days)
        return datetime.strftime(date, date_format)

    def _get_url(self, date_from, date_to, url=None):
        url_template = "{url}?date_from={date_from}&date_to={date_to}"

        return url_template.format(
            url=url or self.url, date_from=date_from, date_to=date_to
        )

    def test_successfull_retrieving_analytics(self):
        """Test successfull retrieving analytics"""
        # First part of testing
        url = self._get_url(
            date_from=self._get_date_query_param(days=8),
            date_to=self._get_date_query_param(days=5),
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["likes_overall"], 4)
        self.assertEqual(response.data["by_day"][self._get_date_query_param(6)], 3)
        self.assertEqual(response.data["by_day"][self._get_date_query_param(7)], 1)

        # Second part of testing
        url = self._get_url(
            date_from=self._get_date_query_param(days=11),
            date_to=self._get_date_query_param(days=9),
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["likes_overall"], 1)
        self.assertEqual(response.data["by_day"][self._get_date_query_param(10)], 1)

    def test_retrieving_analytics_without_query_params(self):
        """Test retrieving analytics without query params"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieving_analytics_on_not_existing_post(self):
        """Test retrieving analytics on post that does not exist"""
        url = self._get_url(
            url=reverse("post_analytics", kwargs={"pk": 200}),
            date_from=self._get_date_query_param(days=10),
            date_to=self._get_date_query_param(days=5),
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
