from dataclasses import field
from .models import Wallet, WalletTransaction, Review, Message
from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
import requests

class ReviewSerializer(serializers.ModelSerializer):
    class Meta():
        model = Review
        fields = ('name', 'profession', 'image', 'content')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password','Phone-number','Date-of-birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email']    
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class WalletSerializer(serializers.ModelSerializer):

    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        bal = WalletTransaction.objects.filter(
            wallet=obj, status="success").aggregate(Sum('amount'))['amount__sum']
        return bal

    class Meta:
        model = Wallet
        fields = ['id', 'currency', 'balance']


def is_amount(value):
    if value <= 0:
        raise serializers.ValidationError({"detail": "Invalid Amount"})
    return value


class DepositSerializer(serializers.Serializer):

    amount = serializers.IntegerField(validators=[is_amount])
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"detail": "Email not found"})

    def save(self):
        user = self.context['request'].user
        wallet = Wallet.objects.get(user=user)
        data = self.validated_data
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        
        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type="deposit",
            amount= data["amount"],
            paystack_payment_reference=response['data']['reference'],
            status="pending",
        )

        return response
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'username', 'password']

   
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']