from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('start_feedback/', views.start_feedback, name='start_feedback'),
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('submit_feedback/<int:teacher_id>/', views.submit_feedback, name='submit_feedback'),

    # Authentication Urls
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('select_role/', views.select_role, name='select_role'),
    path('student_signup/', views.student_signup, name='student_signup'),
    path('faculty_signup/', views.faculty_signup, name='faculty_signup'),

    path('generate_analysis/', views.generate_analysis, name='generate_analysis'),

]