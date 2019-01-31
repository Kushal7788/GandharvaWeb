from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.


# Use this table to store college name for Campaigning.
class College(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class College_year(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


# model for Department
class Department(models.Model):
    dep_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    img = models.CharField(max_length=200)
    link_to = models.CharField(max_length=200)
    banner_src = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


# Abstract User , it is the extension of the base User model which can be customized
class MyUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    coll_email = models.EmailField(max_length=100, blank=True)
    user_coll = models.ForeignKey(College, on_delete=models.PROTECT, blank=True, null=True)
    user_year = models.ForeignKey(College_year, on_delete=models.PROTECT, null=True, blank=True)
    user_dept = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    prof_img = models.ImageField(blank=True)
    user_phone = models.CharField(max_length=10,blank=True)
    count = models.IntegerField(default=0, null=True)
    token1 = models.CharField(max_length=100, null=True)
    token2 = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username


# RoleMaster contains all the vaarious roles of users
class RoleMaster(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# RoleAssignment assigns the roles to the user
class RoleAssignment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleMaster, on_delete=models.PROTECT)

    def __int__(self):
        return self.role.name


# EventMaster to handle the events section
class EventMaster(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=100)
    num_of_winners = models.IntegerField()
    team_size = models.IntegerField()
    entry_fee = models.IntegerField()
    objective = models.TextField(max_length=1000, blank=True)
    rounds = models.TextField(max_length=10000, blank=True)
    rules = models.TextField(max_length=100000, blank=True)
    container_src = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=40,blank=True)
    timings = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.event_name


# links the events with the departments
class EventDepartment(models.Model):
    event = models.ForeignKey(EventMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.event_name


# sponsors model
class SponsorMaster(models.Model):
    sponsor_name = models.CharField(max_length=30)
    sponsor_logo = models.CharField(max_length=200)
    sponsor_info = models.CharField(max_length=200, default='No Info. Available')
    sponsor_type = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.sponsor_name


# contains media for front-end
class Carousel(models.Model):
    src = models.CharField(max_length=200)


# ContactUs contains fields for user Services to contact to admin (Foreign Key to Dept)
class ContactUs(models.Model):
    class Meta:
        verbose_name_plural = "Contact Us"

    user_name = models.CharField(max_length=30)
    user_id = models.EmailField()
    category = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    user_message = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name


# used for all data on home page
class GandharvaHome(models.Model):
    title = models.CharField(max_length=100)
    data = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.title


class Receipt(models.Model):
    name=models.CharField(max_length=70,null=True)
    event = models.ForeignKey(EventMaster, on_delete=models.PROTECT)

    def __str__(self):
        return self.event.event_name


class Team(models.Model):
    #team_name = models.CharField(max_length=50)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)

    #def __str__(self):
        #return self.team_name

class Transaction(models.Model):
    transaction_id=models.CharField(max_length=50,unique=True)
    transaction_request_id=models.CharField(max_length=50)
    instrment_type=models.CharField(max_length=50)
    billing_instrument=models.CharField(max_length=70)
    status=models.CharField(max_length=30)
    date=models.DateField()
    time=models.TimeField()
    receipt=models.ForeignKey(Receipt,on_delete=models.CASCADE)


class Document_type(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        ordering = ['type', ]

    def __str__(self):
        return self.type


def path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("documents/" + instance.category.type + "/" + instance.title, ext)
    return filename


class Document(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Document_type, on_delete=models.CASCADE)
    description = models.TextField(max_length=3000, blank=True)
    file = models.FileField(upload_to=path)

    class Meta:
        ordering = ['category', ]

    def __str__(self):
        return 'Category : ' + self.category.type + '/' + self.title
