from django.urls import path, re_path
from .views import UserProfileUpdateView, UserProfileView, confirm_subscribe, send_password_reset_email, reset_password, subscribe


urlpatterns = [
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('reset_password/', send_password_reset_email, name='send_password_reset_email'),
    path('subscribe/', subscribe, name='subscribe'),
    path('confirm/<str:confirm_token>/', confirm_subscribe, name='confirm_subscribe'),
    re_path(r'^reset_password/(?P<key>\w+)/$', reset_password, name='reset_password'),
]