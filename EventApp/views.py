# inlcude the various features which are to be used in Views here

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from io import BytesIO
from django.core.files import File

from EventApp.models import *
from .forms import *
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
from GandharvaWeb19 import settings
from instamojo_wrapper import Instamojo
from django.db import IntegrityError
import datetime
from django.core.exceptions import ObjectDoesNotExist
import qrcode
import json


# Create your views here.


# Home page Functionality
def home(request):
    args = {
        'events': Department.objects.all(),
        'sponsors': SponsorMaster.objects.all(),
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': GandharvaHome.objects.get(title__startswith="Date").data,
        'About': GandharvaHome.objects.get(title__startswith="About").data,
    }

    return render(request, 'gandharva/index.html', args)


# ComingSoon Page
def comingSoon(request):
    arg = {
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': 'March 20, 2019'
    }

    return render(request, 'gandharva/comingSoon.html', arg)


# Events page of all Departments
def event(request):
    if request.GET:
        dept = request.GET.get('dept')
        dept_choose = Department.objects.get(name=dept)
    else:
        dept = 'All Events'
    args1 = {
        'pageTitle': dept,
        'events': EventDepartment.objects.filter(department=dept_choose),
        'dept_choosen': dept_choose
    }
    return render(request, 'events/newEvent.html', args1)


# Payment success
def success(request):
    if request.method == 'GET':
        print("Enter success")
        payment_id = request.GET.get('payment_id')
        payment_status = request.GET.get('payment_status')
        payment_request_id = request.GET.get('payment_request_id')
        insta = InstamojoCredential.objects.latest('key')
        api2 = Instamojo(api_key=insta.key,
                         auth_token=insta.token,
                         endpoint='https://test.instamojo.com/api/1.1/')
        response2 = api2.payment_request_payment_status(payment_request_id, payment_id)

        print(response2['payment_request']['purpose'])  # Purpose of Payment Request
        print(response2['payment_request']['payment']['status'])  # Payment status
        eid = request.GET.get("eid")
        event = EventMaster.objects.get(event_id=eid)
        user = MyUser.objects.get(email=response2['payment_request']['email'])
        try:
            transaction2 = Transaction.objects.get(transaction_id=payment_id)
            print("herereere")
            print(transaction2)
        except(IntegrityError, ObjectDoesNotExist):
            transaction2 = None
            print("here")
            # transaction2=Transaction.objects.get(transaction_id=payment_id)
            # print(transaction2)
        if transaction2 == None:
            receipt = Receipt()
            team = Team()
            transaction = Transaction()
            receipt.name = response2['payment_request']['payment']['buyer_name']
            receipt.event = event
            receipt.save()
            team.receipt = receipt
            team.user = user
            team.save()
            transaction.transaction_id = payment_id
            transaction.transaction_request_id = payment_request_id
            transaction.instrment_type = response2['payment_request']['payment']["instrument_type"],
            transaction.billing_instrument = response2['payment_request']['payment']["billing_instrument"]
            transaction.status = payment_status
            transaction.receipt = receipt
            transaction.date = datetime.date.today()
            transaction.time = datetime.datetime.now().time()
            transaction.team = team
            transaction.save()
            # Generate QR code if transaction is success full
            if transaction.status == "Credit":
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
                content = "event:" + event.event_name + ", user:" + user.username
                qr.add_data(content)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(user.username + event.event_name + "png")
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')
                team.QRcode.save('ticket-filename.jpg', File(thumb_io), save=False)
                team.save()

        teams = reversed(Team.objects.filter(user=request.user).reverse())
        print(teams)

        return render(request, 'user/registeredEvents.html', {'teams': teams})
    else:
        print("ERROR")


# Details of Individual Events
def details(request):
    if request.method == 'POST':
        insta = InstamojoCredential.objects.latest('key')
        api = Instamojo(api_key=insta.key,
                        auth_token=insta.token,
                        endpoint='https://test.instamojo.com/api/1.1/')
        event_id = request.POST.get('event_id')
        userEmail = request.POST.get('userEmail')
        event = EventMaster.objects.get(pk=event_id)
        user = MyUser.objects.get(email=userEmail)
        response = api.payment_request_create(
            amount=event.entry_fee,
            purpose=event.event_name,
            send_email=False,
            send_sms=False,
            email=user.email,
            phone=user.user_phone,
            redirect_url="http://127.0.0.1:8000/success?eid=" + event_id
        )
        # print the long URL of the payment request.
        print(response['payment_request']['longurl'])
        # print the unique ID(or payment request ID)
        print(response['payment_request']['id'])
        print(response['payment_request']['purpose'])
        print(response['payment_request']['amount'])

        return redirect(response['payment_request']['longurl'])
    else:
        event_name = request.GET.get('event')
        arg = {
            'events_list': EventMaster.objects.all(),
            'pageTitle': EventMaster.objects.get(event_name__startswith=event_name).event_name,
            'event': EventMaster.objects.get(event_name__startswith=event_name),
            'dept': EventDepartment.objects.get(event=EventMaster.objects.get(event_name__startswith=event_name)),
        }
        return render(request, 'events/category1Event1.html', arg)


# ContactUs View (Form created)
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

    return render(request, 'gandharva/contactus.html', {'form': form, 'success_form': success_form})


# Registration for normal User and log in user after registration Immediately
def register(request):
    dept = Department.objects.all()
    coll = College.objects.all()
    year = College_year.objects.all()
    if request.method == 'POST':
        form = UserRegistration(request.POST, request.FILES)

        new_email = request.POST.get('email')

        try:
            old_user = MyUser.objects.get(email=new_email)
        except:
            old_user = None

        if old_user != None and old_user.is_active == False:
            old_user.delete()

        elif old_user != None and old_user.is_active == True:
            args = {
                'error': "You have already registered and your email is verified too. Enter email to reset your password."
            }
            return render(request, "user/reset_password.html", args)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.user_phone = form.cleaned_data.get('user_phone')
            user.save()
            current_site = get_current_site(request)
            token1 = account_activation_token.make_token(user)
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': token1,
            })
            user.token1 = str(token1)
            user.save()
            mail_subject = 'Activate your account to continue.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'user/AccountConfirm.html')
        else:
            print(form.errors, "heere")
    else:
        form = UserRegistration()

    return render(request, 'events/register.html', {'form': form, 'colleges': coll, 'depts': dept, 'years': year})


# Activates the user after clicking on the email link
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None:
        if user.token1 == token:
            user.is_active = True
            user.token1 = None
        user.save()
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        # return redirect('home')
        return render(request, 'user/accountActivate.html')
    else:
        return HttpResponse('You have already confirmed your email id. Activation link is invalid!')


# logout Option View appears only after login
def user_logout(request):
    logout(request)
    return redirect('home')


# Login for user to Existing Account
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


def payment(request):
    return render(request, 'user/paymentDetails.html', {})


# Head Login View only to be used for Heads
# @user_passes_test(lambda u: u.is_superuser)
def RegisterHead(request):
    Roles = RoleMaster.objects.all()
    role_categories = Role_category.objects.all()
    dept = Department.objects.all()
    coll = College.objects.all()
    year = College_year.objects.all()
    if request.method == 'POST':
        userform = UserRegistration(request.POST, request.FILES)
        roleform = RoleMasterForm(request.POST)
        if userform.is_valid() and roleform.is_valid():
            user = userform.save(commit=False)
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False
            user.save()
            print("after user assign")
            roleassign = RoleAssignment()
            roleassign.user = user
            roleassign.role = roleform.cleaned_data.get('role')

            print("after role assign")

            current_site = get_current_site(request)
            token1 = account_activation_token.make_token(user)
            message = render_to_string('user/acc_active_email_register_head.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': token1,
            })
            user.token1 = str(token1)
            token2 = account_activation_token.make_token(user)
            message2 = render_to_string('user/acc_active_email_register_head.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': token2,
            })
            user.token2 = str(token2)
            user.save()
            roleassign.save()
            mail_subject = 'Activate your account to continue.'
            to_email_one = userform.cleaned_data.get('email')
            to_email_two = userform.cleaned_data.get('coll_email')
            email = EmailMessage(mail_subject, message, to=[to_email_one])
            email.send()
            email = EmailMessage(mail_subject, message2, to=[to_email_two])
            email.send()
            return render(request, 'user/AccountConfirm.html')

            #       group = Group.objects.get(name='groupname')
            #      user.groups.add(group)
            # login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        else:
            print(userform.errors)
            print(roleform.errors)


    else:
        userform = UserRegistration()
        roleform = RoleMasterForm
    selected_roles = RoleMaster.objects.all().order_by('name')
    print(selected_roles)
    return render(request, 'events/RegisterHead.html',
                  {'userform': userform, 'roleform': roleform, 'roles': Roles, 'depts': dept, 'colleges': coll,
                   'years': year, 'categories': role_categories, 'selected_roles': selected_roles})


def load_roles(request):
    category_id = request.GET.get('role_categories')
    roles = Category_assign.objects.filter(category_id=category_id)
    return render(request, 'events/category_roles.html', {'selected_roles': roles})


def activate_register_head(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if (user is not None):
        if user.token1 == token:
            user.token1 = None
        if user.token2 == token:
            user.token2 = None
        if user.token1 == None and user.token2 == None:
            user.is_active = True
            user.is_staff = True
        user.save()
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        # return redirect('home')
        return render(request, 'user/accountActivate.html')
    else:
        return HttpResponse('You have already confirmed your email id. Activation link is invalid!')


def Profile(request):
    user = request.user
    if request.method == 'POST':
        if request.method == 'POST' and request.FILES['prof_img']:
            prof_img = request.FILES['prof_img']
            print(request.FILES['prof_img'])
            user.prof_img = prof_img
        user_phone = request.POST.get('user_phone')
        user.user_phone = user_phone
        user.save()
    return render(request, 'user/userProfile.html')


def Registered_Events(request):
    teams = reversed(Team.objects.filter(user=request.user))
    return render(request, 'user/registeredEvents.html', {'teams': teams})


def Payment_Details(request):
    return render(request, 'user/paymentDetails.html')


def TeamDetails(request):
    event = request.GET.get('event')
    event_choose = EventMaster.objects.get(event_name=event)
    if request.method == 'GET':
        form = TeamDetailsForm()
    if request.method == 'POST':
        form = TeamDetailsForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return render(request, 'events/TeamDetails.html', {'form': form, 'event': event_choose})


def reset_password(request):
    if request.method == 'POST':
        email_to_reset = request.POST.get('email')
        try:
            user = MyUser.objects.get(email=email_to_reset)
        except:
            return HttpResponse("Enter your correct email.Go back to enter the email.")

        current_site = get_current_site(request)
        token2 = account_activation_token.make_token(user)
        message = render_to_string('user/reset_password_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': token2,
        })
        user.token2 = str(token2)
        user.save()

        mail_subject = 'Reset Password'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
        return HttpResponse("Mail has been send. Click on the email link to reset password")
    else:
        return render(request, "user/reset_password.html")


def reset_password_new(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist, IntegrityError, ObjectDoesNotExist):
        user = None
    if user is not None:
        if user.token2 == token:
            user.token2 = None
            user.save()
            args = {
                'user': user,
            }
            return render(request, 'user/new_password.html', args)
        else:
            return render(request, "user/reset_password.html")
    return HttpResponse("You have already reset your password")


def new_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        id = request.POST.get('pk')
        user = MyUser.objects.get(pk=id)
        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            return render(request, 'events/login.html', {})

    return render(request, 'user/new_password.html')

## Important Notes:
# to get user role from models
# userget = RoleAssignment.objects.get(user=request.user.id)
#   print (userget.role)
