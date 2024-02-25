import pdb

from django.db.models import Count, Q, Value, CharField
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractQuarter, Concat
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import User, Post, Survey, SurveyResponse


def search_people(params={}):
    q = User.objects.filter(is_active=True)
    name = params.get("name")
    if name:
        q = q.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
        ).filter(full_name__icontains=name)

    return q.all()


def count_users_by_time_period(period='year', year=None):
    # Validating the period parameter
    valid_periods = ['year', 'month', 'quarter']
    if period not in valid_periods:
        raise ValueError(f"Invalid period: {period}. Valid periods are {valid_periods}.")

    # Define the annotation and grouping field based on the period
    annotation_field = f"{period}__date_joined"
    grouping_field = f"{period}"

    # Filter by year if provided
    filter_condition = Q()
    if year:
        filter_condition &= Q(date_joined__year=year)

    # Annotate the User model with the selected period and year
    user_creation_count = (
        User.objects.filter(filter_condition)
        .annotate(**{period: ExtractYear('date_joined')} if period == 'year' else {
            period: ExtractMonth('date_joined')})
        .values(grouping_field)
        .order_by(grouping_field)
        .annotate(count=Count('id'))
    )

    return user_creation_count


def count_posts_by_time_period(period='year', year=None):
    valid_periods = ['year', 'month', 'quarter']
    if period not in valid_periods:
        raise ValueError(f"Invalid period: {period}. Valid periods are {valid_periods}.")

    annotation_field = f"{period}__date_joined"
    grouping_field = f"{period}"

    # Filter by year if provided
    filter_condition = Q()
    if year:
        filter_condition &= Q(date_joined__year=year)

    if period == 'year':
        annotation = ExtractYear('created_date')
    elif period == 'month':
        annotation = ExtractMonth('created_date')
    elif period == 'quarter':
        annotation = ExtractQuarter('created_date')

    post_creation_count = (
        Post.objects.filter(filter_condition)
        .annotate(**{period: annotation})
        .values(grouping_field)
        .order_by(grouping_field)
        .annotate(count=Count('id'))
    )

    return post_creation_count


def stats_survey(survey_id):
    text_questions = []
    multiple_choice_question_counts = {}
    try:
        survey = get_object_or_404(Survey, pk=survey_id)
        responses = SurveyResponse.objects.filter(survey=survey)
        for response in responses:
            for question_response in response.questionresponse_set.all():
                if question_response.question.type == 1:
                    text_questions.append(question_response.response)
                elif question_response.question.type == 2:
                    question_title = question_response.question.title
                    response_choice = question_response.response
                    if question_title not in multiple_choice_question_counts:
                        multiple_choice_question_counts[question_title] = {}
                    if response_choice not in multiple_choice_question_counts[question_title]:
                        multiple_choice_question_counts[question_title][response_choice] = 1
                    else:
                        multiple_choice_question_counts[question_title][response_choice] += 1

                return {
                    'survey': survey,
                    'text_questions': text_questions,
                    'multiple_choice_question_counts': multiple_choice_question_counts
                }
    except Http404:
        return None
