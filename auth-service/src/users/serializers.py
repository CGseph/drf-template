from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["url", "date_joined"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages) from e
        return value

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user passwords (admin only)"""

    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """Validate password strength using Django's built-in validators"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages) from e
        return value

    def validate(self, attrs):
        """Validate that passwords match and user exists"""
        self._validate_user(self.context.get("user_id"))
        return self._validate_password_match(attrs)

    def _validate_password_match(self, attrs):
        """Validate that passwords match"""
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def _validate_user(self, user_id):
        """Validate that the user exists"""
        if not user_id:
            raise serializers.ValidationError("User ID is required.")
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.") from None

    def save(self, **kwargs):
        """Change the user's password"""
        user_id = self.context.get("user_id")
        new_password = self.validated_data["new_password"]

        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        return user
