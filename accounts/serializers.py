from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from notes.serializers import NoteSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=10,
    )
    full_name = serializers.CharField(max_length=40)
    password = serializers.CharField(min_length=6, write_only=True)
    edit_access_to = NoteSerializer(many=True, no_access=True)
    view_access_to = NoteSerializer(many=True, no_access=True)

    def __init__(self, *args, **kwargs):
        show_access_only = kwargs.pop("show_access_only", False)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if not show_access_only:
            self.fields.pop("edit_access_to")
            self.fields.pop("view_access_to")
        else:
            self.fields.pop("id")
            self.fields.pop(User.USERNAME_FIELD)
            self.fields.pop("full_name")

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["mobile"],
            validated_data["password"],
            full_name=validated_data["full_name"],
        )
        return user

    class Meta:
        model = User
        fields = [
            "id",
            User.USERNAME_FIELD,
            "full_name",
            "password",
            "edit_access_to",
            "view_access_to",
        ]
