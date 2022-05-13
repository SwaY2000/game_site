from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

class CustomUser(AbstractUser):
    description = models.CharField(max_length=28, verbose_name='Описание профиля', null=True, blank=True)
    photo = models.ImageField(upload_to='user/', verbose_name='Фото профиля', blank=True)

    def __str__(self):
        return self.username

class News(models.Model):
    game_names = models.CharField(max_length=28, verbose_name='Название игры', null=True, blank=True)
    mini_description = models.CharField(max_length=200, verbose_name='Краткое описание', null=True, blank=True)
    description = models.CharField(max_length=999, verbose_name='Подробное описание', null=True, blank=True)
    price = models.CharField(max_length=10, verbose_name='Цена', null=True, blank=True)
    system_requirements = models.CharField(max_length=999, verbose_name='Системные требование', null=True, blank=True)
    url_to_download = models.CharField(max_length=99, verbose_name='Ccылка на скачку', null=True, blank=True)
    category = models.CharField(max_length=99, verbose_name='Категория', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.game_names

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

class GalleryNews(models.Model):
    image = models.ImageField(upload_to='media', verbose_name='Изображение товара', null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')

class Comment(models.Model):
    post_news = models.ForeignKey('News', verbose_name='Пост', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, verbose_name='Комментарий', null=True, blank=True)
    date = models.CharField(max_length=999, verbose_name='Время комментария', null=True, blank=True)
    author = models.ForeignKey('CustomUser', verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Tournament(models.Model):
    turnament_name = models.CharField(max_length=200, verbose_name='Комментарий', null=True, blank=True)
    turnament_date = models.CharField(max_length=200, verbose_name='Комментарий', null=True, blank=True)
    turnament_fund = models.CharField(max_length=200, verbose_name='Комментарий', null=True, blank=True)
    turnament_game = models.CharField(max_length=200, verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return self.turnament_name