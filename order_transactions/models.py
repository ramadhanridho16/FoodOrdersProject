from django.db import models

from master.models import PaymentMethod, Categories, Medias


class Coupons(models.Model):
    code = models.CharField(max_length=100, primary_key=True, db_column='code')
    name = models.CharField(max_length=100)
    end_date = models.BigIntegerField()
    start_date = models.BigIntegerField()
    quantity = models.IntegerField()
    percentage = models.IntegerField()
    max_discount_price = models.FloatField()
    min_order_price = models.FloatField()
    discount_price = models.FloatField()
    is_fix = models.BooleanField()
    expired = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."coupons"'


class Promos(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(null=False, max_length=200)
    percentage = models.FloatField(null=False)
    start_date = models.BigIntegerField(null=False)
    end_date = models.BigIntegerField(null=False)

    def __str__(self) -> str:
        return f'{self.id} => {self.name}'

    class Meta:
        db_table = '"food_orders"."promos"'


class Menus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Categories, db_column='category_id', on_delete=models.RESTRICT, related_name='menus', default="-")
    description = models.TextField(null=False, default="-")
    price = models.FloatField(null=False)
    promo_id = models.ForeignKey(
        Promos, on_delete=models.RESTRICT, related_name='menus')
    media_id = models.ForeignKey(
        Medias, on_delete=models.RESTRICT, related_name='menus')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."menus"'


class Orders(models.Model):
    session = models.CharField(max_length=100, primary_key=True, db_column='session')
    name = models.CharField()
    queue = models.IntegerField()
    total_price = models.FloatField()
    payment_method = models.ForeignKey(
        PaymentMethod, db_column='payment_method_id', on_delete=models.RESTRICT, related_name='orders', default="-")
    final_price = models.FloatField()
    order_date = models.DateTimeField()
    coupon = models.ForeignKey(
        Coupons, db_column='coupon_code', on_delete=models.RESTRICT, null=True, related_name='orders')
    payment_code = models.CharField(max_length=20)
    payment = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."orders"'


class OrderMenus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    order = models.ForeignKey(
        Orders, on_delete=models.RESTRICT, related_name='order_menus', db_column='session', default="-")
    menu = models.ForeignKey(
        Menus, on_delete=models.RESTRICT, related_name='order_menus', db_column='menu_id', default="-")
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'

    class Meta:
        db_table = '"food_orders"."order_menus"'
