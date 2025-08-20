from operator import mod
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Trainer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MemberProfilePic/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=True)
    age=models.CharField(max_length=20,null=True)
    experience=models.CharField(max_length=30,null=True)
    salary=models.IntegerField(default=0)
    shift=models.CharField(max_length=50,default="")
    status=models.BooleanField(default=False)
    date=models.DateField(auto_now=True,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class Package(models.Model):
    name=models.CharField(max_length=200)
    amount=models.IntegerField()
    duration=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    def __str__(self):
        return self.name+" [ "+str(self.duration)+" ]"


class Member(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MemberProfilePic/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    age=models.CharField(max_length=20,null=True)
    package=models.ForeignKey('Package', on_delete=models.CASCADE,null=True)
    trainer=models.ForeignKey('Trainer', on_delete=models.CASCADE,null=True)
    joineddate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Equipment(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=600)
    price=models.IntegerField()
    unit=models.IntegerField()
    pic= models.ImageField(upload_to='EquipmentPic/',null=True,blank=True)

class Attendance(models.Model):
    member=models.ForeignKey('Member',on_delete=models.CASCADE,null=True)
    date=models.DateField()
    present_status = models.CharField(max_length=10)

class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)
