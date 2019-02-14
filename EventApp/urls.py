from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView


# Url defined here, can access the page related to the url by adding the path
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/$', views.event_register, name='events'),
    url(r'^events/details/$', views.details, name='details'),
    url(r'^contactus/$', views.contactus, name='contactus'),
    url(r'^login/register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^success/$', views.success, name='success'),
    url(r'^profile/$', views.Profile, name='user_profile'),
    url(r'^events-register/$', views.registered_events, name='eventsRegister'),
    url(r'^cashpayment/$', views.cashpayment, name='cashpayment'),
    url(r'^payment-details/$', views.Payment_Details, name='paymentDetails'),
    url(r'^team-details/$', views.team_details, name='TeamDetails'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^register-head$', views.register_head, name='RegisterHead'),
    url(r'^ajax/load-roles/', views.load_roles, name='ajax_load_roles'),
    url(r'^login/reset-password$', views.reset_password, name='reset_password'),
    url(r'new-password', views.new_password, name='new_password'),
    url(r'^service-worker.js', (TemplateView.as_view(
        template_name="service-worker.js",
        content_type='application/javascript',
    )), name='service-worker.js'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activate-register-head/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_register_head, name='activate_register_head'),

    url(r'^reset-password-new/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_password_new, name='reset_password_new'),
    url(r'^campaign-head/$', views.campaign, name='campaign'),
    url(r'^add-volunteer/$', views.AddVolunteer, name='AddVolunteer'),
    url(r'participant-event-register', views.participant_event_register, name='participantEventRegister'),
    url(r'participant-details', views.participant_details, name='participantDetails'),
    url(r'^our-sponsors/$', views.ourSponsors, name='ourSponsors'),
    url(r'^our-team/$', views.ourTeam, name='ourTeam'),
    url(r'^verifyOTP/$', views.verifyOTP, name='verifyOTP'),
    url(r'^excel/$', views.campaigning_excel, name='TableToExcel'),
    url(r'^file-upload/$', views.files, name='files'),
    url(r'^myactions/$', views.myaction, name='myactions'),
    url(r'all-participants', views.all_participants, name='all_participanrs'),
    url(r'^mail-participants', views.mail_participants, name='mail-participants'),
    url(r'^myactions/$', views.myaction, name='myactions'),
    url(r'^offline/$', views.offline, name='offline'),
    url(r'^terms-and-conditions/$', views.terms, name='terms'),
    url(r'^privacy-policy/$', views.policy, name='policy'),
    url(r'^change-password/$', views.change_password, name='change-password'),

]
