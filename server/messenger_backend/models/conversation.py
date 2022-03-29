from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import HStoreField

from . import utils
from .user import User


class Conversation(utils.CustomModel):

    users = models.ManyToManyField(User, db_column="userIds", related_name="+")
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)
    usersLastReadAt = HStoreField()
    convoPhotoUrl = models.TextField(default=None, blank=True, null=True)
    convoName = models.TextField(default=None, blank=True, null=True)

    # find conversation given two user Ids
    def find_conversation(user1Id, user2Id):
        # return conversation or None if it doesn't exist
        try:
            return Conversation.objects.get(
                (Q(user1__id=user1Id) | Q(user1__id=user2Id)),
                (Q(user2__id=user1Id) | Q(user2__id=user2Id)),
            )
        except Conversation.DoesNotExist:
            return None
