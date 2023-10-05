from django import forms
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from .models import Profile, UserAccount


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    first_name= forms.CharField(required= True)
    last_name= forms.CharField(required= True)

    class Meta:
        model = UserAccount
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 3, "placeholder": "Description about yourself", "required": False}))
    dob = forms.DateField(widget=forms.DateInput({
        "type": "date"
    }))
    national_id = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "05121587Y05"}
    ))
    address = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "3155 Wood Broke North "}
    ))
    city = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Bindura"}
    ))
   

    class Meta:
        model = Profile
        fields = ["dob", "national_id", "gender",
                  "marital_status", "bio", "address", "city", "nationality", "thumbnail"]
        widgets = {"nationality": CountrySelectWidget()}


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
