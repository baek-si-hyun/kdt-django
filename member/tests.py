import random

from django.db import connection
from django.db.models import Q, Count, Model, F, ProtectedError, Max, Min
from django.test import TestCase

from member.models import Member
from post.models import Post
from member.models import Member


class MemberTest(TestCase):
    # 클래스 내부에 코드를 작성하면 연결한 테이블에 저장되고,
    # 메소드 내에서 코드를 작성하면 임시 테이블에 저장된 뒤 사라진다.
    # create
    # Member는 Member클래스의 객체이다.
    # objects는 쿼리문을 작성할수 있게 도와주는 메니저이다.
    # 매니저는 장고에서 데이터베이스와 상호작용을 할수 있게 도와주는 역할을 한다.
    # 쿼리문을 사용할수 있게 도와주는 objects 안에는 create 메서드가 존재한다
    # craete 메서드는 데이터베이스에 insert할수 있게 해준다
    member = Member.objects.create(
        member_email='test1@gmail.com',
        member_password='1234',
        member_age=20,
        member_name='테스트1',
    )

    print(member.__dict__)

    # 테스트 코드를 메서드 안에서 작성하면 임시 테이블에 저장되었다가 사라진다.
    def test_member_creation(self):
        member = Member.objects.create(
            member_email='test1@gmail.com',
            member_password='1234',
            member_age=20,
            member_name='테스트1',
        )

        print(member.__dict__)

    # 회원 1명 추가
    Member.objects.create()

    # 회원 2명 추가
    for i in range(2):
        Member.objects.create()

    # save
    datas = {
        'member_email': 'test2@gmail.com',
        'member_password': '1234',
        'member_age': 20,
        'member_name': '테스트2',
    }
    # Member 생성자에게 데이터를 전달한다.
    # 생성자는 키-값 형태의 인자를 받는다
    # datas가 딕셔너리 구조로 되어있기 때문에 kwrgs로 키-값 형태로 바꿔준다.
    member = Member(**datas)
    # save()는 객체의 변경사항을 데이터베이스에 저장한다.
    # 변경된 객체와 같은 데이터가 데이터베이스에 존재하면 수정하고
    # 없으면 생성한다.
    member.save()

    # 회원 1명 추가
    datas = {}
    member = Member(**datas)
    member.save()

    # 회원 2명 추가
    datas = [
        {},
        {},
    ]

    for data in datas:
        member = Member(**data)
        member.save()

    # bulk_create
    # bulk_create는 한번에 여러 객체를 데이터베이스에 생성할때 사용한다.
    # 생성할때는 id가 자동으로 추가 되지만
    # bulk_create를 사용하여 객체를 생성할때는 id를 가져오지 않는다.
    # 그래서 members의 객체들은 id가 출력되지 않는다.
    members = Member.objects.bulk_create([
        Member(
            member_email='test3@gmail.com',
            member_password='1234',
            member_age=10,
            member_name='테스트3'),
        Member(
            member_email='test4@gmail.com',
            member_password='1234',
            member_age=30,
            member_name='테스트4'),
        Member(
            member_email='test5@gmail.com',
            member_password='1234',
            member_age=40,
            member_name='테스트5')
    ])

    for member in members:
        print(member.__dict__)

    # 회원 2명 추가
    datas = [
        {},
        {}
    ]

    members = []

    for data in datas:
        members.append(Member(**data))

    Member.objects.bulk_create(members)

    # get_or_create
    # 객체를 가져오는데 가져오고자 하는 객체가 데이터베이스에 없으면
    # default에 전달한 데이터로 데이터베이스에 저장하고 해당 객테를 가져온다.
    datas = {
        'member_password': '1234',
        'member_age': 50,
        'member_name': '테스트6',
    }
    # 가져오고자 하는 데이터가 있으면 member에 없으면 생성하고 created에 담긴다.
    member, created = Member.objects.get_or_create(member_email='test6@gmail.com', defaults=datas)
    print(member.__dict__, created)

    # member_email이 'admin1@gmail.com'인 회원을 조회한다.
    # 만약 없으면 새로운 정보를 전달하여 회원을 추가한다.
    datas = {}

    member, isCreated = Member.objects.get_or_create(member_email='admin1@gmail.com', defaults=datas)

    # get
    # get은 무조건 하나의 객체만 가져올수 있다.
    # 2개 이상일 경우 에러가 발생한다.
    member = Member.objects.get(id=3)
    print(member.__dict__)

    # all
    # member 테이블의 모든 객체를 가져온다.
    # model의 models에 추가한 매니저중 하나인 enabled_objects를 사용하면
    # filter를 사용해 조건을 추가하지 않아도 알아서 status가 True인 데이터만 가져온다.
    members = Member.objects.all()
    members = Member.enabled_objects.all()
    for member in members:
        print(member.__dict__)

    # filter
    # filter는 sql문의 where절과 비슷한 역할을 한다.
    member_queryset = Member.enabled_objects.filter(member_name='테스트6')
    # exists는 데이터를 가져오는 메서드가 아니라
    # member_queryset이 데이터베이스에 존재하는지 확인하고
    # boolean 값을 리턴하는 메서드이다.
    print(member_queryset.exists())
    # 장고의 QuerySet은 파이썬의 list와 비슷하게 작동한다
    # 그래서 QuerySet에서도 여러개의 객체중에 인덱스 번호를 입력해
    # 해당 QuerySet중에 원하는 순서의 데이터를 출력할수 있다.
    # QuerySet은 여러개의 객체를 한번에 가지고 있는 하나의 자료형이다.
    print(member_queryset[0].__dict__)

    # 로그인된 회원의 상세페이지에서 내가 등록한 맵주소 찾기
    data = {
        'member_email': 'test4@gmail.com',
        'member_password': '1234'
    }

    member = Member.enabled_objects.get(**data)
    print(member.member_name)

    # 게시글과 댓글을 모두 작성한 회원을 찾으세요
    # 화면 예시
    # 회원 정보, 게시글 개수, 댓글 개수
    # 매니저를 사용하기 애매하거나 복잡한 경우 직접 쿼리문을 작성하여 데이터를 출력하는 방식이다.
    query = """
        select m_p.id, m_p.member_email, m_p.member_name, m_p.post_count, count(r.id) reply_count
        from
        (
            select m.id, m.member_email, m.member_name, count(p.id) post_count
            from tbl_member m left outer join tbl_post p
            on m.id = p.member_id
            group by m.id, m.member_email, m.member_name
        ) m_p left outer join tbl_reply r
        on m_p.id = r.member_id
        group by m_p.id, m_p.member_email, m_p.member_name, m_p.post_count
    """
    cursor = connection.cursor()
    cursor.execute(query)
    members = cursor.fetchall()
    descriptions = cursor.description
    members_list = []

    for member in members:
        members_dict = {}
        for i in range(len(descriptions)):
            description, *rest = descriptions[i]
            members_dict[description] = member[i]
        members_list.append(members_dict)

    for member in members_list:
        print(member)

    members_post = Member.objects.values(
        'id',
        'member_email',
        'member_name',
    ).annotate(post_count=Count('post'))

    members_reply = Member.objects.values(
        'id',
        'member_email',
        'member_name',
    ).annotate(reply_count=Count('reply'))

    for i in range(len(members_post)):
        members_post[i]['reply_count'] = members_reply[i]['reply_count']

    for member_post in members_post:
        print(member_post)

    # 회원 이름이 "테스트6"이거나 회원 나이가 30이상인 회원이 작성한 게시글 목록 조회
    # Q()는 쿼리문에 들어갈 여러개의 조건을 하나로 합칠때 사용한다.
    name_condition = Q(member_name='테스트6')
    age_condition = Q(member_age__gte=30)
    # 이렇게 작성하면 Q()에 입력한 두 조건이 OR 연산자와 합쳐져 condition에 담기게 된다.
    condition = name_condition | age_condition

    # values()에 아무것도 전달하지 않으면 모든 칼럼의 데이터를 가져오겠다는 뜻이다.
    members = Member.objects.filter(condition).values()
    for member in members:
        print(member)

    # 새로운 조건식을 사용하기 위해 condition을 초기화 시켜준다.
    # Q()를 사용하면 아무런 조건이 없다는 것을 뜻한다.
    condition = Q()

    # Q()에 입력한 두 조건이 OR 연산자와 합쳐져 condition에 담기게 된다.
    condition |= name_condition
    condition |= age_condition

    # search
    # 화면에서 입력받은 데이터
    data = {
        'region': '',
        'color': '검은색',
        'date': '2019-05-01'
    }
    # Q()를 사용해 조건식을 만든다.
    region_condition = Q(region=data['region'])
    color_condition = Q(color=data['color'])
    # 이전에 만들어둔 condition에 담긴 조건식을 초기화해주고
    condition = Q()
    if data.region:
        # and연산자로 if문 조건에 맞는 조건식을 condition에 추가해준다.
        condition &= region_condition

    if data.color:
        condition &= color_condition
    # if문을 통해 합쳐진 조건식을 filter에 전달하여 search기능을 구현한다.
    Post.objects.filter(condition)

    # range
    # 회원의 나이가 20이상 30이하인 회원이 작성한 게시글 중 post_title에 "테"가 들어가고 내용에 "7"로 끝나는 게시글 정보 조회
    members = Member.objects.filter(
        member_age__range=[20, 30],
        post__post_title__contains='테',
        post__post_content__endswith='7'
    ).values('member_age', 'post__post_title', 'post__post_content')

    for member in members:
        print(member)

    posts = Post.objects.filter(
        member__member_age__range=[20, 30],
        post_title__contains='테',
        post_content__endswith='7'
    ).values('member__member_age', 'post_title', 'post_content')

    for post in posts:
        print(post)

    # contains
    # filter안에 들어갈 조건식을 작성할때 접근하고자하는 필드 뒤에 __contains를 작성하면
    # '테'를 포함하고 있는 member_name 이 있는 객체들을 가져온다.
    # contains는 대소문자를 구별하지 않는다.
    member_queryset = Member.enabled_objects.filter(member_name__contains='테')
    print(member_queryset.exists())
    for member in member_queryset:
        print(member.__dict__)

    # startswith, endswith
    # startswith는 시작하는 단어, endswith는 끝나는 단어가 동일한 객체를 찾아준다.
    member_queryset = Member.enabled_objects.filter(member_name__startswith='테')
    print(member_queryset.exists())
    for member in member_queryset:
        print(member.__dict__)
    member_queryset = Member.enabled_objects.filter(member_name__endswith='3')
    print(member_queryset.exists())
    for member in member_queryset:
        print(member.__dict__)

    # in
    # __in을 사용할 경우 []안에 전달한 값들이 member_email에 정확히 일치하는 객체들을 가져온다.
    member_queryset = Member.enabled_objects.filter(member_email__in=['test3@gmail.com', 'test6@gmail.com']).values(
        'member_email')
    print(member_queryset.query)
    for member in member_queryset:
        print(member.get('member_email'))

    # exclude()
    # exclude()는 전달한 값이 포함되지 않은 객체들을 가져온다.
    # values는 QuerySet이 아닌 dict타입으로 데이터를 가져온다.
    member_queryset = Member.enabled_objects.exclude(member_email='test3@gmail.com').values('member_email')
    for member in member_queryset:
        print(member["member_email"])

    # AND, OR
    # AND는 여러 조건을 모두 충족해야 한다.
    # OR는 여러 조건중 하나만 충족되어도 된다.
    member_queryset = Member.objects.filter(status=True) & Member.objects.filter(member_age__gt=30)
    condition1 = Q(status=True)
    condition2 = Q(member_age__gt=30)
    member_queryset = Member.objects.filter(condition1 & condition2)
    member_queryset = Member.objects.filter(condition1 | condition2)
    for member in member_queryset:
        print(member.member_email, member.member_age, sep=", ")

    # order_by
    # order_by는 가져온 데이터드을 정렬할 때 사용한다.
    member_queryset = Member.objects.all().order_by('-id')
    for member in member_queryset:
        print(member.__dict__)

    # aggregate
    # annotate()는 QuerySet객체로 리턴하기 때문에 뒤에 이어서 추가 작업이 가능하지만,
    # aggregate()는 전체 대상이므로 뒤에 이어서 추가 작업이 불가능하다.
    # aggregate() 는 집계함수를 사용하고자 할때 사용된다.
    # max_age=Max('member_age')를 하게 되면 max_age라는 키를 만들고
    # max_age이란 키에 집계함수를 사용해 나온 값들을 담아둔다.
    # aggregate()는 dict타입을 리턴한다.
    member = Member.objects.aggregate(max_age=Max('member_age'), min_age=Min('member_age'))
    # 출력: 50 20
    print(member['max_age'], member['min_age'])
    # 출력: {'max_age': 50, 'min_age': 20}
    print(member)

    # save
    # save()는 수정된 정보를 저장해준다.
    # 수정할 때는 save()안에서 해주는 것이 아니라
    # 객체를 따로 수정을 해주고 뒤에 save()를 붙여준다.
    # 회원 이름 수정
    data = {
        'member_email': 'test2@gmail.com',
        'member_password': '3333'
    }

    member = Member.objects.get(**data)

    member.member_name = '수정된 이름'
    member.member_password = '3333'
    # save()에 update_fields를 사용해 해당 칼럼명을 입력하면
    # 해당 칼럼만 저장된다.
    # save()를 사용하게 되면 모든 필드를 한번씩 다 저장하게 된다.
    member.save(update_fields=['member_name'])

    member = Member.objects.filter(**data)
    # update()는 업데이트 하고 싶은 필드명과 업데이트할 값을 전달하면 된다.
    count = member.update(member_name='다시 수정된 이름')
    print(count)

    count = Member.objects.update(member_name='수정된 이름')
    print(count)

    # 나이가 20살 이하인 회원의 나이를 +1한다.
    # F()를 사용하게 되면 직접 데이터베이스의 해당 필드의 값을 처리하므로 성능에서 이점이 있다.
    # 조회수 같이 기존 데이터베이스 값을 가져와 업데이트를 해야하는 경우에 용이하다.
    count = Member.objects.filter(member_age__lte=20).update(member_age=F('member_age') + 1)
    print(count)

    # delete
    try:
        count = Member.objects.get(id=26).delete()
        print(count)
    except ProtectedError:
        print('ProtectedError')
