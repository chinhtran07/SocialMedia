from datetime import datetime

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from . import dao
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.

class SocialNetworkAppAdminSite(admin.AdminSite):
    site_header = "Alumni Social Network"

    def get_urls(self):
        return [
            path('stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html')


admin_site = SocialNetworkAppAdminSite(name='myapp')


class AlumniProfileInlineAdmin(admin.StackedInline):
    model = AlumniProfile


def reset_password_change_time(modeladmin, request, queryset):
    for user in queryset:
        user.date_joined = datetime.now()
        user.save()


reset_password_change_time.short_description = "Reset Password Change Time"


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'is_active']
    search_fields = ['username']
    list_filter = ['username', 'first_name', 'role']
    inlines = [AlumniProfileInlineAdmin, ]
    actions = [reset_password_change_time]


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date', 'active']
    form = PostForm


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


admin_site.register(User, UserAdmin)