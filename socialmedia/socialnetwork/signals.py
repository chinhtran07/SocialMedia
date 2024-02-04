from django.conf import settings
from django.core.mail import get_connection, EmailMessage, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import pdb
from django.conf import settings

from .models import User, Invitation


@receiver(post_save, sender=User)
def send_email_to_lecturer(sender, instance, created, **kwargs):
    if created and instance.role == instance.Role.LECTURER:
        subject = 'Account Information'
        message = f'Chào thầy/cô {instance.get_full_name()},'
        f'\n\nTài khoản thầy cô đã được tạo.\nTài khoản: {instance.username}'
        f'\nMật khẩu: {settings.PASSWORD_LECTURER_DEFAULT}\n\n '
        f'Thầy/cô vui lòng đổi mật trong vòng 24h.'
        from_email = settings.EMAIL_HOST_USER
        instance.email_user(subject, message, from_email)


@receiver(post_save, sender=Invitation)
def send_email_invitation(sender, instance, created, **kwargs):
    if created:
        subject = 'THƯ MỜI SỰ KIỆN'
        message = f'Chào các bạn,'
        f'\n\nMời các bạn tham gia, {instance.content}'
        from_email = settings.EMAIL_HOST_USER
        fail_silently = False
        recipient_list = []

        for user in instance.recipients_users.all():
            recipient_list.append(user.email)

        for group in instance.recipients_groups.all():
            for user in group.user_set.all():
                recipient_list.append(user.email)

        send_mail(subject, message, from_email, recipient_list, fail_silently)


@receiver(post_save, sender=User)
def send_mail_confirmation(sender, instance, **kwargs):
    if instance.role == instance.Role.ALUMNI and instance.is_active:
        subject = 'Account Confirmation'
        message = f'Chào bạn {instance.get_full_name()} \n\nTài khoản bạn đã được xác nhận.'
        from_email = settings.EMAIL_HOST_USER
        instance.email_user(subject, message, from_email)
