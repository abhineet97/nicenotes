from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    createdon = models.DateTimeField(auto_now_add=True)
    modifiedon = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    edit_access_to = models.ManyToManyField(User, related_name='edit_access_to', blank=True)
    view_access_to = models.ManyToManyField(User, related_name='view_access_to', blank=True)

    def __str__(self):
        return "A note by {}, created on {} and last modified on {}".format(
                self.owner, self.createdon, self.modifiedon
                )
