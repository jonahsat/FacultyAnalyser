from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Choices for department and semester
DEPARTMENT_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Business Administration', 'Business Administration')
]

SEMESTER_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]

# Extend the User model with `is_student` and `is_faculty`
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    def __str__(self):
        if self.is_student:
            return f'{self.user.get_full_name()} - Student'
        elif self.is_faculty:
            return f'{self.user.get_full_name()} - Teacher'
        else:
            return f'{self.user} - Staff'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=50, unique=True) 
    major = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)

    def __str__(self):
        return f'{self.registration_id}: {self.user.get_full_name()} - {self.major}'

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.department}'

# Question Model
class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Automatically create the five predefined options for each question
        options = [
            ("Strongly Disagree", 1),
            ("Disagree", 2),
            ("Neutral", 3),
            ("Agree", 4),
            ("Strongly Agree", 5)
        ]
        
        # Create options if they don't already exist
        if not self.options.exists():
            for text, value in options:
                Option.objects.create(question=self, text=text, value=value)

# Options Model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.text}"

# Feedback Model
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'teacher', 'question')

    def __str__(self):
        return f"{self.student} - {self.teacher} - {self.question}"


class Analysis(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    overall_rating = models.FloatField()
    summary = models.TextField()
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.teacher} - {self.timestamp}"