from ast import mod
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'gym/index.html')

def aboutus_view(request):
    return render(request,'gym/aboutus.html')


def trainer_signup_view(request):
    userForm=forms.TrainerUserForm()
    trainerForm=forms.TrainerForm()
    mydict={'userForm':userForm,'trainerForm':trainerForm}
    if request.method=='POST':
        userForm=forms.TrainerUserForm(request.POST)
        trainerForm=forms.TrainerForm(request.POST,request.FILES)
        if userForm.is_valid() and trainerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=trainerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_group = Group.objects.get_or_create(name='TRAINER')
            my_group[0].user_set.add(user)
        return HttpResponseRedirect('trainerlogin')
    return render(request,'gym/trainersignup.html',context=mydict)




#for checking user customer, mechanic or admin(by sumit)
def is_tariner(user):
    return user.groups.filter(name='TRAINER').exists()
def is_member(user):
    return user.groups.filter(name='MEMBER').exists()


def afterlogin_view(request):
    if is_tariner(request.user):
        accountapproval=models.Trainer.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('trainer-dashboard')
        else:
            return render(request,'gym/trainer_wait_for_approval.html')
    elif is_member(request.user):
        accountapproval=models.Member.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('member-dashboard')
        else:
            return render(request,'gym/member_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    import datetime
    today = datetime.date.today()
    
    weekday = today.weekday() 
    last_monday = today - datetime.timedelta(days=weekday % 7)
   # print("last_monday-------"+str(last_monday))

    weekday = today.weekday()-1
    last_tuesday = today - datetime.timedelta(days=weekday % 7)
    #print("last_tuesday-------"+str(last_tuesday))

    weekday = today.weekday()-2
    last_wednesday = today - datetime.timedelta(days=weekday % 7)
    #print("last_wednesday-------"+str(last_wednesday))

    weekday = today.weekday()-3
    last_thursday = today - datetime.timedelta(days=weekday % 7)
   # print("last_thursday-------"+str(last_thursday))
    weekday = today.weekday()-4
    last_friday = today - datetime.timedelta(days=weekday % 7)
    #print("last_friday-------"+str(last_friday))
    
    weekday = today.weekday()-5
    last_saturday = today - datetime.timedelta(days=weekday % 7)
    #print("last_saturday-------"+str(last_saturday))
    
    weekday = today.weekday()+1
    last_sunday = today - datetime.timedelta(days=weekday % 7)
    #print("last_sunday-------"+str(last_sunday))

    '''
    first we found last monday,tuesday...
    then from attendance we take all attendances of that day with only present status
    for absent -- total member minus present on that day will be treated as absent... whether admin/
    trainer mark it as absent or not
    NOTE: for one member for same day there should not be 2 record...so do not take attendance of
    member for same day twice...otherwise graph will show wrong data 
    '''
    membercount=models.Member.objects.all().filter(status=True).count()

    dict={
        'trainer_count':models.Trainer.objects.all().filter(status=True).count(),
        'member_count':membercount,
        'package_count':models.Package.objects.all().count(),
        'equipment_count':models.Equipment.objects.all().count(),
        'monday_present':models.Attendance.objects.all().filter(date=last_monday).filter(present_status='Present').count(),
        'monday_absent':membercount-models.Attendance.objects.all().filter(date=last_monday).filter(present_status='Present').count(),

        'tuesday_present':models.Attendance.objects.all().filter(date=last_tuesday).filter(present_status='Present').count(),
        'tuesday_absent':membercount-models.Attendance.objects.all().filter(date=last_tuesday).filter(present_status='Present').count(),
 
        'wednesday_present':models.Attendance.objects.all().filter(date=last_wednesday).filter(present_status='Present').count(),
        'wednesday_absent':membercount-models.Attendance.objects.all().filter(date=last_wednesday).filter(present_status='Present').count(),
 
        'thursday_present':models.Attendance.objects.all().filter(date=last_thursday).filter(present_status='Present').count(),
        'thursday_absent':membercount-models.Attendance.objects.all().filter(date=last_thursday).filter(present_status='Present').count(),
 
        'friday_present':models.Attendance.objects.all().filter(date=last_friday).filter(present_status='Present').count(),
        'friday_absent':membercount-models.Attendance.objects.all().filter(date=last_friday).filter(present_status='Present').count(),

        'saturday_present':models.Attendance.objects.all().filter(date=last_saturday).filter(present_status='Present').count(),
        'saturday_absent':membercount-models.Attendance.objects.all().filter(date=last_saturday).filter(present_status='Present').count(),

        'sunday_present':models.Attendance.objects.all().filter(date=last_sunday).filter(present_status='Present').count(),
        'sunday_absent':membercount-models.Attendance.objects.all().filter(date=last_sunday).filter(present_status='Present').count(),
    
        'last_monday':str(last_monday),
        'last_tuesday':str(last_tuesday),
        'last_wednesday':str(last_wednesday),
        'last_thursday':str(last_thursday),
        'last_friday':str(last_friday),
        'last_saturday':str(last_saturday),
        'last_sunday':str(last_sunday)

    }
    
    return render(request,'gym/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_trainer_view(request):
    return render(request,'gym/admin_trainer.html')

@login_required(login_url='adminlogin')
def admin_view_trainer_view(request):
    trainers=models.Trainer.objects.all().filter(status=True)
    return render(request,'gym/admin_view_trainer.html',{'trainers':trainers})

@login_required(login_url='adminlogin')
def admin_view_trainer_shift_view(request):
    trainers=models.Trainer.objects.all().filter(status=True)
    return render(request,'gym/admin_view_trainer_shift.html',{'trainers':trainers})



@login_required(login_url='adminlogin')
def admin_approve_trainer_view(request):
    trainers=models.Trainer.objects.all().filter(status=False)
    return render(request,'gym/admin_approve_trainer.html',{'trainers':trainers})

@login_required(login_url='adminlogin')
def delete_trainer_view(request,pk):
    trainer=models.Trainer.objects.get(id=pk)
    user=models.User.objects.get(id=trainer.user_id)
    user.delete()
    trainer.delete()
    return redirect('admin-view-trainer')


@login_required(login_url='adminlogin')
def approve_trainer_view(request,pk):
   
    trainerForm=forms.TrainerApprovalForm()
    if request.method=='POST':
        trainerForm=forms.TrainerApprovalForm(request.POST)
        if trainerForm.is_valid():
            trainer=models.Trainer.objects.get(id=pk)
            trainer.salary=trainerForm.cleaned_data['salary']
            trainer.shift=trainerForm.cleaned_data['shift']
            trainer.status=True
            trainer.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-trainer')
    return render(request,'gym/admin_approve_trainer_details.html',{'trainerForm':trainerForm})



@login_required(login_url='adminlogin')
def reject_trainer_view(request,pk):
    trainer=models.Trainer.objects.get(id=pk)
    user=models.User.objects.get(id=trainer.user_id)
    user.delete()
    trainer.delete()
    return redirect('admin-approve-trainer')


@login_required(login_url='adminlogin')
def admin_add_trainer_view(request):
    userForm=forms.TrainerUserForm()
    trainerForm=forms.TrainerFormAdmin()
    mydict={'userForm':userForm,'trainerForm':trainerForm}
    if request.method=='POST':
        userForm=forms.TrainerUserForm(request.POST)
        trainerForm=forms.TrainerFormAdmin(request.POST,request.FILES)
        if userForm.is_valid() and trainerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            trainer=trainerForm.save(commit=False)
            trainer.user=user
            trainer.status=True
            trainer.save()
            my_group = Group.objects.get_or_create(name='TRAINER')
            my_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-trainer')
    return render(request,'gym/admin_add_trainer.html',context=mydict)


@login_required(login_url='adminlogin')
def edit_trainer_view(request,pk):
    trainer=models.Trainer.objects.get(id=pk)
    user=models.User.objects.get(id=trainer.user_id)
    userForm=forms.TrainerUserForm(instance=user)
    trainerForm=forms.TrainerFormAdmin(instance=trainer)
    mydict={'userForm':userForm,'trainerForm':trainerForm}
    if request.method=='POST':
        userForm=forms.TrainerUserForm(request.POST,instance=user)
        trainerForm=forms.TrainerFormAdmin(request.POST,request.FILES,instance=trainer)
        if userForm.is_valid() and trainerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            trainerForm.save()
            return redirect('admin-view-trainer')
    return render(request,'gym/edit_trainer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_package_view(request):
    return render(request,'gym/admin_package.html')



@login_required(login_url='adminlogin')
def admin_add_package_view(request):
    packageForm=forms.PackageForm()
    mydict={'packageForm':packageForm}
    if request.method=='POST':
        packageForm=forms.PackageForm(request.POST,request.FILES)
        if packageForm.is_valid():
            packageForm.save()
        return HttpResponseRedirect('/admin-view-package')
    return render(request,'gym/admin_add_package.html',context=mydict)

@login_required(login_url='adminlogin')
def edit_package_view(request,pk):
    package=models.Package.objects.get(id=pk)
    packageForm=forms.PackageForm(instance=package)
    mydict={'packageForm':packageForm}
    if request.method=='POST':
        packageForm=forms.PackageForm(request.POST,instance=package)
        if packageForm.is_valid():
            packageForm.save()
        return HttpResponseRedirect('/admin-view-package')
    return render(request,'gym/admin_edit_package.html',context=mydict)



@login_required(login_url='adminlogin')
def admin_view_package_view(request):
    packages=models.Package.objects.all()
    return render(request,'gym/admin_view_package.html',{'packages':packages})




@login_required(login_url='adminlogin')
def delete_package_view(request,pk):
    package=models.Package.objects.get(id=pk)
    package.delete()
    return redirect('admin-view-package')



@login_required(login_url='adminlogin')
def admin_equipment_view(request):
    return render(request,'gym/admin_equipment.html')



@login_required(login_url='adminlogin')
def admin_add_equipment_view(request):
    equipmentForm=forms.EquipmentForm()
    mydict={'equipmentForm':equipmentForm}
    if request.method=='POST':
        equipmentForm=forms.EquipmentForm(request.POST,request.FILES)
        if equipmentForm.is_valid():
            equipmentForm.save()
        return HttpResponseRedirect('/admin-view-equipment')
    return render(request,'gym/admin_add_equipment.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_equipment_view(request):
    equipments=models.Equipment.objects.all()
    return render(request,'gym/admin_view_equipment.html',{'equipments':equipments})



@login_required(login_url='adminlogin')
def delete_equipment_view(request,pk):
    equipment=models.Equipment.objects.get(id=pk)
    equipment.delete()
    return redirect('admin-view-equipment')


@login_required(login_url='adminlogin')
def edit_equipment_view(request,pk):
    equipment=models.Equipment.objects.get(id=pk)
    equipmentForm=forms.EquipmentForm(instance=equipment)
    mydict={'equipmentForm':equipmentForm}
    if request.method=='POST':
        equipmentForm=forms.EquipmentForm(request.POST,request.FILES,instance=equipment)
        if equipmentForm.is_valid():
            equipmentForm.save()
        return HttpResponseRedirect('/admin-view-equipment')
    return render(request,'gym/admin_edit_equipment.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_member_view(request):
    return render(request,'gym/admin_member.html')

@login_required(login_url='adminlogin')
def admin_add_member_view(request):
    userForm=forms.MemberUserForm()
    memberForm1=forms.MemberForm1()
    memberForm2=forms.MemberForm2()
    mydict={'userForm':userForm,'memberForm1':memberForm1,'memberForm2':memberForm2}
    if request.method=='POST':
        userForm=forms.MemberUserForm(request.POST,request.FILES)
        memberForm1=forms.MemberForm1(request.POST,request.FILES)
        memberForm2=forms.MemberForm2(request.POST,request.FILES)
        if userForm.is_valid() and memberForm1.is_valid() and memberForm2.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            member=memberForm1.save(commit=False)
            member.user=user
            member.package=memberForm2.cleaned_data['package']
            member.trainer=memberForm2.cleaned_data['trainer']
            member.status=True
            member.save()
            my_group = Group.objects.get_or_create(name='MEMBER')
            my_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-member')
    return render(request,'gym/admin_add_member.html',context=mydict)



@login_required(login_url='adminlogin')
def admin_view_member_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/admin_view_member.html',{'members':members})

@login_required(login_url='adminlogin')
def admin_view_member_trainer_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/admin_view_member_trainer.html',{'members':members})

@login_required(login_url='adminlogin')
def admin_approve_member_view(request):
    members=models.Member.objects.all().filter(status=False)
    return render(request,'gym/admin_approve_member.html',{'members':members})



@login_required(login_url='adminlogin')
def delete_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    user=models.User.objects.get(id=member.user_id)
    user.delete()
    member.delete()
    return redirect('admin-view-member')

@login_required(login_url='adminlogin')
def edit_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    user=models.User.objects.get(id=member.user_id)
    userForm=forms.MemberUserForm(instance=user)
    memberForm1=forms.MemberForm1(instance=member)
    memberForm2=forms.MemberForm2()
    mydict={'userForm':userForm,'memberForm1':memberForm1,'memberForm2':memberForm2}
    if request.method=='POST':
        userForm=forms.MemberUserForm(request.POST,request.FILES,instance=user)
        memberForm1=forms.MemberForm1(request.POST,request.FILES,instance=member)
        memberForm2=forms.MemberForm2(request.POST,request.FILES)
        if userForm.is_valid() and memberForm1.is_valid() and memberForm2.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            member=memberForm1.save(commit=False)
            member.user=user
            member.package=memberForm2.cleaned_data['package']
            member.trainer=memberForm2.cleaned_data['trainer']
            member.status=True
            member.save()
            my_group = Group.objects.get_or_create(name='MEMBER')
            my_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-member')
    return render(request,'gym/admin_edit_member.html',context=mydict)


@login_required(login_url='adminlogin')
def reject_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    user=models.User.objects.get(id=member.user_id)
    user.delete()
    member.delete()
    return redirect('admin-approve-member')

@login_required(login_url='adminlogin')
def approve_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    member.status=True
    member.save()
    return redirect('admin-approve-member')


def admin_attendance_view(request):
    return render(request,'gym/admin_attendance.html')

def admin_take_attendance_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/admin_take_attendance.html',{'members':members})

def take_attendance_view(request,pk):
    member=models.Member.objects.get(id=pk)
    attendanceForm=forms.AttendanceForm()
    mydict={'attendanceForm':attendanceForm,'member':member}
    if request.method=='POST':
        attendanceForm=forms.AttendanceForm(request.POST,request.FILES)
        if attendanceForm.is_valid():
            present_status=attendanceForm.cleaned_data['present_status']
            date=attendanceForm.cleaned_data['date']
            attendance=models.Attendance()
            attendance.member=member
            attendance.date=date
            attendance.present_status=present_status
            attendance.save()
        return HttpResponseRedirect('/admin-take-attendance')
    return render(request,'gym/take_attendance.html',context=mydict)

def admin_view_attendance_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/admin_view_attendance.html',{'members':members})

def view_attendance_view(request,pk):
    member=models.Member.objects.get(id=pk)
    attendances=models.Attendance.objects.all().filter(member=member)
    return render(request,'gym/view_attendance.html',{'attendances':attendances,'member':member})

#============================================================================================
# MEMBER RELATED views start
#============================================================================================

def member_signup_view(request):
    userForm=forms.MemberUserForm()
    memberForm1=forms.MemberForm1()
    memberForm2=forms.MemberForm2()
    mydict={'userForm':userForm,'memberForm1':memberForm1,'memberForm2':memberForm2}
    if request.method=='POST':
        userForm=forms.MemberUserForm(request.POST,request.FILES)
        memberForm1=forms.MemberForm1(request.POST,request.FILES)
        memberForm2=forms.MemberForm2(request.POST,request.FILES)
        if userForm.is_valid() and memberForm1.is_valid() and memberForm2.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            member=memberForm1.save(commit=False)
            member.user=user
            member.package=memberForm2.cleaned_data['package']
            member.trainer=memberForm2.cleaned_data['trainer']
            member.status=False
            member.save()
            my_group = Group.objects.get_or_create(name='MEMBER')
            my_group[0].user_set.add(user)
        return HttpResponseRedirect('/memberlogin')
    return render(request,'gym/membersignup.html',context=mydict)



@login_required(login_url='memberlogin')
def member_dashboard_view(request):
    member=models.Member.objects.get(user_id=request.user.id)   
    dict={
        'my_fee':member.package.amount,
        'trainer_assigned':member.trainer,
        'trainer_shift':member.trainer.shift,
        'trainer_count':models.Trainer.objects.all().filter(status=True).count(),
        'package_count':models.Package.objects.all().count(),
        'equipment_count':models.Equipment.objects.all().count(),
        
    }
    return render(request,'gym/member_dashboard.html',context=dict)



@login_required(login_url='memberlogin')
def member_view_package_view(request):
    packages=models.Package.objects.all()
    return render(request,'gym/member_view_package.html',{'packages':packages})


@login_required(login_url='memberlogin')
def member_view_equipment_view(request):
    equipments=models.Equipment.objects.all()
    return render(request,'gym/member_view_equipment.html',{'equipments':equipments})

@login_required(login_url='memberlogin')
def member_view_trainer_view(request):
    dict={
        'trainers':models.Trainer.objects.all().filter(status=True)
    }
    return render(request,'gym/member_view_trainer.html',context=dict)


@login_required(login_url='memberlogin')
def member_view_attendance_view(request):
    member=models.Member.objects.get(user_id=request.user.id)
    attendances=models.Attendance.objects.all().filter(member=member)
    return render(request,'gym/member_view_attendance.html',{'attendances':attendances,'member':member})


@login_required(login_url='memberlogin')
def member_profile_view(request):
    member=models.Member.objects.get(user_id=request.user.id)
    return render(request,'gym/member_profile.html',{'member':member})










#============================================================================================
# TRAINER RELATED views start
#============================================================================================


@login_required(login_url='trainerlogin')
def trainer_dashboard_view(request):
    import datetime
    today = datetime.date.today()
    
    weekday = today.weekday() 
    last_monday = today - datetime.timedelta(days=weekday % 7)
   # print("last_monday-------"+str(last_monday))

    weekday = today.weekday()-1
    last_tuesday = today - datetime.timedelta(days=weekday % 7)
    #print("last_tuesday-------"+str(last_tuesday))

    weekday = today.weekday()-2
    last_wednesday = today - datetime.timedelta(days=weekday % 7)
    #print("last_wednesday-------"+str(last_wednesday))

    weekday = today.weekday()-3
    last_thursday = today - datetime.timedelta(days=weekday % 7)
   # print("last_thursday-------"+str(last_thursday))
    weekday = today.weekday()-4
    last_friday = today - datetime.timedelta(days=weekday % 7)
    #print("last_friday-------"+str(last_friday))
    
    weekday = today.weekday()-5
    last_saturday = today - datetime.timedelta(days=weekday % 7)
    #print("last_saturday-------"+str(last_saturday))
    
    weekday = today.weekday()+1
    last_sunday = today - datetime.timedelta(days=weekday % 7)
    #print("last_sunday-------"+str(last_sunday))

    '''
    first we found last monday,tuesday...
    then from attendance we take all attendances of that day with only present status
    for absent -- total member minus present on that day will be treated as absent... whether admin/
    trainer mark it as absent or not
    NOTE: for one member for same day there should not be 2 record...so do not take attendance of
    member for same day twice...otherwise graph will show wrong data 
    '''
    trainer=models.Trainer.objects.get(user_id=request.user.id)
    membercount=models.Member.objects.all().filter(status=True).count()
   
    dict={
        'my_member_count':models.Member.objects.all().filter(status=True).filter(trainer=trainer).count(),
        'member_count':membercount,
        'package_count':models.Package.objects.all().count(),
        'equipment_count':models.Equipment.objects.all().count(),
        'monday_present':models.Attendance.objects.all().filter(date=last_monday).filter(present_status='Present').count(),
        'monday_absent':membercount-models.Attendance.objects.all().filter(date=last_monday).filter(present_status='Present').count(),

        'tuesday_present':models.Attendance.objects.all().filter(date=last_tuesday).filter(present_status='Present').count(),
        'tuesday_absent':membercount-models.Attendance.objects.all().filter(date=last_tuesday).filter(present_status='Present').count(),
 
        'wednesday_present':models.Attendance.objects.all().filter(date=last_wednesday).filter(present_status='Present').count(),
        'wednesday_absent':membercount-models.Attendance.objects.all().filter(date=last_wednesday).filter(present_status='Present').count(),
 
        'thursday_present':models.Attendance.objects.all().filter(date=last_thursday).filter(present_status='Present').count(),
        'thursday_absent':membercount-models.Attendance.objects.all().filter(date=last_thursday).filter(present_status='Present').count(),
 
        'friday_present':models.Attendance.objects.all().filter(date=last_friday).filter(present_status='Present').count(),
        'friday_absent':membercount-models.Attendance.objects.all().filter(date=last_friday).filter(present_status='Present').count(),

        'saturday_present':models.Attendance.objects.all().filter(date=last_saturday).filter(present_status='Present').count(),
        'saturday_absent':membercount-models.Attendance.objects.all().filter(date=last_saturday).filter(present_status='Present').count(),

        'sunday_present':models.Attendance.objects.all().filter(date=last_sunday).filter(present_status='Present').count(),
        'sunday_absent':membercount-models.Attendance.objects.all().filter(date=last_sunday).filter(present_status='Present').count(),
    
        'last_monday':str(last_monday),
        'last_tuesday':str(last_tuesday),
        'last_wednesday':str(last_wednesday),
        'last_thursday':str(last_thursday),
        'last_friday':str(last_friday),
        'last_saturday':str(last_saturday),
        'last_sunday':str(last_sunday)

    }
    return render(request,'gym/trainer_dashboard.html',context=dict)


@login_required(login_url='trainerlogin')
def trainer_view_member_view(request):
    dict={
        'members':models.Member.objects.all().filter(status=True)
    }
    return render(request,'gym/trainer_view_member.html',context=dict)


@login_required(login_url='trainerlogin')
def trainer_view_my_member_view(request):
    trainer=models.Trainer.objects.get(user_id=request.user.id)
    dict={
        'members':models.Member.objects.all().filter(status=True).filter(trainer=trainer)
    }
    return render(request,'gym/trainer_view_my_member.html',context=dict)


@login_required(login_url='trainerlogin')
def trainer_view_package_view(request):
    packages=models.Package.objects.all()
    return render(request,'gym/trainer_view_package.html',{'packages':packages})


@login_required(login_url='trainerlogin')
def trainer_view_equipment_view(request):
    equipments=models.Equipment.objects.all()
    return render(request,'gym/trainer_view_equipment.html',{'equipments':equipments})

@login_required(login_url='trainerlogin')
def trainer_view_attendance_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/trainer_view_attendance.html',{'members':members})


@login_required(login_url='trainerlogin')
def trainer_view_attendance_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    attendances=models.Attendance.objects.all().filter(member=member)
    return render(request,'gym/trainer_view_attendance_member.html',{'attendances':attendances,'member':member})


@login_required(login_url='trainerlogin')
def trainer_take_attendance_view(request):
    members=models.Member.objects.all().filter(status=True)
    return render(request,'gym/trainer_take_attendance.html',{'members':members})

@login_required(login_url='trainerlogin')
def trainer_take_attendance_member_view(request,pk):
    member=models.Member.objects.get(id=pk)
    attendanceForm=forms.AttendanceForm()
    mydict={'attendanceForm':attendanceForm,'member':member}
    if request.method=='POST':
        attendanceForm=forms.AttendanceForm(request.POST,request.FILES)
        if attendanceForm.is_valid():
            present_status=attendanceForm.cleaned_data['present_status']
            date=attendanceForm.cleaned_data['date']
            attendance=models.Attendance()
            attendance.member=member
            attendance.date=date
            attendance.present_status=present_status
            attendance.save()
        return HttpResponseRedirect('/trainer-take-attendance')
    return render(request,'gym/trainer_take_attendance_member.html',context=mydict)

@login_required(login_url='trainerlogin')
def trainer_profile_view(request):
    trainer=models.Trainer.objects.get(user_id=request.user.id)
    return render(request,'gym/trainer_profile.html',{'trainer':trainer})

