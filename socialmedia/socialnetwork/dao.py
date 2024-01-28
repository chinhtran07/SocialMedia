from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractQuarter

from .models import User, Post


def search_people(params={}):
    q = User.objects.filter(active=True)

    name = params.get('name')
    if name:
        q = q.filter(get_full_name__icontains=name)

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
    post_creation_count = (
        Post.objects.filter(filter_condition)
        .annotate(**{period: ExtractYear('created_date')} if period == 'year'else {period: ExtractMonth('created_date')})
        .values(grouping_field)
        .order_by(grouping_field)
        .annotate(user_count=Count('id'))
    )

    return post_creation_count
