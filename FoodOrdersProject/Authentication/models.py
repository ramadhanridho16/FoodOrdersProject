from django.db import models

# Create your models here.
class Users(models.Model):
    class PrefixChoices(models.TextChoices):
        PRIA = 'P', 'Pria'
        WANITA = 'W', 'Wanita'

    username = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=1, null=False, choices=PrefixChoices.choices)
    birth_date = models.DateField(null=False)
    email = models.CharField(max_length=100, null=True)
    activate = models.BooleanField(null=False, default=False)

    def __str__(self) -> str:
        return f'{self.username}'
    
    class Meta:
        db_table = '"food_orders"."users"'


class UserVerifies(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    token = models.CharField(max_length=100, null=False)
    expired_at = models.DateTimeField(null=False)
    username = models.OneToOneField(Users, on_delete=models.CASCADE, null=False, db_column='username')

    def __str__(self) -> str:
        return f'{self.id} => {self.username}'
    
    class Meta:
        db_table = '"food_orders"."user_verifies"'


class ForgetPasswords(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    token = models.CharField(max_length=100, null=False)
    expired_at = models.DateTimeField(null=False)
    username = models.OneToOneField(Users, on_delete=models.CASCADE, null=False, db_column='username')

    def __str__(self) -> str:
        return f'{self.id} => {self.username}'
    
    class Meta:
        db_table = '"food_orders"."forget_passwords"'
