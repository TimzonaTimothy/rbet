from django.urls import path, re_path, reverse_lazy
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name="login"),
    path('logout', user_logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('dashboard', dashboard, name="dashboard"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)