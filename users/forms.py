import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordMixin


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'validate teal-text', 'placeholder': ' Имя пользователя'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate teal-text', 'placeholder': ' Пароль'}),
        label='Пароль'
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'teal-text', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'teal-text', 'placeholder': 'Повтор пароля'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email',
                  'first_name', 'last_name',
                  'date_birth', 'photo',
                  'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'teal-text', 'placeholder': 'E-mail'}),
            'first_name': forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Ваша фамилия'}),
            'date_birth': forms.TextInput(attrs={'class': 'teal-text datepicker', 'placeholder': 'Дата рождения'}),
            'photo': forms.FileInput(attrs={'class': 'teal-text', 'placeholder': 'Фото', 'name': 'photo'}),
        }
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_birth': 'Дата рождения',
            'photo': 'Фотография',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой e-mail уже существует")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Логин'}))
    email = forms.EmailField(disabled=True, label='E-mail', widget=forms.EmailInput(attrs={'class': 'teal-text', 'placeholder': 'E-mail'}))
    first_name = forms.CharField(required=False, label='Имя', widget=forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Ваше имя'}))
    last_name = forms.CharField(required=False, label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'teal-text', 'placeholder': 'Ваша фамилия'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_birth']
        labels = {
            'photo': 'Фото',
        }
        widgets = {
            'date_birth': forms.TextInput(attrs={'class': 'teal-text datepicker', 'placeholder': 'Дата рождения'}),
            'photo': forms.FileInput(attrs={'class': 'teal-text', 'placeholder': 'Фото'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'teal-text', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'teal-text', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label='Подтверждение пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'teal-text', 'placeholder': 'Повтор пароля'}))


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='E-mail',
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "teal-text", "placeholder": "E-mail"}),
    )


class SetPasswordForm(SetPasswordMixin, forms.Form):

    new_password1, new_password2 = SetPasswordMixin.create_password_fields(
        label1="New password", label2="New password confirmationDD",
    )


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def get_initial_for_field(self, field, field_name):
        field.widget.attrs['placeholder'] = 'Новый пароль' if field_name == "new_password1" else "Повтор нового пароля"
        return super().get_initial_for_field(field, field_name)


    def clean(self):
        self.validate_passwords("new_password1", "new_password2")
        self.validate_password_for_user(self.user, "new_password2")
        return super().clean()

    def save(self, commit=True):
        return self.set_password_and_save(self.user, "new_password1", commit=commit)
