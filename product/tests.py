import datetime
import math
import random

from django.db.models import F
from django.db.models.functions import Floor
from django.test import TestCase
from django.utils import timezone

from product.models import Product


class ProductTestCase(TestCase):
    # 상품 추가
    datas = [
        Product(product_name='춘천 국물 닭갈비', product_price=13_200, product_discount=15),
        Product(product_name='노르웨이 생연어', product_price=17_900, product_discount=20),
        Product(product_name='성주 참외', product_price=25_900, product_discount=11),
        Product(product_name='간편 미식 도시락', product_price=5_200, product_discount=20),
    ]
    # 여러 상품들을 등록
    Product.objects.bulk_create(datas)

    # 상품 게시
    count = Product.objects.all().update(status=True)
    print(count)

    # 상품 할인율 적용 가격
    products = Product.enabled_objects.all().annotate(
        # F()로 데이터베이스의 해당 칼럼에 접근해 값을 가져오고 할인율을 적용시켜 Floor로 실수타입으로 바꾼다.
        product_sell_price=Floor(F('product_price') * (1 - F('product_discount') / 100) / 10) * 10)
    for product in products:
        print(product.product_price, product.product_discount, product.product_sell_price)
        print("=" * 20)

    # 상품 수정
    count = Product.objects.filter(id=3).update(product_price=25000, updated_date=timezone.now())
    print(count)
