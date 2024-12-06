from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  
    path('', views.student_list, name='student_list'),
    path('new/', views.student_create, name='student_create'),
    path('edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),


    path('enroll_student/', views.enroll_student, name='enroll_student'),  # <---- Ruta para enroll_student
    path('enrollment_list/', views.enrollment_list, name='enrollment_list'),
    path('grade_student/<int:pk>/', views.grade_student, name='grade_student'),

    # Login y Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/new/', views.subject_create, name='subject_create'),
    path('subjects/edit/<int:pk>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:pk>/', views.subject_delete, name='subject_delete'),
]
