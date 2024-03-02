from datetime import datetime

from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.template.response import TemplateResponse
from django.urls import path
from rest_framework import permissions

from . import dao
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.

class SocialNetworkAppAdminSite(admin.AdminSite):
    site_header = "Alumni Social Network"

    def get_urls(self):
        return [
            path('stats/', self.stats_view),
            path('survey_stats/', self.survey_stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        type_statistic = request.GET.get('object')
        period = request.GET.get('period')
        year = request.GET.get('year')
        period = period if period is not None else 'year'
        if type_statistic == 'users':
            stats = dao.count_users_by_time_period(period, year)
        else:
            stats = dao.count_posts_by_time_period(period, year)
        return TemplateResponse(request, 'admin/stats.html', {'stats': stats, 'period': period})

    def survey_stats_view(self, request):
        survey_id = request.POST.get('survey_id')
        statistic_data = dao.stats_survey(survey_id)

        return TemplateResponse(request, 'admin/survey_stats.html',
                                {'survey': statistic_data['survey'],
                                 'text_questions': statistic_data['text_questions'],
                                 'mcq_counts': statistic_data['multiple_choice_question_counts']})


admin_site = SocialNetworkAppAdminSite(name='myapp')


def confirm_student(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = True
        user.save()


def reset_password_change_time(modeladmin, request, queryset):
    for user in queryset:
        user.date_joined = datetime.now()
        user.save()


reset_password_change_time.short_description = "Reset Password Change Time"
confirm_student.short_description = "Confirm student"


class AlumniProfileInlineAdmin(admin.StackedInline):
    model = AlumniProfile


class AlumniAdmin(admin.ModelAdmin):
    search_fields = ['student_id']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'is_active']
    search_fields = ['username']
    list_filter = ['role', 'username', 'first_name', ]
    inlines = [AlumniProfileInlineAdmin, ]
    actions = [reset_password_change_time, confirm_student]


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = '__all__'


class ImagesInlineAdmin(admin.StackedInline):
    model = Image


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_date', 'active']
    inlines = [ImagesInlineAdmin, ]
    form = PostForm


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


class ChoiceInlineAdmin(admin.StackedInline):
    model = Choice


class QuestionInline(admin.StackedInline):
    model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'survey', ]
    inlines = [ChoiceInlineAdmin, ]


class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    inlines = [QuestionInline, ]


class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'time', 'place']


admin.site.register(User, UserAdmin)
admin.site.register(AlumniProfile, AlumniAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Group, GroupAdmin)
