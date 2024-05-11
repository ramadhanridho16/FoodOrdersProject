from rest_framework import serializers


class Test(serializers.Serializer):
    name = serializers.CharField(allow_blank=False, error_messages={'blank': 'Harus diisi ngab'})
    age = serializers.IntegerField(max_value=10, required=True)
