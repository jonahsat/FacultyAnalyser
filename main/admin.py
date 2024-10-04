from django.contrib import admin
from .models import UserProfile, Student, Teacher, Question, Feedback, Analysis

# Customizing the UserProfile model in the admin interface
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_student', 'is_faculty')  # Displays the user and their role (student or faculty)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')  # Enables search by username and name
    list_filter = ('is_student', 'is_faculty')  # Adds filters for student/faculty role

# Customizing the Student model in the admin interface
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'user_full_name', 'major', 'semester')  # Displays registration ID, user, major, and semester
    search_fields = ('registration_id', 'user__first_name', 'user__last_name', 'major')  # Enables search by registration ID and name
    list_filter = ('major', 'semester')  # Adds filters for major and semester
    ordering = ('registration_id',)  # Orders students by their registration ID

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Student Name'

# Customizing the Teacher model in the admin interface
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'department')  # Displays the teacher's name and department
    search_fields = ('user__first_name', 'user__last_name', 'department')  # Enables search by name and department
    list_filter = ('department',)  # Adds a filter for department
    ordering = ('user__last_name',)  # Orders teachers alphabetically by their last name

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Teacher Name'

# Customizing the Question model in the admin interface
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)  # Displays the question text
    search_fields = ('text',)  # Enables search by question text
    ordering = ('text',)  # Orders questions alphabetically by text


# Customizing the Feedback model in the admin interface
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student_full_name', 'teacher_full_name', 'question', 'selected_option', 'timestamp')  # Displays feedback details
    readonly_fields = ('student', 'teacher', 'question', 'selected_option', 'timestamp')
    search_fields = ('student__user__first_name', 'teacher__user__first_name', 'question__text', 'selected_option__text')  # Enables search by student, teacher, question, and option
    list_filter = ('teacher', 'student', 'question')  # Adds filters for teacher, student, and question
    ordering = ('-timestamp',)  # Orders feedback by the most recent

    def student_full_name(self, obj):
        return obj.student.user.get_full_name()
    student_full_name.short_description = 'Student Name'

    def teacher_full_name(self, obj):
        return obj.teacher.user.get_full_name()
    teacher_full_name.short_description = 'Teacher Name'


# Customizing the Analysis model in the admin interface
@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('teacher_full_name', 'overall_rating', 'timestamp')  # Displays the teacher, overall rating, and timestamp
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'summary', 'strengths', 'areas_for_improvement')  # Enables search by teacher name, summary, strengths, and areas for improvement
    list_filter = ('teacher', 'timestamp')  # Adds filters for teacher and timestamp
    ordering = ('-timestamp',)  # Orders analyses by the most recent

    def teacher_full_name(self, obj):
        return obj.teacher.user.get_full_name()
    teacher_full_name.short_description = 'Teacher Name'
