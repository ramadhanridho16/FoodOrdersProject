from rest_framework import serializers
from .models import Categories


class Test(serializers.Serializer):
    name = serializers.CharField(allow_blank=False, error_messages={
                                 'blank': 'Harus diisi ngab'})
    age = serializers.IntegerField(max_value=10, required=True)


class CategoryRequest(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']
