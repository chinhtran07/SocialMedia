from django.conf import settings
from django.core.mail import get_connection, EmailMessage, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import pdb
from django.conf import settings

from .models import User


@receiver(post_save, sender=User)
def send_email_to_lecturer(sender, instance, created, **kwargs):
    if created and instance.role == 'lecturer':
        send_mail(
                subject='Account Information',
                message=f'Chào thầy/cô {instance.get_full_name()},'
                        f'\n\nTài khoản thầy cô đã được tạo.\nTài khoản: {instance.username}'
                        f'\nMật khẩu: {settings.PASSWORD_LECTURER_DEFAULT}\n\n '
                        f'Thầy/cô vui lòng đổi mật trong vòng 24h.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
        )

