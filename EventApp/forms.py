# include the various features to be used in forms here
from django import forms
from .models import ContactUs, MyUser, Department, RoleMaster, College, College_year


class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=100, required=True)
    coll_email = forms.EmailField(max_length=100, required=False)
    user_dept = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    user_year = forms.ModelChoiceField(queryset=College_year.objects.all(), required=False)
    user_coll = forms.ModelChoiceField(queryset=College.objects.all(), required=False)
    # full_name = forms.CharField(widget=forms.CharField())

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'user_dept', 'user_year', 'user_coll', 'coll_email','full_name']


class ContactUsForm(forms.ModelForm):
    user_name = forms.CharField(required=True)
    user_id = forms.EmailField(required=True)
    category = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    user_message = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = ContactUs
        fields = ['user_name', 'user_id', 'user_message', 'category']


class RoleMasterForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=RoleMaster.objects.all(), required=False)

    class Meta:
        model = RoleMaster
        fields = ['name']
