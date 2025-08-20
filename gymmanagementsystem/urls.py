
from django.contrib import admin
from django.urls import path
from gym import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('adminlogin', LoginView.as_view(template_name='gym/adminlogin.html'),name='adminlogin'),
    path('memberlogin', LoginView.as_view(template_name='gym/memberlogin.html'),name='memberlogin'),
    path('trainerlogin', LoginView.as_view(template_name='gym/trainerlogin.html'),name='trainerlogin'),
    path('membersignup', views.member_signup_view,name='membersignup'),
    path('trainersignup', views.trainer_signup_view,name='trainersignup'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='gym/index.html'),name='logout'),


    path('admin-trainer', views.admin_trainer_view,name='admin-trainer'),
    path('admin-view-trainer', views.admin_view_trainer_view,name='admin-view-trainer'),
    path('admin-approve-trainer', views.admin_approve_trainer_view,name='admin-approve-trainer'),
    path('admin-add-trainer', views.admin_add_trainer_view,name='admin-add-trainer'),
    path('admin-view-trainer-shift', views.admin_view_trainer_shift_view,name='admin-view-trainer-shift'),
    path('delete-trainer/<int:pk>', views.delete_trainer_view,name='delete-trainer'),
    path('edit-trainer/<int:pk>', views.edit_trainer_view,name='edit-trainer'),
    path('approve-trainer/<int:pk>', views.approve_trainer_view,name='approve-trainer'),
    path('reject-trainer/<int:pk>', views.reject_trainer_view,name='reject-trainer'),

    path('admin-package', views.admin_package_view,name='admin-package'),
    path('admin-view-package', views.admin_view_package_view,name='admin-view-package'),
    path('admin-add-package', views.admin_add_package_view,name='admin-add-package'),
    path('delete-package/<int:pk>', views.delete_package_view,name='delete-package'),
    path('edit-package/<int:pk>', views.edit_package_view,name='edit-package'),


    path('admin-equipment', views.admin_equipment_view,name='admin-equipment'),
    path('admin-view-equipment', views.admin_view_equipment_view,name='admin-view-equipment'),
    path('admin-add-equipment', views.admin_add_equipment_view,name='admin-add-equipment'),
    path('delete-equipment/<int:pk>', views.delete_equipment_view,name='delete-equipment'),
    path('edit-equipment/<int:pk>', views.edit_equipment_view,name='edit-equipment'),

    path('admin-member', views.admin_member_view,name='admin-member'),
    path('admin-view-member', views.admin_view_member_view,name='admin-view-member'),
    path('admin-view-member-trainer', views.admin_view_member_trainer_view,name='admin-view-member-trainer'),
    path('admin-add-member', views.admin_add_member_view,name='admin-add-member'),
    path('delete-member/<int:pk>', views.delete_member_view,name='delete-member'),
    path('edit-member/<int:pk>', views.edit_member_view,name='edit-member'),
    path('admin-approve-member', views.admin_approve_member_view,name='admin-approve-member'),
    path('approve-member/<int:pk>', views.approve_member_view,name='approve-member'),
    path('reject-member/<int:pk>', views.reject_member_view,name='reject-member'),
    path('admin-attendance', views.admin_attendance_view,name='admin-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('view-attendance/<int:pk>', views.view_attendance_view,name='view-attendance'),
    path('take-attendance/<int:pk>', views.take_attendance_view,name='take-attendance'),



    path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),
    path('trainer-view-member', views.trainer_view_member_view,name='trainer-view-member'),
    path('trainer-view-my-member', views.trainer_view_my_member_view,name='trainer-my-view-member'),
    path('trainer-view-equipment', views.trainer_view_equipment_view,name='trainer-view-equipment'),
    path('trainer-view-package', views.trainer_view_package_view,name='trainer-view-package'),
    path('trainer-view-attendance', views.trainer_view_attendance_view,name='trainer-view-attendance'),
    path('trainer-view-attendance-member/<int:pk>', views.trainer_view_attendance_member_view,name='trainer-view-attendance-member'),
    path('trainer-take-attendance', views.trainer_take_attendance_view,name='trainer-take-attendance'),
    path('trainer-take-attendance-member/<int:pk>', views.trainer_take_attendance_member_view,name='trainer-take-attendance-member'),
    path('trainer-profile', views.trainer_profile_view,name='trainer-profile'),



    path('member-dashboard', views.member_dashboard_view,name='member-dashboard'),
    path('member-view-equipment', views.member_view_equipment_view,name='member-view-equipment'),
    path('member-view-package', views.member_view_package_view,name='member-view-package'),
    path('member-view-trainer', views.member_view_trainer_view,name='member-view-trainer'),
    path('member-view-attendance', views.member_view_attendance_view,name='member-view-attendance'),
    path('member-profile', views.member_profile_view,name='member-profile'),


    path('aboutus', views.aboutus_view),
    
]
