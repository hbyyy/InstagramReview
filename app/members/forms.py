from django import forms
from django.contrib.auth import authenticate

from members.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '아이디'
        }
    ))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호',
        }
    ))

    def clean_username(self):
        username_check = User.objects.filter(username=self.cleaned_data['username']).exists()
        if username_check is True:
            return self.cleaned_data['username']
        else:
            raise forms.ValidationError('존재하지 않는 아이디입니다')

    def clean_password(self):
        if self.errors:
            return
        else:
            password_check = User.objects.get(
                username=self.cleaned_data['username']
            ).check_password(self.cleaned_data['password'])
            if password_check is True:
                return self.cleaned_data['password']
            else:
                raise forms.ValidationError('비밀번호가 틀렸습니다.')

    def authenticate(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        return authenticate(request, username=username, password=password)


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': '이메일을 입력하세요'
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '아이디를 입력하세요'
        }
    ))
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '이름을 입력하세요'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        }
    ))

    def clean_username(self):
        username_check = User.objects.filter(username=self.cleaned_data['username']).exists()

        if username_check is True:
            raise forms.ValidationError('이미 사용중인 아이디입니다')
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        email_check = User.objects.filter(email=self.cleaned_data['email']).exists()

        if email_check is True:
            raise forms.ValidationError('이미 사용중인 Email입니다')
        else:
            return self.cleaned_data['email']

    def save(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']

        return User.objects.create_user(
            email=email,
            username=username,
            name=name,
            password=password
        )
