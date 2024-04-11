from django.db import models
from django.db.models import Q, F


class FriendManager(models.Manager):
    def filter_member(self, member, **kwargs):
        # 두 조건식을 만든다
        condition_sender = Q(sender=member)
        condition_receiver = Q(receiver=member)
        # 여기서 super()는 Friend 객체이다.
        # get_queryset는 objects와 비슷한 역할을 수행한다.
        # annotate로 receiver와 sender를 기반으로 friend라는 새로운 칼럼을 생성한다.
        # filter에 Q()로 만든 조건식을 전달하고, filter_member에서 받은 member, **kwargs를 **kwargs로 filter에 전달한다.
        friends_receiver = super().get_queryset().annotate(friend=F('receiver')).filter(condition_sender, **kwargs)
        friends_sender = super().get_queryset().annotate(friend=F('sender')).filter(condition_receiver, **kwargs)
        # union을 통해 friends_receiver와 friends_sender QuerySet을 병합해 새로운 QuerySet을 만든다.
        # union은 중복된 결과를 제거하고 하나의 새로운 QuerySet을 만들어준다.
        friends = friends_sender.union(friends_receiver)
        return friends
