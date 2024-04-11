from django.db import models
from django.utils import timezone

# status가 True인 데이터들만 가져오고 싶은 경우가 많을때
# 매번 filter에 조건을 추가하기보다는
# manager를 새롭게 만들어서 사용한다
class EnableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Period(models.Model):
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, default=timezone.now)
    # objects 매니저는 기본적인 쿼리셋을 관리하며, enabled_objects 매니저는 status가 True인 데이터만을 필터링하여 제공하게 된다.
    # 역참조 시 위에 선언한 Manager가 사용된다.
    objects = models.Manager()
    # 새로추가한 매니저를 사용하기 위해서는 클래스의 필드에 존재해야 한다.
    # 앞으로 Period를 상속받는 클래스들은 객체를 통해 enabled_objects에 접근해
    # status가 True인 데이터들만 가져올수 있다.
    enabled_objects = EnableManager()

    class Meta:
        abstract = True
