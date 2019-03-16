from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView
from django.urls import path

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
    url(r'^register-head11$', views.register_head, name='RegisterHead'),
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
    url(r'^our-team/$', views.our_team, name='ourTeam'),
    url(r'^verifyOTP/$', views.verifyOTP, name='verifyOTP'),
    url(r'^excel/$', views.campaigning_excel, name='TableToExcel'),
    url(r'^volunteer-data/$', views.volunteer_excel, name='volunteer-data'),
    url(r'^file-upload/$', views.files, name='files'),
    url(r'^myactions/$', views.myaction, name='myactions'),
    url(r'all-participants', views.all_participants, name='all_participanrs'),
    url(r'^mail-participants', views.mail_participants, name='mail-participants'),
    # url(r'^myactions/$', views.myaction, name='myactions'),
    url(r'^offline/$', views.offline, name='offline'),
    url(r'^terms-and-conditions/$', views.terms, name='terms'),
    url(r'^privacy-policy/$', views.policy, name='policy'),
    url(r'^change-password/$', views.change_password, name='change-password'),
    url(r'^send-username/$', views.send_username, name='send-username'),
    url(r'^other-uploads/$', views.other_uploads, name='other-uploads'),
    url(r'^uploaded-docs/$', views.uploaded_docs, name='uploaded-docs'),
    url(r'^event-head/$', views.event_head, name='event-head'),
    url(r'^publicity-head/$', views.publicity_head, name='publicity-head'),
    url(r'^hear-about-us$', views.hear_about_us, name='hear-about-us'),
    url(r'^participant-live$', views.participant_live, name='participant-live'),
    url(r'^verifyOTP-event$', views.verifyOTP_event, name='verifyOTP-event'),
    url(r'^pariwartan$', views.pariwartan, name='pariwartan'),
    url(r'^event-count', views.event_count, name='event-count'),
    url(r'^pariwartan-upload$', views.pariwartan_upload, name='pariwartan-upload'),
    url(r'^live$', views.live, name='live'),
    url(r'^json-view', views.jsonview, name='json-view'),
    url(r'^qr-code-verify$', views.qr_verify, name='qr-verify'),

    url(r'^web-push$', views.web_push, name='web-push'),
    url(r'^event-presenty$', views.event_present, name='event-presenty'),
    url(r'^send-push$', views.send_push, name='send-push'),
    url(r'^webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    url(r'^verify-feedback$', views.verify_qr_feedback, name='verify_qr_feedback'),
    url(r'^feedback$', views.feedback, name='feedback'),
]
