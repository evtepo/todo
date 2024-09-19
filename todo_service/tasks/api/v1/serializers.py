from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Tag, Task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    users = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = ("name", "description", "status", "tags", "users")
