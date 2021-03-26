from rest_framework import permissions, viewsets

from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """
    List the user's notes or create a new note.
    """

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs1 = user.notes.all()
        qs2 = user.edit_access_to.all()
        qs3 = user.view_access_to.all()

        has_pk = bool(self.kwargs.get("pk", None) is not None)
        if self.request.method == "GET" and has_pk:
            return qs1 | qs3
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            return qs1 | qs2
        else:
            return qs1
