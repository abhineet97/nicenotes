from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Note

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )

    edit_access_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    view_access_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        no_access = kwargs.pop("no_access", False)
        super(NoteSerializer, self).__init__(*args, **kwargs)

        if no_access:
            self.fields.pop("edit_access_to")
            self.fields.pop("view_access_to")

    class Meta:
        model = Note
        fields = [
            "id",
            "content",
            "createdon",
            "modifiedon",
            "owner",
            "edit_access_to",
            "view_access_to",
        ]
