from datetime import datetime, timedelta

from django.http import HttpResponse


class PasswordChangeLecturerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and not user.password_changed and user.role == 'lecturer':
            account_date_joined = user.date_joined
            if account_date_joined and datetime.now() - account_date_joined >= timedelta(hours=24):
                # Block the account or perform any desired action
                user.is_active = False
                return HttpResponse("Tài khoản của thầy cô đã bị khóa. "
                                    "Vui lòng liên lạc với Quản trị viên để reset thời gian đổi mật khẩu")

        response = self.get_response(request)
        return response