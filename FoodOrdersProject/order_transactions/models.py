from django.db import models
from master.models import PaymentMethod, Categories, Medias, Promos


class Couponts(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    end_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    percentage = models.IntegerField()
    max_discount_price = models.IntegerField()
    min_order_price = models.IntegerField()
    discount_price = models.IntegerField()
    is_fix = models.BooleanField()
    expired = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."couponts"'


class Menus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='master')
    category = models.CharField()
    price = models.IntegerField()
    promo_price = models.IntegerField()
    promo = models.BooleanField()
    promo_id = models.ForeignKey(
        Promos, on_delete=models.CASCADE, related_name='master')
    media_id = models.ForeignKey(
        Medias, on_delete=models.CASCADE, related_name='master')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."Menus"'


class Orders(models.Model):
    session = models.CharField()
    name = models.CharField()
    queue = models.IntegerField()
    total_price = models.IntegerField()
    payment_method_id = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name='master')
    final_price = models.IntegerField()
    order_date = models.DateField()
    coupont_code = models.ForeignKey(
        Couponts, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    payment_code = models.CharField(max_length=20)
    payment = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."orders"'


class OrderMenus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    session = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name='order_transactions')
    menu_id = models.CharField()
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = '"food_orders"."order_menus"'
