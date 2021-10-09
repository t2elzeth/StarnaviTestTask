from rest_framework import serializers

from .models import Like, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body"]

    def create(self, validated_data):
        validated_data.update({"owner": self.context["request"].user})
        return super().create(validated_data)


class PostAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["liked_by", "post", "date_created"]
