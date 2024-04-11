from django.db.models import Q
from django.test import TestCase

from friend.models import Friend
from member.models import Member


class FriendTest(TestCase):
    data = {
        'member_email': 'zzanggu@naver.com',
        'member_password': 'zzzz',
        'member_name': '짱구',
        'member_age': 5
    }
    Member.objects.create(**data)

    # 친구 요청
    # 로그인한 회원의 정보이다.
    # 친구 신청을 보내는 사람의 정보
    data = {
        'member_email': 'hoon@gmail.com',
        'member_password': 'hhhh'
    }
    sender = Member.objects.get(**data)
    # 친구 요청을 받는 사람의 정보
    data = {
        'member_email': 'zzanggu@naver.com'
    }
    # 받은 정보로 친구요청을 받을 사람을 조회한다.
    receiver = Member.objects.get(member_email=data['member_email'])
    # Friend 테이블에 받는 사람과 보내는 사람의 정보를 저장한다.
    Friend.objects.create(sender=sender, receiver=receiver)

    # 친구 요청 조건(False일 때에만 요청 가능)
    data = {
        'member_email': 'yuri@hanmail.net'
    }
    # 받을 사람의 정보를 조회한다.
    receiver = Member.objects.get(member_email=data['member_email'])
    # Q()객체를 통해 조건을 결합한다.
    # 친구요청을 보낸 사람과 받는 사람의 정보가 있다는 조건
    condition_exist = Q(receiver=receiver, sender=sender)
    # 친구 요청 상태가 '승인'상태이거나 '대기'상태이면 이라는 조건
    condition_status = Q(status=1) | Q(status=0)
    # 두 조건을 and연산자로 연결한다.
    # 친구요청을 보낸 사람과 받는 사람의 정보가 있거나
    # 친구 요청 상태가 '승인'상태이거나 '대기'상태이면
    # 이라는 조건을 만든다.
    condition = condition_exist & condition_status
    # 해당 조건으로 filter를 통해 조회하고, 존재 여부를 exists를 통해 확인해준다.
    condition = Friend.objects.filter(condition).exists()

    # 친구 목록
    data = {
        'member_email': 'zzanggu@naver.com',
        'member_password': 'zzzz'
    }

    # 로그인한 회원
    member = Member.objects.get(**data)
    # 친구 요청을 보냈거나 받은 사용자 목록에 로그인한 회원이 존재하는지 확인한다.
    condition_sender = Q(sender=member)
    condition_receiver = Q(receiver=member)
    # 두 조건을 or로 결합해준다.
    condition = condition_sender | condition_receiver

    ############################################################################
    # 친구 수락이 된 정보 모두 조회
    # 매니저를 통해 만든 새로운 QuerySet이 friends에 담긴다.
    friends = Friend.friends_objects.filter_member(member, status=True)
    # 모든 조건을 만족한 QuerySet들이 friends에 담긴다.
    for friend in friends:
        #friends를 순회하면서 id값이 일치한 Friend 객체들의 status를 -1로 업데이트한다.
        Friend.objects.filter(id=friend.id).update(status=-1)
        print(friend.friend)
    ############################################################################
    # 이전에 만든 조건인 condition과 status가 Ture이 Friend객체들을 가져온다.
    members = Friend.enabled_objects.filter(condition, status=True)
    friends = []
    for friend in members:
        # 로그인한 회원이 아닌 상대 회원 정보 추출
        friends.append(friend.sender if friend.sender.id != member.id else friend.receiver)

    # 내 친구 목록
    print(friends)

    for friend in friends:
        print(friend.__dict__)

    # 친구 삭제: 상태가 1인 친구들
    # 친구 거절: 상태가 0인 친구들
    data = {
        'member_email': 'yuri@hanmail.net',
        'member_password': 'yyyy'
    }

    member = Member.objects.get(**data)

    data = {
        'member_email': 'zzanggu@naver.com',
    }

    friend = Member.objects.get(**data)

    Friend.friends_objects.filter_member(member, friend=friend.id, status=1).update(status=-1)

    # 친구 수락
    data = {
        'member_email': 'zzanggu@naver.com',
        'member_password': 'zzzz'
    }

    receiver = Member.objects.get(**data)

    data = {
        'member_email': 'hoon@gmail.com'
    }

    sender = Member.objects.get(**data)

    Friend.objects.filter(sender=sender, receiver=receiver, status=0).update(status=True)
