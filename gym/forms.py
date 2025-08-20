from django import forms
from django.contrib.auth.models import User
from . import models

class TrainerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TrainerForm(forms.ModelForm):
    class Meta:
        model=models.Trainer
        fields=['age','mobile','profile_pic','experience']
        

class TrainerFormAdmin(forms.ModelForm):
    class Meta:
        model=models.Trainer
        fields=['age','mobile','profile_pic','experience','salary','shift']



class TrainerApprovalForm(forms.Form):
    salary=forms.IntegerField();
    shift=forms.CharField(max_length=200);

class MemberUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MemberForm1(forms.ModelForm):
    class Meta:
        model=models.Member
        fields=['age','mobile','profile_pic']
class MemberForm2(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of  model will be shown there in html
    package=forms.ModelChoiceField(queryset=models.Package.objects.all(),empty_label="Package Name",to_field_name='id')
    trainer=forms.ModelChoiceField(queryset=models.Trainer.objects.all(),empty_label="Trainer Name",to_field_name='id')


#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()
  












class PackageForm(forms.ModelForm):
    class Meta:
        model=models.Package
        fields=['name','amount','duration','description']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model=models.Equipment
        fields=['name','description','pic','unit','price']





class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['by','message']
        widgets = {
        'message':forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
