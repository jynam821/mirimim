from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from account.models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import uri_to_iri

def get_user(request):
    try:
        print("get_user")
        email=request.session['email']
        user = User.objects.get(email = email)
        print("user", user, "user")
    except:
        print('except')
        return None
    return user


def index(request):
    user = get_user(request)
    if user == None:
        return HttpResponse("<script>alert('로그인 후 이용해주세요.');location.href = '/account/signin';</script>")
    try:
        if user == None:
            return HttpResponse("<script>alert('로그인 후 이용해주세요.');location.href= '/account/signin';</script>")
        today = datetime.today().strftime("%Y%m%d")
        lists = Notice.objects.all()
        notices = []
        for notice in lists:
            if notice.submit_at != None:
                if notice.submit_at.strftime("%Y%m%d") == today:
                    notices.append(notice)
        return render(request, 'home/index.html', {'user':user,'notices':notices,'today':today})
    except: 
        return HttpResponse("<script>alert('로그인 후 이용해주세요.');location.href = '/account/signin';</script>")


def ban(request):
    user = get_user(request)
    print("ban", user)
    notices = Notice.objects.filter(Q(classroom_id=int(user.s_id[:2])) | Q(scope=-1)).order_by("-updated_at")
    submits = Assignment.objects.filter(email = user.email)
    today = datetime.today().strftime("%Y%m%d")
    return render(request, 'home/ban.html',{'user':user,'notices':notices,'today':today, 'submits':submits})
   

@csrf_exempt
def sub(request):
    user = get_user(request)
    print(user.email)
    attend = None
    try:
        if request.method == 'POST':
            num=int(request.POST['num'])
            classroom = get_object_or_404(Classroom, pk=num)
            attend = Attend.objects.create(email=user.email, classroom_id=classroom.classroom_id,class_name = classroom.class_name, teacher= classroom.class_name)
    except:
        return HttpResponse("<script>alert('없는 방번호입니다.다시 한번 확인해주세요.');history.back(-1);</script>")
    attends = Attend.objects.filter(Q(email=user.email)).exclude(classroom_id=int(user.s_id[:2]))
    today = datetime.today().strftime("%Y%m%d")
    return render(request, 'home/sub.html',{'user':user,'attends':attends,'today':today, 'attend':attend})



@csrf_exempt
def add(request):
    user = get_user(request)
    if request.method=='POST':
        classroom_id = int(request.POST['classroom_id'])
        title = request.POST['title']
        content = request.POST['content']
        sa = request.POST['submit_at']
        if sa == "":
            submit_at = None
        else:
            submit_at = "{date} {time}".format(date=sa[:10],time=sa[11:16])
        file_urls = simple_upload(request)
        notice = Notice.objects.create(classroom_id=classroom_id,title = title, email = user.email,s_id = user.s_id, name = user.name, content = content, scope=classroom_id, submit_at = submit_at)
        if file_urls != None:
            for file_url in file_urls:
                File.objects.create(obj_code=0,obj_id=notice.notice_id,file_url=file_url)
        return HttpResponse("<script>alert('공지가 성공적으로 작성되었습니다.'); history.go(-2);</script>")
    attends = Attend.objects.filter(email = user.email)
    return render(request, 'home/add.html',{'user':user,'attends':attends})


@csrf_exempt
def update(request,*args, **kwargs):
    user = get_user(request)
    if request.method=='POST':
        classroom_id = int(request.POST['classroom_id'])
        title = request.POST['title']
        content = request.POST['content']
        sa = request.POST['submit_at']
        if sa == "":
            submit_at = None
        else:
            submit_at = "{date} {time}".format(date=sa[:10],time=sa[11:16])
        notice = Notice.objects.filter(notice_id = kwargs['pk']).update(classroom_id=classroom_id,title = title, email = user.email,s_id = user.s_id, name = user.name, content = content, scope=classroom_id, submit_at = submit_at)
        url = '/detail/'+str(kwargs['pk'])+'/'
        return redirect(url)
    user = get_user(request)
    notice = get_object_or_404(Notice, pk=kwargs['pk'])
    files = File.objects.filter(obj_code=0,obj_id=kwargs['pk'])
    file_urls=[]
    for file in files:
        file_urls.append(uri_to_iri(file.file_url))
    print(file_urls)
    attends = Attend.objects.filter(email = user.email)
    if notice.submit_at != None:
        notice.submit_at =notice.submit_at.strftime("%Y-%m-%d")+"T"+notice.submit_at.strftime("%H:%M")
    return render(request, 'home/update.html',{'user':user,'attends':attends, 'notice':notice, 'files':file_urls})


def simple_upload(request):
    url_list = []
    try:
        if request.method == 'POST' and request.FILES['upload_file']:
            print("if files upload")
            myfiles = request.FILES.getlist('upload_file')
            for myfile in myfiles:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                url_list.append(uploaded_file_url)
            return url_list
    except:
        print("except error")
        return None


def get_file(request):
        user = get_user(request)
        return user.file_url


def submit(request,*args, **kwargs):
    user = get_user(request)
    notice = get_object_or_404(Notice, pk=kwargs['pk'])
    if request.method=='POST':
        assignment = Assignment.objects.create(classroom_id=notice.classroom_id,notice_id = notice.notice_id, email = user.email,s_id = user.s_id, name = user.name)
        file_urls = simple_upload(request)
        if file_urls != None:
            for file_url in file_urls:
                File.objects.create(obj_code=1,obj_id=assignment.assignment_id,file_url=file_url)
        return redirect('/my_submitlist')
    return render(request,'home/submit.html',{"user":user,"notice":notice})

def submitlist(request):
    user = get_user(request)
    submitlist = Assignment.objects.filter(email=user.email)
    notices = Notice.objects.all()
    return render(request, 'home/submitlists.html',{"submitlist":submitlist,"notices":notices})

def submitlists(request,*args, **kwargs):
    user = get_user(request)
    submitlist = Assignment.objects.filter(notice_id=kwargs['pk'])
    notices = Notice.objects.all()
    return render(request, 'home/submitlists.html',{"submitlist":submitlist,"notices":notices})

def submit_detail(request,*args, **kwargs):
    return render(request,'home/submit_detail.html')

@csrf_exempt
def addclass(request):
    user = get_user(request)
    if request.method == 'POST':
        sbj_code = int(request.POST['subject'])
        class_name = request.POST['title']
        last = Classroom.objects.all().order_by('-classroom_id').first()
        classroom = Classroom.objects.create(classroom_id = last.classroom_id+1,sbj_code=sbj_code, class_name=class_name, teacher=user.name)
        Attend.objects.create(classroom_id=classroom.classroom_id,email=user.email, class_name=classroom.class_name, teacher = classroom.teacher)
        return HttpResponse("<script>alert('클래스가 성공적으로 추가되었습니다. 방번호는 "+ str(classroom.classroom_id)+"입니다.');location.href = '/sub';</script>")
    subjects = Subject.objects.all()
    return render(request,'home/addclass.html',{'subjects':subjects})

class SubmitDetailView(DetailView):
    model = Assignment
    def get(self, request, *args, **kwargs):
        file_urls = []
        user = get_user(request)
        submit = get_object_or_404(Assignment, pk=kwargs['pk'])
        notice = get_object_or_404(Notice, pk=submit.notice_id)
        print(notice.title)
        files = File.objects.filter(obj_code=1,obj_id=kwargs['pk'])
        for file in files:
            file_urls.append(uri_to_iri(file.file_url))
        context = {'notice': notice,'files': files, 'submit':submit, 'user':user,'file_urls':file_urls}
        return render(request, 'home/submit_detail.html', context)


@csrf_exempt
def submit_update(request,*args, **kwargs):
    user = get_user(request)
    submit = get_object_or_404(Assignment,  pk=kwargs['pk'])
    notice = get_object_or_404(Notice, pk=submit.notice_id)
    if request.method=='POST':
        Assignment.objects.filter(pk=submit.assignment_id).update(updated_at=datetime.now())
        File.objects.filter(obj_code=1,obj_id=submit.assignment_id).delete()
        file_urls = simple_upload(request)
        if file_urls != None:
            for file_url in file_urls:
                File.objects.create(obj_code=1,obj_id=submit.assignment_id,file_url=file_url)
        return redirect('/my_submitlist')
    return render(request,'home/submit.html',{"user":user,"notice":notice})

def class_index(request,*args, **kwargs):
    user = get_user(request)
    classroom = get_object_or_404(Classroom, classroom_id=kwargs['pk'])
    notices = Notice.objects.filter((Q(classroom_id=kwargs['pk']) | Q(scope=-1)))
    return render(request,'home/class_index.html',{'user':user,'notices':notices,'classroom':classroom})

class NoticeDetailView(DetailView):
    model = Notice
    def get(self, request, *args, **kwargs):
        file_urls = []
        user = get_user(request)
        notice = get_object_or_404(Notice, pk=kwargs['pk'])
        attends = Attend.objects.filter(email = user.email)
        files = File.objects.filter(obj_code=0,obj_id=kwargs['pk'])
        for file in files:
            file_urls.append(uri_to_iri(file.file_url))
        context = {'notice': notice,'files': files, 'attends':attends, 'user':user,'file_urls':file_urls}
        return render(request, 'home/notice_detail.html', context)
        

class NoticeDeleteView(DeleteView):
    model = Notice
    success_url = reverse_lazy('home:submitlist')

def notice_delete(request, *args, **kwarg):
    notice = get_object_or_404(Notice, pk=kwarg['pk'])
    class_id = notice.classroom_id
    Notice.objects.filter(pk = kwarg['pk']).delete()
    if class_id >36:
        return redirect('/class_index/{}/'.format(class_id))
    else:
        return redirect('/ban/')

class SubmitDeleteView(DeleteView):
    model = Assignment
    success_url = reverse_lazy('home:submitlist')

@csrf_exempt
def refer(request, *args, **kwarg):
    user = get_user(request)
    if request.method == 'POST':
        content = request.POST['content']
        Refer.objects.create(email=user.email,name=user.name, content=content,notice_id=kwarg['pk'])
    refers = Refer.objects.filter(notice_id=kwarg['pk']).order_by('created_at')
    print(refers)
    return render(request,'home/refer.html',{'refers':refers})
    
