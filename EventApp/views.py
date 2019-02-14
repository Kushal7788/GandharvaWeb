# inlcude the various features which are to be used in Views here

import datetime
import json
import re
import string
from io import BytesIO

import openpyxl
import qrcode
import sweetify
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from instamojo_wrapper import Instamojo

from EventApp.decorators import *
from GandharvaWeb19 import settings
from .forms import *
from .token import *
from instamojo_wrapper import Instamojo
from django.db import IntegrityError
import datetime
from django.core.exceptions import ObjectDoesNotExist
import qrcode
import json
import string
import openpyxl
import sweetify
import re
from .email_sender import send_email


@staff_user
def campaigning_excel(request):
    all_transactions = Transaction.objects.filter(status='Credit')
    wb = openpyxl.Workbook()
    sheet = wb.active
    columns = ['Participant Name', 'Event', 'College', 'Date']

    heading_row_num = 1

    data_starting_number = 3

    for counter, each_column in enumerate(columns):
        curr_cell = sheet.cell(row=heading_row_num, column=counter + 1)
        curr_cell.value = each_column

    for row, each_transaction in enumerate(all_transactions):
        values = [each_transaction.team.user.first_name + " " + each_transaction.team.user.last_name,
                  each_transaction.receipt.event.event_name,
                  each_transaction.team.user.user_coll.name,
                  str(each_transaction.date)]
        for col, each_value in enumerate(values):
            curr_cell = sheet.cell(row=row + data_starting_number, column=col + 1)
            curr_cell.value = each_value

    # i = 2
    # c1 = sheet.cell(row=1, column=1)
    # c1.value = "ParticipantName"
    # c3 = sheet.cell(row=1, column=2)
    # c3.value = "EventName"
    # c2 = sheet.cell(row=1, column=3)
    # c2.value = "College Name"
    # c1 = sheet.cell(row=1, column=4)
    # c1.value = "VisitingDate"
    # c1 = sheet.cell(row=1, column=5)
    # c1.value = "VisitingTime"
    # for t in transaction:
    #     c1 = sheet.cell(row=i, column=1)
    #     c1.value = t.team.user.first_name + " " + t.team.user.last_name
    #     c2 = sheet.cell(row=i, column=2)
    #     c2.value = t.receipt.event.event_name
    #     c2 = sheet.cell(row=i, column=3)
    #     c2.value = t.team.user.user_coll.name
    #     c3 = sheet.cell(row=i, column=4)
    #     c3.value = str(t.date)
    #     c4 = sheet.cell(row=i, column=5)
    #     c4.value = str(t.time)
    #     i = i + 1
    insta = InstamojoCredential.objects.latest('pk')
    current_site = get_current_site(request)
    pathw = current_site.domain + 'media/CampaignData.xlsx'
    wb.save("media/CampaignData.xlsx")
    arg = {
        'filename': pathw,
        'transaction': all_transactions

    }
    return render(request, 'user/TableToExcel.html', arg)


def offline(request):
    return render(request, 'gandharva/offline.html', {})


# Home page Functionality
def home(request):
    userget = 0
    if request.user and (not request.user.is_anonymous):
        user = request.user
        role = user.roleassignment_set.all()
        if len(role) > 1:
            return HttpResponse('Multiple Role')
        else:
            role = role[0]
            if role.role.name == "Jt Campaigning Head" or role.role.name == "Campaigning Head":
                userget = 1

    args = {
        'events': Department.objects.all().order_by("rank"),
        'sponsors': SponsorMaster.objects.all(),
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': GandharvaHome.objects.get(title__startswith="Date").data,
        'About': GandharvaHome.objects.get(title__startswith="About").data,
        'role': userget
    }
    sweetify.sweetalert(request, 'Westworld is awesome',
                        text='Really... if you have the chance - watch it! persistent = I agree!')
    return render(request, 'gandharva/index.html', args)


# ComingSoon Page
def coming_soon(request):
    arg = {
        'carouselImage': Carousel.objects.all(),
        'gandharvaDate': 'March 20, 2019'
    }
    return render(request, 'gandharva/comingSoon.html', arg)


# Events page of all Departments
def event_register(request):
    if request.GET:
        dept = request.GET.get('dept')
        dept_choose = Department.objects.get(name=dept)

        args1 = {
            'pageTitle': dept,
            'events': EventDepartment.objects.filter(department=dept_choose).order_by('event__rank'),
            'dept_choosen': dept_choose
        }
        return render(request, 'events/newEvent.html', args1)


# Payment success
def success(request):
    if request.method == 'GET':
        # print("Enter success")
        payment_id = request.GET.get('payment_id')
        payment_status = request.GET.get('payment_status')
        payment_request_id = request.GET.get('payment_request_id')
        insta = InstamojoCredential.objects.latest('pk')
        api2 = Instamojo(api_key=insta.key,
                         auth_token=insta.token)
        response2 = api2.payment_request_payment_status(payment_request_id, payment_id)
        # print(response2)
        # print(response2['payment_request']['purpose'])  # Purpose of Payment Request
        # print(response2['payment_request']['payment']['status'])  # Payment status
        eid = request.GET.get("eid")
        event = EventMaster.objects.get(event_id=eid)
        user = MyUser.objects.get(email=response2['payment_request']['email'])
        try:
            transaction2 = Transaction.objects.get(transaction_id=payment_id)
        except(IntegrityError, ObjectDoesNotExist):
            transaction2 = None
            # transaction2=Transaction.objects.get(transaction_id=payment_id)
            # print(transaction2)

        if transaction2 is None:
            receipt = Receipt()
            team = Team()
            transaction = Transaction()
            receipt.name = response2['payment_request']['payment']['buyer_name']
            receipt.event = event
            receipt.save()
            team.receipt = receipt
            team.user = user
            if request.GET.get('ref') != "0":
                try:
                    referral = MyUser.objects.get(username=request.GET.get('ref'))
                    team.referral = referral
                except:
                    pass
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
                # print("credit ...")
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
                # content = "event:" + event.event_name + ", user:" + user.username

                # While loop for generating a unique refral code for user
                unique_event_code = ''
                while True:
                    try:
                        unique_event_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(3)) + str(
                            random.randint(100, 999))
                        Team.objects.get(Refral_Code=unique_event_code)
                    except:
                        break
                content = {
                    'event': event.event_name,
                    'username': user.username,
                    'name': receipt.name,
                    'unique_event_code': unique_event_code
                }
                qr.add_data(json.dumps(content))
                img = qr.make_image(fill_color="black", back_color="white")
                # img.save(user.username + event.event_name + "png")
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')
                team.QRcode.save('ticket-filename.jpg', File(thumb_io), save=False)

                team.Refral_Code = unique_event_code
                team.save()

                # Event Receipt Mail

                mail_subject = 'You have registered for ' + event.event_name + ' using cash payment'
                message = render_to_string('events/receiptCashPayment.html', {
                    'user': user,
                    'event': event,
                    'team': team,
                    'transaction': transaction,
                })

                send_email(user.email, mail_subject, message, [team.QRcode.path])

            if transaction.status == "Credit":
                return render(request, 'user/paymentSsuccess.html')
            elif transaction.status == "Failed":
                return render(request, 'user/paymentFailed.html')
            teams = reversed(Team.objects.filter(user=user).reverse())
            # print(teams)
        else:
            return redirect('/')
    else:
        print("ERROR")


@staff_user
def all_participants(request):
    role = RoleAssignment.objects.get(user=request.user.id)
    if role.role.name == 'Event Head':
        eventid = role.event.event_id
        # print(eventid)
        # receipt = Receipt.objects.filter(event=eventid)
        # receipt.event.event_id = event_id
        receipts = Receipt.objects.filter(event=eventid)
        # print(receipts)

        """participants = []
        for receipt in receipts:
            user = receipt.transaction_set.all()
            participants.append(user)
        print("----------------------------")
        print(participants)
        for participant in participants:
            print(participant)
        """

        participants = Transaction.objects.all()
        arg = {
            'participants': participants,
        }
        return render(request, 'events/all_participants.html', arg)


def mail_participants(request):
    if request.method == 'GET':
        emails = request.GET.getlist('email')
        return render(request, 'events/mail_participants.html', {'emails': emails})

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # regular expression to convert string to list
        to_email = re.findall(r'[\w\.-]+@[\w\.-]+', request.POST.get('emails'))

        send_email(to_email, subject, message)
        return render(request, 'events/mail_response.html')


# Details of Individual Events
def details(request):
    if request.method == 'POST':
        insta = InstamojoCredential.objects.latest('pk')
        api = Instamojo(api_key=insta.key,
                        auth_token=insta.token, )
        event_id = request.POST.get('event_id')
        userEmail = request.POST.get('userEmail')
        event = EventMaster.objects.get(pk=event_id)
        user = MyUser.objects.get(email=userEmail)
        current_site = get_current_site(request)
        head = 'http://'
        if settings.USE_HTTPS:
            head = 'https://'
        response = api.payment_request_create(
            amount=event.entry_fee,
            purpose=event.event_name,
            send_email=False,
            send_sms=False,
            email=user.email,
            phone=user.user_phone,
            buyer_name=user.first_name + " " + user.last_name,

            redirect_url=head + current_site.domain + "success?eid=" + event_id
        )
        # print the long URL of the payment request.
        # print(response['payment_request']['longurl'])
        # print the unique ID(or payment request ID)
        # print(response['payment_request']['id'])
        # print(response['payment_request']['purpose'])
        # print(response['payment_request']['amount'])

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
    success_form = 2
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            msg = request.POST.get('user_message')
            name = request.POST.get('user_name')
            user_email = request.POST.get('user_id')
            category = request.POST.get('category')
            form.save()
            success_form = 1
            mail_subject = 'The person' + name + ' has contacted us'
            message = render_to_string('gandharva/contact-us-mail.html', {
                'user': name,
                'category': category,
                'id': user_email,
                'msg': msg,
            })
            send_email('hello@viitgandharva.com', mail_subject, message)

        else:
            # print(form.errors)
            success_form = 0
    else:
        form = ContactUsForm()

    return render(request, 'gandharva/contactus.html', {'form': form, 'success_form': success_form})


# Registration for normal User and log in user after registration Immediately
@user_passes_test(lambda u: u.is_superuser)
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

        if old_user is not None and old_user.is_active is False:
            old_user.delete()

        elif old_user is not None and old_user.is_active is True:
            args = {
                'error': "You have already registered and your email is verified too. Enter email to reset your password."
            }
            return render(request, "user/reset_password.html", args)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
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
            send_email(to_email, mail_subject, message)
            return render(request, 'user/AccountConfirm.html')
            # else:
            # print(form.errors, "heere")
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
        try:
            usercheck = MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            usercheck = None
        if usercheck is not None:
            if not usercheck.is_active:
                # print("your account is inactive")
                messages.error(request, 'Email not verified, please verify your email to login')
                return render(request, 'events/login.html', {})

            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        # print("io")
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.error(request, 'Invalid Username or Password')
                        return render(request, 'events/login.html', {})
                else:
                    messages.error(request, 'Invalid Username or Password')
                    return render(request, 'events/login.html', {})

        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request, 'events/login.html', {})
    else:
        return render(request, 'events/login.html', {})


@staff_user
def myaction(request):
    role = RoleAssignment.objects.get(user=request.user.id)
    if role.role.name == "Campaigning Head" or role.role.name == "Jt Campaigning Head":
        args = {
            'button_name': 'Campaign',
            'urlaccess': campaign,
            'roles': role.role
        }
        return render(request, 'user/myactions.html', args)
    if role.role.name == 'Event Head':
        args = {
            'button_name': 'All Participants',
            'roles': role.role
        }
        return render(request, 'user/myactions.html', args)
    else:
        args = {
            'button_name': "No Actions",
            'urlaccess': None,
            'roles': role.role
        }
    return render(request, 'user/myactions.html', args)


def payment(request):
    return render(request, 'user/paymentDetails.html', {})


# Head Login View only to be used for Heads
# @user_passes_test(lambda u: u.is_superuser)
def register_head(request):
    print("enter")
    Roles = RoleMaster.objects.all()
    role_categories = Role_category.objects.all()
    dept = Department.objects.all()
    coll = College.objects.all()
    year = College_year.objects.all()
    events = EventMaster.objects.all()
    if request.method == 'POST':


        # try:
        #     old_user = MyUser.objects.get(email=userform.email)
        #     print(old_user)
        # except:
        #     old_user = None
        # try:
        #     old_user2 = MyUser.objects.get(coll_email=userform.coll_email)
        # except:
        #     old_user2 = None
        #
        # print(old_user2)
        # print(old_user)
        if MyUser.objects.filter(email=request.POST.get('email')).count() == 0:
            old_user=None
            print(old_user)
        else:
            old_user = MyUser.objects.get(email=request.POST.get('email'))
            print(old_user)
        if MyUser.objects.filter(coll_email=request.POST.get('coll__email')).count() == 0:
            old_user2 = None
            print(old_user2)
        else:
            old_user2 = MyUser.objects.get(coll_email=request.POST.get('coll__email'))
            print(old_user2)
        if old_user is not None and old_user.is_active is False:
            old_user.delete()
        elif old_user2 is not None and old_user2.is_active is False and old_user is None:
            old_user2.delete()
        elif (old_user is not None and old_user.is_active is True) or (old_user2 is not None and old_user2.is_active is True):
            args = {
                'error': "You have already registered and your email is verified too. Enter email to reset your password."
            }
            return render(request, "user/reset_password.html", args)
        userform = UserRegistration(request.POST, request.FILES)
        roleform = RoleMasterForm(request.POST)
        if userform.is_valid() and roleform.is_valid():
            user = userform.save(commit=False)
            password = userform.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False
            user.full_name = user.first_name + " " + user.last_name
            user.save()
            roleassign = RoleAssignment()
            roleassign.user = user
            roleassign.role = roleform.cleaned_data.get('role')
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
            send_email(to_email_one, mail_subject, message)
            send_email(to_email_two, mail_subject, message2)
            return render(request, 'user/AccountConfirm.html')

            #       group = Group.objects.get(name='groupname')
            #      user.groups.add(group)
            # login(request, user, backend='social_core.backends.google.GoogleOAuth2')
            # else:
            # print(userform.errors)
            # print(roleform.errors)
    else:
        userform = UserRegistration()
        roleform = RoleMasterForm
    selected_roles = RoleMaster.objects.all().order_by('name')
    # print(selected_roles)
    return render(request, 'events/RegisterHead.html',
                  {'userform': userform, 'roleform': roleform, 'roles': Roles, 'depts': dept, 'colleges': coll,
                   'years': year, 'categories': role_categories, 'selected_roles': selected_roles,'events': events})


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
    if user is not None:
        if user.token1 == token:
            user.token1 = None
        if user.token2 == token:
            user.token2 = None
        if user.token1 is None and user.token2 is None:
            user.is_active = True
            user.is_staff = True
        user.save()
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        # return redirect('home')
        return render(request, 'user/accountActivate.html')
    else:
        return HttpResponse('You have already confirmed your email id. Activation link is invalid!')


def participant_event_register(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        eventId = request.POST.get('event_id')
        if useremail != "":
            otp = random.randint(100000, 999999)
            message = render_to_string('user/OTP.html' ,{
                'otp': otp
            })
            mail_subject = 'OTP for email verification.'
            request.session['otp'] = otp
            send_email(useremail, mail_subject, message)

            return render(request, 'events/participantEventRegister.html',
                          {'email': useremail, 'event_id': eventId, 'btndisable': True})
        else:
            return render(request, 'events/participantEventRegister.html', {'event_id': eventId, 'email': useremail})
    if request.method == 'GET':
        event_id = request.GET.get('event_id')
        return render(request, 'events/participantEventRegister.html', {'event_id': event_id})


def verifyOTP(request):
    if request.method == 'POST':
        userEmail = request.POST.get('useremail')
        eventId = request.POST.get('event_id')
        event = EventMaster.objects.get(pk=eventId)
        otpEntered = request.POST.get('otp')
        originalotp = str(request.session.get('otp'))
        # print(originalotp)
        # print("original otp", originalotp)
        if originalotp != otpEntered or len(originalotp) < 6:
            error = "Invalid OTP"
            return render(request, 'events/participantEventRegister.html',
                          {'error': error, 'event_id': eventId, 'email': userEmail})

        else:
            request.session['otp'] = ""
            coll = College.objects.all().order_by('name')
            if MyUser.objects.filter(email=userEmail).count() == 0:
                if MyUser.objects.filter(coll_email=userEmail).count() == 0:
                    ifuser = None

                else:
                    ifuser = MyUser.objects.get(coll_email=userEmail)
            else:
                ifuser = MyUser.objects.get(email=userEmail)
            readm = "readonly"
            return render(request, 'events/participantDetails.html',
                          {'event': event, 'colleges': coll, 'email_participant': userEmail, 'present_user': ifuser,
                           'readm': readm})


def participant_details(request):
    if request.method == "POST":

        participant_email = request.POST.get('email')
        event_id = request.POST.get('event_id')
        # print(event_id)
        # print("POst mail:", participant_email)
        form = PaymentForm(request.POST)
        coll = College.objects.all().order_by('name')

        if MyUser.objects.filter(email=participant_email).count() == 0:
            if MyUser.objects.filter(coll_email=participant_email).count() == 0:
                ifuser = None

            else:
                ifuser = MyUser.objects.get(coll_email=participant_email)
        else:
            ifuser = MyUser.objects.get(email=participant_email)

        event_new = EventMaster.objects.get(pk=event_id)
        if len(request.POST.get('user_phone')) < 10:
            error = "Invalid mobile number"
            return render(request, 'events/participantDetails.html',
                          {'event': event_new, 'colleges': coll, 'email_participant': participant_email,
                           'present_user': ifuser, 'error': error})
        if request.POST.get('button_state') == "on":
            pass
        else:
            error = "You need to accept"
            return render(request, 'events/participantDetails.html',
                          {'event': event_new, 'colleges': coll, 'email_participant': participant_email,
                           'present_user': ifuser, 'error': error})
        if form.is_valid():
            if ifuser is None:
                user = form.save(commit=False)
                password = None
                user.set_password = password
                user.username = participant_email
                user.is_active = False
                user.save()

            # print("name", event_new.event_name)
            user = MyUser.objects.get(email=participant_email)
            if request.POST.get('card'):
                # print("towards Payment")
                current_site = get_current_site(request)
                # print("here", current_site.domain)
                refer = request.POST.get('refer')
                try:
                    referral = MyUser.objects.get(username=refer)
                except(IntegrityError, ObjectDoesNotExist):
                    refer = "0"

                insta = InstamojoCredential.objects.latest('pk')
                # print(insta.key, insta.token, insta.salt)
                api = Instamojo(api_key=insta.key,
                                auth_token=insta.token, )
                head = 'http://'
                if settings.USE_HTTPS:
                    head = 'https://'

                response = api.payment_request_create(
                    amount=event_new.entry_fee,
                    purpose=event_new.event_name,
                    send_email=False,
                    send_sms=False,
                    email=user.email,
                    phone=user.user_phone,
                    buyer_name=user.first_name + " " + user.last_name,
                    # redirect_url="http://127.0.0.1:8000/success?eid=" + event_id + "&ref=" + str(refer)
                    redirect_url=head + current_site.domain + "/" + "success?eid=" + event_id + "&ref=" + str(
                        refer) + "success?eid=" + event_id + "&ref=" + str(refer)

                )
                # print the long URL of the payment request.
                # print(response)
                # print(response['payment_request']['longurl'])
                # print the unique ID(or payment request ID)
                # print(response['payment_request']['id'])
                # print(response['payment_request']['purpose'])
                # print(response['payment_request']['amount'])
                return redirect(response['payment_request']['longurl'])
            elif request.POST.get('cash'):
                cashpayment(request, event_new, user)
                teams = reversed(Team.objects.filter(user=user).reverse())
                # print("CAAAAA")
                return render(request, 'user/registeredEvents.html', {'teams': teams})
        else:
            # print(form.errors)
            error = form.errors
            return render(request, 'events/participantDetails.html',
                          {'event': event_new, 'colleges': coll, 'email_participant': participant_email,
                           'present_user': ifuser, 'error': error})
    else:
        return redirect('/')


@staff_user
def cashpayment(request, event_new, user):
    id = ""
    flag = 0
    while flag == 0:
        try:
            id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            transaction = Transaction.objects.get(transaction_id=id)
        except(IntegrityError, ObjectDoesNotExist):
            flag = 1
    receipt = Receipt()
    team = Team()
    transaction = Transaction()
    receipt.name = user.first_name + " " + user.last_name
    receipt.event = event_new
    receipt.save()
    team.receipt = receipt
    team.user = user
    team.referral = request.user
    team.save()
    transaction.transaction_id = id
    transaction.transaction_request_id = id
    transaction.instrment_type = "Cash"
    transaction.billing_instrument = "Cash"
    transaction.status = "Cash"
    transaction.receipt = receipt
    transaction.date = datetime.date.today()
    transaction.time = datetime.datetime.now().time()
    transaction.team = team
    transaction.save()
    # Generate QR code if transaction is success full
    if transaction.status == "Cash":
        # print("cashhh")
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        content = "event:" + event_new.event_name + ", user:" + user.username
        qr.add_data(content)
        img = qr.make_image(fill_color="black", back_color="white")
        # img.save(user.username + event.event_name + "png")
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        team.QRcode.save('ticket-filename.jpg', File(thumb_io), save=False)

        # While loop for generating a unique refral code for user
        while True:
            try:
                Refral_Code = ''.join(random.choice(string.ascii_uppercase) for _ in range(3)) + str(
                    random.randint(100, 999))
                Team.objects.get(Refral_Code=Refral_Code)
            except:
                break

        team.Refral_Code = Refral_Code

        team.save()

        mail_subject = 'You have registered for ' + event_new.event_name + ' using cash payment'
        message = render_to_string('events/receiptCashPayment.html', {
            'user': user,
            'event': event_new,
            'team': team,
            'transaction': transaction,
        })
        send_email(user.email, mail_subject, message, [team.QRcode.path])


@staff_user
def Profile(request):
    user = request.user
    if request.method == 'POST':
        if request.method == 'POST' and len(request.FILES) == 1:
            prof_img = request.FILES['prof_img']
            # print(request.FILES['prof_img'])
            user.prof_img = prof_img
        user_phone = request.POST.get('user_phone')
        user.user_phone = user_phone
        user.save()
    return render(request, 'user/userProfile.html')


@staff_user
def registered_events(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'user/registeredEvents.html', {'teams': teams})


def Payment_Details(request):
    return render(request, 'user/paymentDetails.html')


# def cashPayment(request):
#     coll = College.objects.all()
#     year = College_year.objects.all()
#     event_id = request.GET.get('event_id')
#     campaign_name = request.GET.get('userEmail')
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             firstname = form.cleaned_data.get('first_name')
#             username = form.cleaned_data.get('username')
#             password = None
#             user.set_password=password
#             user.is_active=False
#             user.save()
#             receipt = Receipt()
#             receipt.event = EventMaster.objects.get(pk=event_id)
#             receipt.name = firstname
#             team = Team()
#             team.receipt=receipt
#             team.user=user
#             team.referral= campaign_name
#             receipt.save()
#             team.save()
#         else:
#             print(form.errors)
#
#     else:
#         form = PaymentForm()
#         event = EventMaster.objects.get(pk=event_id)
#     return render(request, 'events/cashPayment.html',{'form':form,'event':event,'colleges':coll,'years':year})

def team_details(request):
    event = request.GET.get('event')
    event_choose = EventMaster.objects.get(event_name=event)
    if request.method == 'GET':
        form = TeamDetailsForm()
    if request.method == 'POST':
        form = TeamDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            # else:
            # print(form.errors)

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
        send_email(user.email, mail_subject, message, otp=1)
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

@staff_user
def change_password(request):
    status=True
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        user = authenticate(username = request.user.username, password=old_password)
        if user is not None:
            status = True
            return render(request, 'user/new_password.html', {'status':status})
        else:
            status = False
            messages.error(request,"Invalid Password",{'status':status})

    return render(request, 'user/change-password.html',{'status':status})

def send_username(request):
    status = 0
    if request.method == 'POST':
        user_email = request.POST.get('user-email')
        count = MyUser.objects.filter(email = user_email).count()
        if count:
            user = MyUser.objects.get(email = user_email)
            if user.is_active:
                message = render_to_string('user/username-email-sent.html',
                {
                    'user': user,
                })
                mail_subject = 'Activate your account to continue.'
                to_email = user_email
                send_email(to_email, mail_subject, message)
                status = 1
                return render(request, 'user/send-username.html', {'status': status})
            else:
                status = 3
                return render(request, 'user/send-username.html', {'status': status})
        else:
            status = -1
            return render(request, 'user/send-username.html', {'status': status})
    return render(request, 'user/send-username.html', {'status': status})
# Important Notes:
# to get user role from models
# userget = RoleAssignment.objects.get(user=request.user.id)
#   print (userget.role)


# Volunteer College Date Entry by Campaign Head
@user_Campaign_head
def AddVolunteer(request):
    if request.method == "POST":
        uid = request.POST.get('volunteers')
        cid = request.POST.get('colleges')
        user = MyUser.objects.get(pk=uid)
        college = College.objects.get(pk=cid)
        volunteer = Volunteer()
        volunteer.user = user
        volunteer.college = college
        volunteer.date = request.POST.get('campaignDate')
        volunteer.save()
        volunteerData = Volunteer.objects.all()
        volunteers = []
        roles = RoleAssignment.objects.all()
        for role in roles:
            if role.role.name == "Volunteer":
                volunteers.append(role.user)
                # print(role.user)
        colleges = College.objects.all()
        args = {
            'volunteers': volunteers,
            'colleges': colleges,
            'volunteerData': volunteerData
        }
        return render(request, 'events/campaignVolunteer.html', args)


@staff_user
def ourSponsors(request):
    Sponsors = SponsorMaster.objects.all()
    sponsors=[]
    partners=[]
    for s in Sponsors:
        if 'partner' in s.sponsor_type.lower():
            print(s)
            partners.append(s)
        elif 'sponsor' in s.sponsor_type.lower():
            print(s)
            sponsors.append(s)
    args = {
        'partners':partners,
        'sponsors': sponsors
    }
    return render(request, 'gandharva/ourSponsors.html', args)


@staff_user
def ourTeam(request):
    return render(request, 'gandharva/ourTeam.html')


# upload file view
@staff_user
def files(request):
    glbdoc = Document.objects.get(category=Document_type.objects.get(type="Global"))
    current_doc = fileDocument.objects.filter(user=request.user).order_by("uploaded_at").reverse()
    dictonary = {}
    juniors = AssignSub.objects.filter(rootuser=request.user)
    for junior in juniors:
        doc_list = fileDocument.objects.filter(user=junior.subuser).order_by("uploaded_at").reverse()
        dictonary[junior.subuser] = doc_list

    if request.method == 'POST':
        form = fileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.fname = request.FILES['document'].name
            # print(request.FILES['document'].name)
            f.save()
            return render(request, 'events/fileExplorer.html', {
                'form': fileForm,
                'dict': dictonary,
                'documents': current_doc,
                'global': glbdoc

            })
    else:
        form = fileForm()
    return render(request, 'events/fileExplorer.html', {
        'form': form,
        'dict': dictonary,
        'documents': current_doc,
        'global': glbdoc
    })


# Campaign Head Method
@user_Campaign_head
def campaign(request):
    if request.method == "POST":
        check = request.POST.get('criteria')
        # volunteer wise
        if check == "0":
            volunteers = []
            transactions = Transaction.objects.all()
            for transaction in transactions:
                if transaction.status == "Credit" or "Cash":

                    try:
                        ref = transaction.team.referral.username
                        name = MyUser.objects.get(username=ref)
                    except Exception:
                        continue
                    c = 0
                    for i in range(len(volunteers)):
                        if volunteers[i].username == ref:
                            c = 1
                            volunteers[i].count = volunteers[i].count + 1
                            break
                    if c == 0:
                        v = Volunteerwise()
                        v.username = ref
                        v.name = name
                        v.count = 1
                        volunteers.append(v)
            args = {

                'volunteers': volunteers,
            }
            # print("volunteer")
            # print(volunteers)
            return render(request, 'events/campaigningData.html', args)
        elif check == "1":
            events = []
            transactions = Transaction.objects.all()
            for transaction in transactions:
                if transaction.status == "Credit" or transaction.status == "Cash":
                    event = transaction.team.receipt.event
                    c = 0
                    for i in range(len(events)):
                        if events[i].event_id == event.event_id:
                            c = 1
                            events[i].count = events[i].count + 1
                            break
                    if c == 0:
                        e = Eventwise()
                        e.event_id = event.event_id
                        e.event_name = event.event_name
                        e.count = 1
                        events.append(e)
                args = {
                    'events': events,
                }
                # print("")
                # print(events)
            return render(request, 'events/campaigningData.html', args)
        elif check == "2":
            colleges = []
            transactions = Transaction.objects.all()
            for transaction in transactions:
                if transaction.status == "Credit" or transaction.status == "Cash":
                    college = transaction.team.user.user_coll
                    c = 0
                    for i in range(len(colleges)):
                        if colleges[i].name == college.name:
                            c = 1
                            colleges[i].count = colleges[i].count + 1
                            break
                    if c == 0:
                        c = Collegewise()
                        c.name = college.name
                        c.count = 1
                        colleges.append(c)
                args = {
                    'colleges': colleges,
                }
                # print("")
                # print(colleges)
            return render(request, 'events/campaigningData.html', args)

        elif check == "3":
            volunteers = []
            roles = RoleAssignment.objects.all()
            for role in roles:
                if role.role.name == "Volunteer":
                    volunteers.append(role.user)
                    # print(role.user)
            colleges = College.objects.all()
            volunteerData = Volunteer.objects.all()
            args = {
                'volunteers': volunteers,
                'colleges': colleges,
                'volunteerData': volunteerData
            }
            return render(request, 'events/campaignVolunteer.html', args)

    else:
        return render(request, 'events/campaignHead.html')


def terms(request):
    terms = TermsConditons.objects.all()

    return render(request, 'gandharva/terms-and-conditions.html', {'terms': terms})


def policy(request):
    policy = TermsConditons.objects.all()

    return render(request, 'gandharva/privacy-policy.html', {'policys': policy})


class Volunteerwise:
    username = ""
    name = ""
    count = 0


class Eventwise:
    event_id = 0
    event_name = ""
    count = 0


class Collegewise:
    cid = ""
    name = ""
    count = 0
