from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView

#Url defined here, can access the page related to the url by adding the path
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/$',views.event, name='events'),
    url(r'^events/details/$', views.details, name='details'),
    url(r'^contactus/$', views.contactus, name='contactus'),
    url(r'^login/register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^RegisterHead/$', views.RegisterHead, name='RegisterHead'),
    url(r'^service-worker.js', (TemplateView.as_view(
    template_name="service-worker.js",
    content_type='application/javascript',
    )), name='service-worker.js'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]



