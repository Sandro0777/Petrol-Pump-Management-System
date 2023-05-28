from secrets import choice
from django import forms

from gsmsApp import models
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

class SaveUser(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2',)

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class SavePetrol(forms.ModelForm):
    name = forms.CharField(max_length=250, help_text="Enter Petrol Type Name", label="Petrol Type Name")
    description = forms.CharField(widget=forms.Textarea, help_text="Enter Petrol Type Name", label="Petrol Type Description")
    status = forms.ChoiceField(help_text="Select Status", choices=[('1','Active'),('0','Inactive')], label="Status")
    price = forms.CharField(max_length=250, help_text="Enter Petrol Type Price", label="Petrol Type Price")


    class Meta:
        model = models.Petrol
        fields = ('name', 'description', 'status', 'price', )

    def clean_name(self):
        name = self.cleaned_data['name']
        id = self.data['id'] if (self.data['id']).isnumeric() else 0

        try:
            if id > 0:
                petrol = models.Petrol.objects.exclude(id=id).get(name=name, delete_flag = 0)
            else:
                petrol = models.Petrol.objects.get(name=name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError(f"{name} already exists.")


class SaveStock(forms.ModelForm):
    date = forms.CharField(max_length=250, help_text="Date Added", label="Date Added")
    petrol = forms.CharField(max_length=250, help_text="Petrol", label="Petrol")
    volume = forms.CharField(max_length=250, help_text="Stock-In Volume", label="Stock-In Volume")


    class Meta:
        model = models.Stock
        fields = ('petrol', 'volume', 'date',)

    def clean_petrol(self):
        pid = self.cleaned_data['petrol']
        try:
            petrol = models.Petrol.objects.get(id=pid)
            return petrol
        except:
            raise forms.ValidationError(f"Petrol ID is Invalid.")

class SaveSale(forms.ModelForm):
    date = forms.CharField(max_length=250, help_text="Date Added", label="Date Added")
    customer_name = forms.CharField(max_length=250, help_text="Customer", label="Customer")
    petrol = forms.CharField(max_length=250, help_text="Petrol", label="Petrol")
    volume = forms.CharField(max_length=250, help_text="Stock-In Volume", label="Stock-In Volume")
    price = forms.CharField(max_length=250, help_text="Price", label="Price")
    amount = forms.CharField(max_length=250, help_text="Amount", label="Amount")


    class Meta:
        model = models.Sale
        fields = ('petrol', 'volume', 'date', 'price', 'amount', 'customer_name',)

    def clean_petrol(self):
        pid = self.cleaned_data['petrol']
        try:
            petrol = models.Petrol.objects.get(id=pid)
            return petrol
        except:
            raise forms.ValidationError(f"Petrol ID is Invalid.")
