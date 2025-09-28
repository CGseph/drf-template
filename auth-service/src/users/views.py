from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .serializers import PasswordChangeSerializer, UserSerializer

User = get_user_model()


class UserViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    # Cache settings
    list_cache_timeout = 15 * 60  # 15 minutes
    object_cache_timeout = 15 * 60  # 15 minutes

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
        url_path="change-password",
        url_name="change_password",
        serializer_class=PasswordChangeSerializer,
    )
    def set_password(self, request, pk=None, **kwargs):
        """
        Change a user's password. Only admin users can perform this action.
        """

        serializer = PasswordChangeSerializer(
            data=request.data, context={"user_id": pk, "request": request}
        )

        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {
                        "message": f"Password successfully \
                                    changed for user {user.username}",
                        "user_id": user.id,
                        "username": user.username,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to change password", "detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
