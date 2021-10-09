import faker
from django.test import TestCase
from posts.serializers import PostSerializer
from posts.tests.factory import PostFactory


class TestPostSerializerCreate(TestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker()
        self.title = self.fake.sentence(nb_words=2)
        self.body = self.fake.paragraph(nb_sentences=3)

    def test_create_full_valid_data(self):
        data = {"title": self.title, "body": self.body}

        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertTrue(serializer.data)

    def test_create_empty_data(self):
        data = {}

        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertIn("title", serializer.errors)
        self.assertIn("body", serializer.errors)


class TestPostSerializerSerializedData(TestCase):
    def setUp(self) -> None:
        self.post = PostFactory.create()

    def test_expected_data(self):
        expected_data = {
            "id": self.post.id,
            "title": self.post.title,
            "body": self.post.body,
        }

        serialized_data = PostSerializer(instance=self.post).data

        self.assertEqual(serialized_data, expected_data)
