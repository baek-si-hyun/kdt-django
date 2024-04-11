from django.db import models

from friend.managers import FriendManager
from member.models import Member
from model.models import Period


class Friend(Period):
    FRIEND_STATUS = [
        (-1, '거절'),
        (0, '대기'),
        (1, '승인')
    ]

    sender = models.ForeignKey(Member, related_name='sender_set', null=False, on_delete=models.PROTECT)
    receiver = models.ForeignKey(Member, related_name='receiver_set', null=False, on_delete=models.PROTECT)
    status = models.SmallIntegerField(choices=FRIEND_STATUS, default=0)
    objects = models.Manager()
    friends_objects = FriendManager()

    class Meta:
        db_table = 'tbl_friend'
