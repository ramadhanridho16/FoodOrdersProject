from rest_framework import serializers


class RegisterRequest(serializers.Serializer):
    # name = serializers.CharField(allow_blank=False, max_length=100, error_messages={'blank': 'name cannot be blank', 'required': 'name is required'})
    name = serializers.CharField(allow_blank=False, max_length=100)
    password = serializers.CharField(allow_blank=False, max_length=100)
    email = serializers.EmailField(allow_blank=False, max_length=100)
    phone = serializers.CharField(allow_blank=False, max_length=20)
    username = serializers.CharField(allow_blank=False, max_length=100)
    confirmation_password = serializers.CharField(allow_blank=False, max_length=100)
    gender = serializers.CharField(allow_blank=False, max_length=1)
    birth_date = serializers.CharField(allow_blank=False)
