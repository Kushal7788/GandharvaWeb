# include the various features to be used in forms here
from django import forms
from .models import *


class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=100, required=True)
    coll_email = forms.EmailField(max_length=100, required=False)
    user_dept = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    user_year = forms.ModelChoiceField(queryset=College_year.objects.all(), required=False)
    user_coll = forms.ModelChoiceField(queryset=College.objects.all(), required=False)
    user_phone = forms.CharField(max_length=10, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    prof_img = forms.ImageField(required=False);


    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'user_dept', 'user_year', 'user_coll', 'coll_email','first_name','last_name','prof_img']

    def clean(self):
        cleaned_data = super(UserRegistration, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class ContactUsForm(forms.ModelForm):
    user_name = forms.CharField(required=True)
    user_id = forms.EmailField(required=True)
    category = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    user_message = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = ContactUs
        fields = ['user_name', 'user_id', 'user_message', 'category']


class RoleMasterForm(forms.ModelForm):
    class Meta:
        model = Category_assign
        fields = ['role','category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = RoleMaster.objects.none()

class TeamDetailsForm(forms.ModelForm):
    team_name = forms.CharField(required=True)
    user = forms.CharField(required=True)

    class Meta:
        model = ContactUs
        fields = ['team_name', 'user',]