from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm

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
    if request.user.is_authenticated is True:
        return redirect('posts:post_list')

    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post_list')

    else:
        form = SignupForm()

    context = {
        'signup_form': form
    }
    return render(request, 'members/signup.html', context)
