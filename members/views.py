
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Job, Member
from .forms import Captcha, MemberProfile
import datetime


def members_login(requests):
    if requests.method == 'POST':
        captcha = Captcha(requests.POST)
        if captcha.is_valid():
            user = auth.authenticate(
                username=requests.POST['username'],
                password=requests.POST['password'],
            )
            if user is not None:
                auth.login(requests, user)
                return redirect('members_home')
            else:
                error = 'Incorrect Username or Password'
        else:
            error = 'cAPTCHA Security Authorisation Fail'

        return render(
                requests,
                'members/members_login.html',
                {'error': error, 'captcha': captcha}
        )

    else:
        captcha = Captcha()
        return render(requests, 'members/members_login.html', {'captcha': captcha})


@login_required(login_url="/members/login")
def members_home(requests):

    jobs = Job.objects.all()
    now = datetime.datetime.now()
    return render(requests, 'members/members_home.html', {'jobs': jobs, 'now': now})


@login_required(login_url="/members/login")
def profile(requests):

    if requests.method == 'POST':
        user = requests.user
        response = {
            'captcha_return': False,
            'response': False,
        }
        captcha = Captcha(requests.POST)
        if captcha.is_valid():
            response['captcha_return'] = True
            form = MemberProfile(requests.POST)
            if form.is_valid():
                session_user = User.objects.get(username=user)
                session_user.first_name = form.cleaned_data['first_name']
                session_user.last_name = form.cleaned_data['last_name']
                session_user.email = form.cleaned_data['email']
                session_user.member.nickname = form.cleaned_data['nickname']
                session_user.member.phone = form.cleaned_data['phone']
                session_user.member.sector = int(form.cleaned_data['sector'])
                session_user.member.level = int(form.cleaned_data['level'])
                session_user.member.years = years = int(form.cleaned_data['years'])

                # score equation
                multi_p = 0
                for i in range(3, years, 3):
                    multi_p += 1
                score = session_user.member.sector*session_user.member.level+24*multi_p
                session_user.member.score = score
                # score equation end

                session_user.member.bio = form.cleaned_data['bio']
                session_user.save()
                response['response'] = True

        response['captcha'] = captcha
        return render(requests, 'members/profile_response.html', response)

    captcha = Captcha()
    session_user = requests.user
    user_dic = dict()
    for field in [
        'first_name', 'last_name',
        'nickname', 'email', 'phone'
    ]:
        if field in ['first_name', 'last_name', 'email']:
            field_value = getattr(session_user, field)
        else:
            field_value = getattr(session_user.member, field)

        if field_value:
            user_dic[field] = f'value="{field_value}"'
        else:
            user_dic[field] = ''

    user_dic['sector'] = session_user.member.sector
    user_dic['sector_value'], user_dic['sector'] = [
        i for i in Member.SECTORS if i[0] == user_dic['sector']
    ][0]
    user_dic['level'] = session_user.member.level
    user_dic['level_value'], user_dic['level'] = [
        i for i in Member.LEVELS if i[0] == user_dic['level']
    ][0]
    user_dic['years'] = session_user.member.years
    user_dic['years_range'] = range(1, 41)
    user_dic['username'] = session_user.username
    user_dic['bio'] = session_user.member.bio

    return render(
        requests,
        'members/member_profile.html',
        {'captcha': captcha, 'user': user_dic},
    )


def logout(requests):
    if requests.method == 'POST':
        auth.logout(requests)
        return redirect('members_login')
    else:
        pass
