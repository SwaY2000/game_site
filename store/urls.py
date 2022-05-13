from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import NewsDetailView

urlpatterns = [
    path('', views.main, name='main'),
    path('news/', views.news, name='news'),
    path('news/<str:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('login/', views.user_login, name='user_login'),
    path('profile/', views.user_profile, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
