#inlcude the various features which are to be used in Views here
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from EventApp.models import Department, EventMaster, Carousel, SponsorMaster, RoleAssignment, RoleMaster, MyUser, EventDepartment,GandharvaHome,College
from .forms import UserRegistration , ContactUsForm, RoleMasterForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from .token import *
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from EventApp.decorators import user_Role_head

# Create your views here.


#Home page Functionality
def home(request):

    args = {
        'events': Department.objects.all(),
        'sponsors': SponsorMaster.objects.all(),
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': GandharvaHome.objects.get(title__startswith= "Date").data,
        'About' : GandharvaHome.objects.get(title__startswith= "About").data,
    }

    return render(request, 'gandharva/index.html', args)

#ComingSoon Page
def comingSoon(request):

    arg = {
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': 'March 20, 2019'
    }

    return render(request, 'gandharva/comingSoon.html', arg)

#Events page of all Departments
def event(request):
    if request.GET:
        dept = request.GET.get('dept')
        dept_choose = Department.objects.get(name=dept)
    else:
        dept = 'All Events'
    args1 = {
        'pageTitle': dept,
        'events': EventDepartment.objects.filter(department = dept_choose),
        'dept_choosen': dept_choose
    }
    return render(request, 'events/newEvent.html', args1)

#Details of Individual Events
def details(request):
    event_name = request.GET.get('event')

    arg = {
        'events_list': EventMaster.objects.all(),
        'pageTitle': EventMaster.objects.get(event_name__startswith=event_name).event_name,
        'event': EventMaster.objects.get(event_name__startswith=event_name),
        'dept': EventDepartment.objects.get(event = EventMaster.objects.get(event_name__startswith=event_name)),
    }
    return render(request, 'events/category1Event1.html', arg)

#ContactUs View (Form created)
def contactus(request):
    success_form = False
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            success_form = True
        else:
            print(form.errors)
    else:
        form = ContactUsForm()

    return render(request, 'gandharva/contactus.html',{'form':form, 'success_form' : success_form})

#Registration for normal User and log in user after registration Immediately
@user_passes_test(lambda u: u.is_superuser)
def register(request):
    dept = Department.objects.all();
    coll = College.objects.all();
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('user/acc_active_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account to continue.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'user/AccountConfirm.html')
        else:
            print(form.errors)
    else:
        form = UserRegistration()

    return render(request, 'events/register.html', {'form': form,'colleges':coll,'depts': dept})


# Activates the user after clicking on the email link
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        # return redirect('home')
        return render(request, 'user/accountActivate.html')
    else:
        return HttpResponse('You have already confirmed your email id. Activation link is invalid!')


#logout Option View appears only after login
def user_logout(request):
        logout(request)
        return redirect('home')

#Login for user to Existing Account
def user_login(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home')
                    else:
                        print("Your account was inactive.")
            else:
                messages.error(request, 'Error wrong username/password')
                return render(request, 'events/login.html', {})

        else:
            return render(request, 'events/login.html', {})

def payment (request):
    return render(request, 'user/paymentDetails.html', {})

#Head Login View only to be used for Heads
@user_passes_test(lambda u: u.is_superuser)
def RegisterHead(request):
    Roles = RoleMaster.objects.all();
    dept = Department.objects.all();
    coll = College.objects.all();
    if request.method == 'POST':
        userform = UserRegistration(request.POST)
        roleform = RoleMasterForm(request.POST)
        if userform.is_valid() and roleform.is_valid():
            user = userform.save()
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            roleassign = RoleAssignment()
            roleassign.user=user
            roleassign.role = roleform.cleaned_data.get('name')
            roleassign.save()
      #       group = Group.objects.get(name='groupname')
      #      user.groups.add(group)
      #login(request, user, backend='social_core.backends.google.GoogleOAuth2')
            return redirect('home')
        else:
            print (userform.errors)
            print (roleform.errors)


    else:
        userform = UserRegistration()
        roleform = RoleMasterForm

    return render(request, 'events/RegisterHead.html', {'userform': userform , 'roleform': roleform, 'roles':Roles ,'depts':dept,'colleges':coll})




## Important Notes:
# to get user role from models
 #userget = RoleAssignment.objects.get(user=request.user.id)
 #   print (userget.role)


