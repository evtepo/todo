from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from tasks.models import Tag, Task
from tasks.api.v1.serializers import TagCreateSerializer, TagSerializer, TaskCreateSerializer, TaskSerializer


class APIViewMixin(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    class Meta:
        abstract = True


class TagListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TagCreateSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailAPIView(APIViewMixin):
    def get_object(self, tag_id):
        return get_object_or_404(Tag, id=tag_id)

    def get(self, request, tag_id, *args, **kwargs):
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, tag_id, *args, **kwargs):
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tag_id, *args, **kwargs):
        tag = self.get_object(tag_id)
        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(users=request.user).prefetch_related("tags", "users")
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not data.get("users"):
            data["users"] = [request.user.id]

        serializer = TaskCreateSerializer(data=data)
        if serializer.is_valid():
            task = serializer.save()

            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIViewMixin):
    def get_object(self, task_id):
        return get_object_or_404(Task, id=task_id)

    def get(self, request, task_id, *args, **kwargs):
        task = self.get_object(task_id)
        if not request.user in task.users.all():
            raise PermissionDenied("You do not have permission to delete this task.")

        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_id, *args, **kwargs):
        task = self.get_object(task_id)
        if not request.user in task.users.all():
            raise PermissionDenied("You do not have permission to delete this task.")

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, *args, **kwargs):
        task = self.get_object(task_id)
        if not request.user in task.users.all():
            raise PermissionDenied("You do not have permission to delete this task.")

        task.delete()

        return Response({"Msg": "Successfully deleted."}, status=status.HTTP_200_OK)
