import factory
from authorization.tests.factory import UserFactory
from posts.models import Like, Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    owner = factory.SubFactory(UserFactory)

    title = factory.Faker("sentence", nb_words=3)
    body = factory.Faker("paragraph", nb_sentences=5)


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like

    liked_by = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
