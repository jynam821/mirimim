from django.db import models


class User(models.Model):
    name = models.CharField(null=True, max_length=50)
    email = models.CharField(max_length=50, primary_key=True)
    s_id = models.CharField(null=True, max_length=10)#학생=학번 선생님=담당반 과목코드 T ex)331T
    password = models.CharField(null=True, max_length=255)
    active = models.BooleanField(default=False)
