from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUser(models.Model):
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                related_name='profiles_user', 
                                primary_key=True, 
                                verbose_name='Пользователь')
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to = 'images/', verbose_name = 'Изображение', blank=True)
    user_resume = models.FileField(upload_to='pdfs/', blank=True, verbose_name='Файлы')
    about_user = models.TextField(blank=True, verbose_name='О человеке')


class ProfileRecruiter(models.Model):
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                related_name='profiles_recruiter', 
                                primary_key=True, 
                                verbose_name='Работодатель')
    company_name = models.TextField(blank=True, verbose_name='Компания')
    location = models.TextField(blank=True, verbose_name='Адрес')
    company_phone = models.IntegerField(blank=True, null=True,default=0, verbose_name='Телефон')
    amount_of_emplyees = models.IntegerField(blank=True, null=True,default=0, verbose_name='Количество людей')
    about_company = models.TextField(blank=True, verbose_name='О компании')
