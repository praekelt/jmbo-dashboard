from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('jmbodashboard.geckoboard.views',
    url(r'^total-users-joined/$', 'total_users_joined', name='total_users_joined'),
    url(r'^total-comments/$', 'total_comments', name='total_comments'),
    url(r'^total-page-views/$', 'total_page_views', name='total_page_views'),
    url(r'^page-views-by-article/$', 'page_views_by_article', name='page_views_by_article'),
)