import hashlib
import json
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.http import HttpResponse, JsonResponse
from .models import PasswordResetLink, SubMails
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


def generate_confirm_token(email):
    return hashlib.sha256(email.encode('utf-8')).hexdigest()

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body.get('email')
        confirm_token = generate_confirm_token(email)
        confirm_url = request.build_absolute_uri(reverse('confirm_subscribe', args=[confirm_token]))
        message = f'Перейдите по ссылке для подтверждения подписки: {confirm_url}'

        send_mail(
            'YANKI SHOP подписка на рассылку',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        SubMails.objects.create(email=email, confirm_token=confirm_token)
        return JsonResponse({'message': 'Подтвердите подписку, перейдя по ссылке, которую мы отправили на вашу почту.'})
    
    return JsonResponse({'Error'})

def confirm_subscribe(request, confirm_token):
    subscription = SubMails.objects.filter(confirm_token=confirm_token).first()
    if subscription:
        subscription.confirmed = True
        subscription.save()
        return HttpResponse('Вы успешно подписались на рассылку!')
    else:
        return JsonResponse({'Error'})



@require_POST
@csrf_exempt
def send_password_reset_email(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    email = body.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required'})

    user = get_object_or_404(User, email=email)
    key = get_random_string(length=32)

    password_reset_link = PasswordResetLink.objects.create(user=user, key=key)

    reset_url = request.build_absolute_uri(reverse('reset_password', args=[key]))
    message = f'Перейдите по ссылке для сброса пароля: {reset_url}'

    send_mail(
        'YANKI SHOP сброс пароля',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return JsonResponse({'success': 'Password reset link sent to email'})


@csrf_exempt
def reset_password(request, key):
    password_reset_link = get_object_or_404(PasswordResetLink, key=key)
    user = password_reset_link.user
    if request.method == 'GET':
        # Generate a new random password
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        # Delete the password reset link
        password_reset_link.delete()

        # Send the new password to the user via email
        send_mail(
            'YANKI SHOP новый пароль',
            f'Ваш новый пароль: {new_password}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return HttpResponse('Пароль успешно сброшен! Закройти данную страницу')
    password_reset_link.delete()



