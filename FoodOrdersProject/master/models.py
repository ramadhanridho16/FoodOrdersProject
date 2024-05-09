from django.db import models


class Categories(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(null=False, max_length=100)

    def __str__(self) -> str:
        return f'{self.id} => {self.name}'

    class Meta:
        db_table = '"food_orders"."categories"'


class Medias(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(null=False, max_length=200)
    type = models.CharField(null=False, max_length=100)
    size = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f'{self.id} => {self.name}'

    class Meta:
        db_table = '"food_orders"."medias"'


class PaymentMethod(models.Model):
    class PrefixChoices(models.TextChoices):
        BANK = 'BNK', 'Bank'
        GOJEK = 'GJK', 'Gojek'
        DANA = 'DNA', 'Dana'
        OVO = 'OVO', 'Ovo'
        SHOPEE = 'SHP', 'Shopee'

    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(null=False, max_length=200)
    prefix_code = models.CharField(
        default='', max_length=3, null=False, choices=PrefixChoices.choices)

    def __str__(self) -> str:
        return f'{self.prefix_code} => {self.name}'

    class Meta:
        db_table = '"food_orders"."payment_methods"'


class Promos(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(null=False, max_length=200)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self) -> str:
        return f'{self.id} => {self.name}'

    class Meta:
        db_table = '"food_orders"."promos"'


class HomeBanners(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, null=False)
    media = models.OneToOneField(
        Medias, on_delete=models.RESTRICT, db_column='media_id', null=False)

    def __str__(self) -> str:
        return f'{self.id} => {self.name}'

    class Meta:
        db_table = '"food_orders"."home_banners"'
