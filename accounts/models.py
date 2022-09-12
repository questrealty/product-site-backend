
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, first_name, password1=None, password2=None):
        user = self.create_user(self, email, first_name, password1, password2)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        # if other_fields.get('is_staff') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_staff=True.')
        # if other_fields.get('is_superuser') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_superuser=True')
        # return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, country_code, format_digits, password1=None, password2=None):
        if not email:
            raise ValueError(_('You must provide a valid email address'))
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, first_name=first_name, last_name=last_name, country_code=country_code, format_digits=format_digits, password1=password1, password2=password2)

        user.set_password(password1)
        user.save(using=self._db)

        return user

    def create_agent(self, email, first_name, last_name, country_code, format_digits, password1=None, password2=None):
        user = self.create_user(self, email, first_name, last_name, country_code, format_digits, password1, password2)

        user.is_agent = True
        user.save(using=self._db)

        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique= True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    country_code = models.IntegerField()
    format_digits = models.IntegerField()
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
