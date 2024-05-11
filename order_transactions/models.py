from django.db import models

from master.models import PaymentMethod, Categories, Medias, Promos


class Coupons(models.Model):
    code = models.CharField(max_length=100, primary_key=True, db_column='code')
    name = models.CharField(max_length=100)
    end_date = models.DateField()
    start_date = models.DateField()
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


class Menus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(
        Categories, on_delete=models.RESTRICT, related_name='menus')
    price = models.FloatField()
    promo_price = models.FloatField()
    promo = models.BooleanField()
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
    payment_method_id = models.ForeignKey(
        PaymentMethod, on_delete=models.RESTRICT, related_name='orders')
    final_price = models.FloatField()
    order_date = models.DateTimeField()
    coupon_code = models.ForeignKey(
        Coupons, on_delete=models.RESTRICT, null=True, related_name='orders')
    payment_code = models.CharField(max_length=20)
    payment = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."orders"'


class OrderMenus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    session = models.ForeignKey(
        Orders, on_delete=models.RESTRICT, related_name='order_menus', db_column='session')
    menu_id = models.ForeignKey(
        Menus, on_delete=models.RESTRICT, related_name='order_menus', db_column='menu_id')
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'

    class Meta:
        db_table = '"food_orders"."order_menus"'
