from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.models import User

# 장고 기본유저나 Custom
from members.forms import LoginForm

User = get_user_model()


def login_view(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = LoginForm()

    context = {
        'login_form': form
    }
    return render(request, 'members/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('members:login')


def signup_view(request):

    username = request.POST['username']
    email = request.POST['email']
    name = request.POST['name']
    password = request.POST['password']

    user_check = User.objects.filter(username=username).exists()
    email_check = User.objects.filter(email=email).exists()
    if user_check is True or email_check is True:
        return HttpResponse(f'이미 사용중인 username/email입니다')

    user = User.objects.create_user(username=username, password=password, email=email, name=name)
    login(request, user)
    return redirect('posts:post_list')
