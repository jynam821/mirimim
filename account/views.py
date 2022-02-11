from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import auth
from .models import *
from home.models import *


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']+'@e-mirim.hs.kr'
        users = User.objects.filter(email = email)
        for user in users:
            if user.email == email:
                return HttpResponse("<script>alert(존재하는 이메일입니다.);</script>")
        password = request.POST['password']
        grade = request.POST['grade']
        ban = request.POST['ban']
        if request.POST['chk']=="0":
            number = request.POST['student_number']
        else:
            number = request.POST['teacher_number']
        s_id = grade+ban+number
        if s_id[:2]!="00":
            Attend.objects.create(classroom_id = s_id[:2],email = email)
        User.objects.create(name = name, email=email, password=password, s_id=s_id)
        return redirect('/account/signin')
    subjects = Subject.objects.all()
    return render(request, 'account/signup.html',{'subjects':subjects})

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']+'@e-mirim.hs.kr'
        password = request.POST['password']
        users = User.objects.filter(email = email, password=password)
        for user in users:
            if user.email == email and user.password == password:
                request.session['email']=email
                return redirect('../../')
        return HttpResponse("<script>alert('회원정보가 잘못되었습니다.');history.back();</script>")
    return render(request, 'account/signin.html')

def logout(request):
    request.session.clear()
    return redirect('/account/signin/')