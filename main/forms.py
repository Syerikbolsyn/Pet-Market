from django import forms
from .models import *
from django.core.validators import MinLengthValidator


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, validators=[MinLengthValidator(8)])
    email = forms.CharField(widget=forms.EmailInput())
    phone = forms.CharField(widget=forms.TextInput(), max_length=18)

    class Meta:
        model = UserC
        fields = ["username", "password", "email", 'first_name', 'last_name', 'phone']

    def clean_username(self):
        usname = self.cleaned_data.get("username")
        if User.objects.filter(username=usname).exists():
            raise forms.ValidationError("User this username already exists")

        return usname

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class PetForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget = forms.FileInput(attrs={
        "class" : "form-control",
        "multiple" : True
    }) )
    class Meta:
        model = Pet
        fields = ["name", "price", "gender", "birthday_date", "city", "image",
                  "comment", "type", "breed"]
        widgets = {
            "name" : forms.TextInput(attrs = {
                "class" : "form-control",
                "placeholder" : "Введите имя питомца"
            }),
            "price" : forms.NumberInput(attrs = {
                "class" : "form-control",
                "placeholder" : "Укажите цену"
            }),
            "gender" : forms.Select (attrs = {
                "class" : "form-control",
                "placeholder": "Пол"
            }),
            "birthday_date": forms.DateInput(attrs = {
                "class": "form-control",
                "placeholder": "Дата рождения"

            }),
            "city": forms.Select(attrs = {
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput (attrs = {
                "class": "form-control",
                "placeholder": "img"
            }),
            "comment": forms.Textarea(attrs = {
                "class": "form-control",
                "placeholder": "Введите описание"
            }),
            "type": forms.Select(attrs = {
                "class": "form-control"
            }),
            "breed": forms.Select(attrs = {
                "class": "form-control"
            })

        }

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Электронный адрес"
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if UserC.objects.filter(user__email=e).exists():
            pass
        else :
            raise forms.ValidationError(
                "Аккаунт не найден. "
                "Повторите попытку или зарегистрируйтесь"
            )
        return e
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password", min_length=8, validators=[MinLengthValidator(8)] )

    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password", min_length=8,validators=[MinLengthValidator(8)] )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password





