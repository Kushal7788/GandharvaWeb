from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .validators import validate_file_size


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


def department_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Department_images/" + instance.name, ext)
    return filename


def departmentbanner_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Department_images/" + "Banner_images/" + instance.name, ext)
    return filename


# model for Department
class Department(models.Model):
    rank = models.IntegerField(default=1)
    dep_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    img = models.ImageField(upload_to=department_path, blank=True)
    link_to = models.CharField(max_length=200)
    banner_src = models.ImageField(upload_to=departmentbanner_path, blank=True)

    def __str__(self):
        return self.name


def ourteam_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("OurTeam_images/" + instance.name, ext)
    return filename


def sponsor_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Sponsor_images/" + instance.sponsor_name, ext)
    return filename


def carousel_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Carousel_images/", ext)
    return filename


def rules_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Rules_doc/" + instance.event_name, ext)
    return filename


def prof_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("profile_img/" + instance.username, ext)
    return filename


def QRcode_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("QRcode/" + instance.user.username, ext)
    return filename


# Abstract User , it is the extension of the base User model which can be customized
class MyUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    level = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=100)
    coll_email = models.EmailField(max_length=100, blank=True)
    user_coll = models.ForeignKey(College, on_delete=models.PROTECT, blank=True, null=True)
    user_year = models.ForeignKey(College_year, on_delete=models.PROTECT, null=True, blank=True)
    user_dept = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    prof_img = models.ImageField(upload_to=prof_path, blank=True)
    user_phone = models.CharField(max_length=10, blank=True)
    count = models.IntegerField(default=0, null=True)
    token1 = models.CharField(max_length=100, null=True, blank=True)
    token2 = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.coll_email) + ' ' + str(self.username) + ' ' + str(self.full_name) + ' ' + str(self.first_name)

    # class Meta:
    #     ordering = ['email']


# RoleMaster contains all the vaarious roles of users
class RoleMaster(models.Model):
    name = models.CharField(max_length=50)
    assigned_work = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Role_category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Category_assign(models.Model):
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    category = models.ForeignKey(Role_category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.category + self.role.name


# EventMaster to handle the events section
class EventMaster(models.Model):
    rank = models.IntegerField(default=1)
    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, blank=True)
    num_of_winners = models.IntegerField()
    team_size = models.IntegerField()
    rules_file = models.FileField(upload_to=rules_path, blank=True, default=None)
    entry_fee = models.IntegerField()
    prize = models.TextField(null=True, max_length=1000)
    objective = models.TextField(max_length=1000, blank=True)
    rounds = models.TextField(max_length=10000, blank=True)
    rules = models.TextField(max_length=100000, blank=True)
    container_src = models.ImageField(max_length=500, blank=True)
    location = models.CharField(max_length=40, blank=True)
    timings = models.CharField(max_length=200, blank=True)
    can_register = models.BooleanField(default=True)

    def __str__(self):
        return self.event_name


# RoleAssignment assigns the roles to the user
class RoleAssignment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleMaster, on_delete=models.PROTECT)
    event = models.ForeignKey(EventMaster, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.role.name) + ' ' + str(self.user)
        except:
            return str(self.role.name)

    # class Meta:
    #     ordering = ['role']


class Domain(models.Model):
    domain_name = models.CharField(max_length=100)

    def __str__(self):
        return self.domain_name


# links the events with the departments

class EventDepartment(models.Model):
    event = models.ForeignKey(EventMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.event_name

#sponsor category
class SponsorCategory(models.Model):
    sponsor_category = models.CharField(max_length=30)
    category_rank = models.IntegerField()

    def __str__(self):
        return self.sponsor_category

# sponsors model
class SponsorMaster(models.Model):
    sponsor_name = models.CharField(max_length=30)
    sponsor_logo = models.ImageField(upload_to=sponsor_path, blank=True)
    sponsor_info = models.CharField(max_length=200, default='No Info. Available')
    sponsor_type = models.CharField(max_length=30, blank=True)
    sponsor_link = models.URLField(blank=True)
    sponsor_rank = models.IntegerField(default=1)
    sponsor_category = models.ForeignKey(SponsorCategory, on_delete=models.PROTECT,blank=True,default= None,null=True)
    def __str__(self):
        return self.sponsor_name




# contains media for front-end
class Carousel(models.Model):
    src = models.CharField(max_length=200, blank=True)
    images = models.ImageField(upload_to='Carousel_images/', blank=True)


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
    name = models.CharField(max_length=70, null=True)
    event = models.ForeignKey(EventMaster, on_delete=models.PROTECT)

    def __str__(self):
        return self.event.event_name


class Team(models.Model):
    # team_name = models.CharField(max_length=50)
    QRcode = models.ImageField(upload_to=QRcode_path, blank=True, null=True)
    Refral_Code = models.CharField(max_length=10, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='participant')
    referral = models.ForeignKey(MyUser, on_delete=models.PROTECT, blank=True, related_name='Refral_Volunteer',
                                 null=True)
    ispresent = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_request_id = models.CharField(max_length=50)
    instrment_type = models.CharField(max_length=50)
    billing_instrument = models.CharField(max_length=70)
    status = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.transaction_id


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


def filePath(instance, filename):
    fPath = "Doc/" + instance.user.username + "/" + filename
    return fPath


class fileDocument(models.Model):
    fname = models.CharField(max_length=250)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    document = models.FileField(upload_to=filePath, validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Username : ' + self.user.username


class AssignSub(models.Model):
    rootuser = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='root')
    subuser = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='subordinate')

    def __str__(self):
        return 'Root : ' + str(self.rootuser.first_name) + ' ' + str(self.rootuser.full_name) + ' Sub: ' + str(
            self.subuser.first_name) + ' ' + str(self.subuser.full_name)

    class Meta:
        unique_together = ('rootuser', 'subuser',)


class InstamojoCredential(models.Model):
    key = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    salt = models.CharField(max_length=50)
    payment_url = models.CharField(max_length=60, null=True, blank=True)


class Volunteer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    college = models.ForeignKey(College, on_delete=models.PROTECT)
    date = models.DateField()


class TermsConditons(models.Model):
    terms = models.TextField(max_length=2000)
    policy = models.TextField(max_length=2000)


class SocialMedia(models.Model):
    name = models.CharField(max_length=100, blank=True)
    src = models.CharField(max_length=200)
    cls = models.CharField(max_length=300, blank=True)


class OurTeam(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to=ourteam_path)
    post = models.CharField(max_length=100, default=None)
    rank = models.IntegerField(default=1)
    fb_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    def __str__(self):
        return 'Username : ' + self.name


class HearAboutUs(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
    source = models.CharField(default=None, max_length=200, blank=True)

    def __str__(self):
        return self.user.username + ' -> ' + self.source


def pariwartan(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format("Vishwa-Pariwartan/" + instance.user.email, ext)
    return filename


class Pariwartan(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    doc = models.FileField(upload_to=pariwartan)

    def __str__(self):
        return self.user.username
