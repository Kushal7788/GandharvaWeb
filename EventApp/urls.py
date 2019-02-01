from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView


# Url defined here, can access the page related to the url by adding the path
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/$', views.event, name='events'),
    url(r'^events/details/$', views.details, name='details'),
    url(r'^contactus/$', views.contactus, name='contactus'),
    url(r'^login/register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^success/$', views.success, name='success'),
    url(r'^profile/$', views.Profile, name='user_profile'),
    url(r'^eventsRegister/$', views.Registered_Events, name='eventsRegister'),
    url(r'^paymentDetails/$', views.Payment_Details, name='paymentDetails'),
    url(r'^TeamDetails/$', views.TeamDetails, name='TeamDetails'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^RegisterHead/$', views.RegisterHead, name='RegisterHead'),
    url(r'^login/reset_password$', views.reset_password, name='reset_password'),
    url(r'new_password', views.new_password, name='new_password'),
    url(r'^service-worker.js', (TemplateView.as_view(
        template_name="service-worker.js",
        content_type='application/javascript',
    )), name='service-worker.js'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activate_register_head/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_register_head, name='activate_register_head'),

    url(r'^reset_password_new/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_password_new, name='reset_password_new'),
]
