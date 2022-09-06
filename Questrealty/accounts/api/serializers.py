import email
from rest_framework import serializers
from accounts.models import NewUser
from django.contrib.auth import get_user_model
User = get_user_model()

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_agent',  'country_code', 'format_digits')
        extra_kwargs = {"password": {'write_only': True}}

        if NewUser.is_agent == 'True':
            NewUser.is_agent = True
        else:
            NewUser.is_agent = False
        
    def create(self, validated_data):
        password = validated_data.pop("password", None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance