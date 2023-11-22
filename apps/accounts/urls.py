from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('remember_token/', RememberTokenView.as_view(), name='remember_token'),
]
