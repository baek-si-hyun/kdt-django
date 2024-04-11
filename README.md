# Model

- Django에서 models.Model이라는 추상화된 클래스를 사용하여 데이터베이스에 테이블을 정의 할 수 있다
- models.Model 을 상속받은 클래스로 구현할 수 있으며, 내부 클래스로 Meta 클래스를 선언할 수 있다.

## Model Convention

    모델 내 코드를 작성할 때 아래의 순서에 맞춰 작성하는 것을 권장한다.
    1. Constant for choices
    2. All databases Field
    3. Custom manager attributes
    4. class Meta
    5. def __str__()
    6. def save()
    7. def get_absolute_url()
    8. Any custom methods

### 1. Constant for choices

- DB에 저장할 값과 실제 화면에 보여지는 값이 다를 경우 미리 튜플 형태로 선언해 놓고 사용한다.

####

      CONSTANT = [
        ('DB 저장 값', '화면 출력 값'),
        ...
      ]

### 2. All databases Field

####

    ForeignKey(to, verbose_name, related_name, related_query_name, on_delete, null)
    OneToOneField(to, verbose_name, related_name, related_query_name, on_delete, null)
    ManyToManyField(to, verbose_name, related_name, related_query_name, on_delete, null)

    - related_name
      - 역참조가 필요한 다대다 또는 일대다 관계에서 유용하게 사용된다.
      - B필드에 a객체 선언 후 참조 시 b.a로 접근할 수 있으나
      - 역참조인 a.b로는 접근할 수 없다. A필드에는 b객체가 없기 때문이다.
      - _set객체를 사용하면 역참조가 가능하고 a.b_set으로 역참조가 가능하다.
      - 만약 _set객체의 이름을 다른 이름으로 사용하고자 할 때 바로 related_name을 사용한다.

- 문자열

  - 문자열 필드는 null=False로 하고 필수 요소가 아니라면 blank=True로 설정한다.
  - 이렇게 설정하는 이유는 null과 빈 값을 "null이거나 빈 문자일 경우 빈 값이다"라고 검사할 필요 없이 빈 문자열인지로만 판단할 수 있게 되기 때문이다.

  ####

      최대 길이 제한이 필요한 경우
      CharField(verbose_name, max_length, choices, blank, null, default)

      최대 길이 제한이 필요 없을 경우
      TextField(verbose_name, null=False, blank=True)

- 정수

  - max_length를 지정하지 않고 기본적으로 byte가 정해져있다.

  ####

      PositiveSmallIntegerField(verbose_name, choices, null, default)
      SmallIntegerField(verbose_name, choices, null, default)
      IntegerField(verbose_name, choices, null, default): 4byte
      BigIntegerField(verbose_name, choices, null, default)
      BooleanField(verbose_name, default): 1byte

- 날짜

####

- auto_now_add=True

  - 최초 한 번만 자동으로 필드 값을 현재 시간으로 설정한다.
  - 보통 등록 날짜 항목으로 사용된다.

- auto_now=True

  - 객체가 변경될 때마다 자동으로 필드 값을 현재 시간으로 수정한다.
  - 보통 수정된 날짜 항목으로 사용된다.
  - 하지만, save()를 사용해야 적용되고 update()를 사용하면 적용되지 않는다.
  - auto_now=True처럼 사용하고 싶다면, default=timezone.now을 사용하는 것이 올바르다.
  - ※ django.utils.timezone.now으로 설정한 뒤 update할 때 마다 그 때의 now로 넣어준다.

  ####

      DateField(verbose_name, null, default, auto_now_add, auto_now)
      TimeField(verbose_name, null, default, auto_now_add, auto_now)
      DateTimeField(verbose_name, null, default, auto_now_add, auto_now)

### 3. Custom manager attributes

- 데이터베이스와 상호작용하는 인터페이스(틀)이며 Model.object 속성을 통해 사용한다.
- Custom Manager와 Custop QuerySet을 통해 사용할 수 있으며,
  공통적으로 사용되는 쿼리를 공통 함수로 정의할 수 있고 싱제 동작을 숨길 수 있다.

### 4. class Meta

- Model클래스 안에 선언되는 내부 클래스이며, 모델에 대한 기본 설정들을 변경할 수 있다
- Meta 클래스가 작동하기 위해서는 정해진 속성과 속성값을 작성해야 하고, 이를 통해, Django를 훨씬 편하게 사용할 수 있다.

- 데이터 조회 시 정렬 방법 설정
  - ordering = ['필드명']
  - ordering = ['-필드명']
- 테이블 생성시 이름 설정
  - db_table = '테이블명'
- 테이블을 생성할 것인지 설정
  - abstract = False

### 5. def \_\_str\_\_()

- 객체 조회 시 원하는 데이터를 직접 눈으로 확인하고자 할 때 사용하며, 객체 출력시 자동으로 사용되는 메서드이다.
- 모델 필드 내에서 재정의하여 원하는 필드를 문자열로 리턴하면 앞으로 객체 출력 시 해당 값이 출력된다.

### 6. def save()

- 모델 클래스를 객체화한 뒤 save()를 사용하면 INSERT 또는 UPDATE 쿼리가 발생한다.
- 이는 Django ORM이 save()를 구현해놨기 때문이다.
- save() 사용시, INSERT 또는 UPDATE 쿼리 발생 외 다른 로직이 필요할 경우 재정의 할 수 있다.
- 하지만 재정의를 하면, 객체를 대량으로 생성하거나 수정할 때 동작하지 않는다.

### 7. def get_absolute_url()

- 모델에 대해서 상세보기(DetailView)를 제작한다면, redirect(모델 객체)를 통해
  자동으로 get_absolute_url()을 호출한다.
- 추가 혹은 수정 서비스 이후 상세보기 페이지로 이동하게 된다면,
  매번 redirect에 경로를 작성하지 않고 get_absolute_url()을 재정의해서 사용하는 것을 추천한다.
