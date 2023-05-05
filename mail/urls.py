from django.urls import path, re_path
from .views import send_password_reset_email, reset_password


urlpatterns = [
    path('reset_password/', send_password_reset_email, name='send_password_reset_email'),
    re_path(r'^reset_password/(?P<key>\w+)/$', reset_password, name='reset_password'),
]