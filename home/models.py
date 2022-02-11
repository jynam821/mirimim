from django.db import models


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    classroom_id = models.IntegerField(blank=False, default=-1)
    email = models.CharField(null=True, max_length=50)
    s_id = models.CharField(null=True, max_length=10)
    name = models.CharField(null=True, max_length=50)
    title = models.CharField(null=True, max_length=50)
    content = models.TextField(null=True, max_length=500)
    scope = models.IntegerField(blank=True, default=-1)
    submit_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Assignment(models.Model): #과제 제출
    assignment_id = models.AutoField(primary_key=True)
    classroom_id = models.IntegerField(blank=False, default=-1)
    notice_id = models.IntegerField(blank=False, default=-1)
    email = models.CharField(null=True, max_length=50)
    s_id = models.CharField(null=True, max_length=10)
    name = models.CharField(null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class File(models.Model):#다중 file 저장을 위해 따로
    file_id = models.AutoField(primary_key=True)
    obj_code = models.BooleanField(default=False) #0은 notice, 1은 assignment
    obj_id = models.IntegerField() #assignment_id, notice_id
    file_url = models.CharField(null=True, max_length=100)

class Subject(models.Model): #과목코드
    sbj_code = models.IntegerField()
    sbj_name = models.CharField(null=True, max_length=50)

class Classroom(models.Model): #과목별 선생님들이 추가하는
    classroom_id = models.IntegerField(primary_key=True)
    sbj_code = models.IntegerField(null=True)
    class_name = models.CharField(null=True, max_length=50)
    teacher = models.CharField(null=True, max_length=10)

class Attend(models.Model):
    classroom_id = models.IntegerField()
    email = models.CharField(null=True, max_length=50)
    class_name = models.CharField(null=True, max_length=50)
    teacher = models.CharField(null=True, max_length=50)

class Refer(models.Model):
    email = models.CharField(max_length=50)
    refer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notice_id =models.IntegerField(null=True)


try:
    for i in range(1,4):
        for j in range(1,7):
            classroom_id = int(str(i)+str(j))
            class_name = "{}-{}".format(i,j)
            teacher = "ㅇㅇㅇ"
            Classroom.objects.create(classroom_id=classroom_id,class_name=class_name,teacher=teacher)
except:
    print("이미 1-1~3-6까지 있음")