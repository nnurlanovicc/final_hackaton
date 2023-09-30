from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError ('Поле email не может быть пустым')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user
        
    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    username = None


    objects =UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    
    def create_activation_code(self):
        code = get_random_string(length=10, allowed_chars='0123456789')
        self.activation_code = code




'=============================================  последняя фиксация ============================================='