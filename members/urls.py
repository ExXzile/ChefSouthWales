from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.members_login, name='members_login'),
    path('', views.members_home, name='members_home'),
    path('logout', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
