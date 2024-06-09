from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Логин"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': "Пароль"}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': "Повтор пароля"}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Почта"}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Имя"}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Фамилия"}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Неправильное имя пользователя или пароль. Пожалуйста, проверьте правильность ввода."
        ),
        'inactive': ("Этот аккаунт неактивен."),
    }