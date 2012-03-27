from time import strptime
from datetime import datetime, date, time, timedelta
from django_geckoboard.decorators import number_widget, rag_widget, funnel
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db.models import Sum

from jmbocomments.models import UserComment
from jmboarticles.models import Article


def time_comparison(qs, field, days):
    delta = timedelta(days=int(days))
    ts_start = datetime.now() - delta - delta
    ts_middle = datetime.now() - delta

    qs_this = qs.filter(**{'%s__gte' % field: ts_middle})
    qs_past = qs.filter(**{'%s__range' % field: (ts_start, ts_middle)})
    return (qs_this.count(), qs_past.count())


@number_widget
def total_users_joined(request):
    """
    Total users.
    """
    days = request.GET.get('days', None)
    qs = User.objects.filter(
        username__startswith=request.GET.get('startswith', ''))

    if days:
        return time_comparison(qs, 'date_joined', days)
    return qs.count()


@number_widget
def total_comments(request):
    """
    Total comments
    """
    days = request.GET.get('days', None)
    qs = UserComment.objects.filter(site=Site.objects.get_current())

    if days:
        return time_comparison(qs, 'submit_date', days)
    return qs.count()

@number_widget
def total_page_views(request):
    """.order_by('-pub_date',
    Total page views
    """
    result = Article.objects.all().aggregate(view_count=Sum('view_count'))

    return result['view_count']

@funnel
def page_views_by_article(request):
    """
    Total page views by articles
    """
    
    limit = request.GET.get('limit', 5)
    all_articles = Article.objects.all().order_by('-view_count')
    
    return {
        "items": [(article.view_count, article.title) for article in all_articles[:limit]],
        "type": "standard",   # default, 'reverse' changes direction
                              # of the colors.
        }