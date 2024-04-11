from django.db import models

from member.models import Member
from model.models import Period
from post.models import Post


class Reply(Period):
    PRIVATE_STATUS = [
        (True, '비밀 댓글'),
        (False, '일반 댓글')
    ]

    reply_content = models.TextField(blank=False, null=False)
    member = models.ForeignKey(to=Member, on_delete=models.PROTECT)
    post = models.ForeignKey(to=Post, on_delete=models.PROTECT)
    group_id = models.BigIntegerField(null=True)
    reply_depth = models.BigIntegerField(null=False, default=1)
    reply_private_status = models.BooleanField(null=False, default=False, choices=PRIVATE_STATUS)

    class Meta:
        db_table = 'tbl_reply'
        ordering = ['-id']

    def __str__(self):
        return self.reply_content
