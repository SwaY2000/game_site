from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelChoiceField, ModelForm
from django.utils.safestring import mark_safe
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm
#
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'username', 'description', 'photo']

admin.site.register(CustomUser)

class GalleryInline(admin.TabularInline):
    fk_name = 'news'
    model = GalleryNews

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,]

admin.site.register(Comment)
