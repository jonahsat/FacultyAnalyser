from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
import google.generativeai as genai

genai.configure(api_key="AIzaSyB5IAY1e0H-lCdM9Nu2zr97zBNxi0UIrak")

# Home page rendering only
def home(request):
    return render(request, 'home.html')

# Page to choose the faculty or student signup
def select_role(request):
    return render(request, 'select_role.html')

# Password validation function
def validate_passwords(password, confirm_password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if password != confirm_password:
        return "Passwords do not match."
    return None

# Student Signup View
def student_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        registration_id = request.POST['registration_id']
        major = request.POST['major']
        semester = request.POST['semester']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose another.")
            return render(request, 'student_signup.html')

        # Validate password
        password_validation_error = validate_passwords(password, confirm_password)
        if password_validation_error:
            messages.error(request, password_validation_error)
            return render(request, 'student_signup.html')

        # Create user and student profile
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_student = True
        user_profile.save()
        student = Student.objects.create(user=user, registration_id=registration_id, major=major, semester=semester)
        messages.success(request, "Student account created successfully.")
        return redirect('login')  # Redirect to login page or homepage

    return render(request, 'student_signup.html')

# Faculty Signup View
def faculty_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        department = request.POST['department']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose another.")
            return render(request, 'faculty_signup.html')

        # Validate password
        password_validation_error = validate_passwords(password, confirm_password)
        if password_validation_error:
            messages.error(request, password_validation_error)
            return render(request, 'faculty_signup.html')

        # Create user and teacher profile
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_faculty = True
        user_profile.save()
        teacher = Teacher.objects.create(user=user, department=department)
        

        messages.success(request, "Faculty account created successfully.")
        return redirect('login')  # Redirect to login page or homepage

    return render(request, 'faculty_signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user by email
        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username (which is email in this case) and password
        except User.DoesNotExist:
            user = None

        # If authentication is successful
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to homepage or another page after successful login
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'login.html')

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('home')


# Page to choose faculty before feedback
@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def start_feedback(request):
    student = request.user.student
    matching_faculty = Teacher.objects.filter(department=student.major) # Filter the teachers whose department matches the student's major
    return render(request, 'start_feedback.html', {'faculty_list': matching_faculty})


# Feedback form for the selected faculty
@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def feedback_form(request):
    if request.method == 'POST':
        teacher_id = request.POST['faculty_id']
        teacher = Teacher.objects.get(id=teacher_id)
    questions = Question.objects.all()
    return render(request, 'feedback_form.html', {'teacher': teacher, 'questions': questions})

@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def submit_feedback(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=teacher_id)
        student = request.user.student
        questions = Question.objects.all()
        
        for question in questions:
            option_id = request.POST.get(f'question_{question.id}')
            if option_id:
                option = get_object_or_404(Option, id=option_id)
                Feedback.objects.update_or_create(
                    student=student,
                    teacher=teacher,
                    question=question,
                    defaults={'selected_option': option}
                )
        
        messages.success(request, 'Feedback submitted successfully.')
        return redirect('student_dashboard')
    return redirect('start_feedback')


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_dashboard(request):
    student = request.user.student  # Get the current student instance
    teachers = Teacher.objects.filter(department=student.major)  # Get teachers in the same major

    # Get distinct teacher IDs from feedback
    submitted_feedbacks = Feedback.objects.filter(student=student).values('teacher').distinct()
    submitted_teacher_ids = [feedback['teacher'] for feedback in submitted_feedbacks]
    submitted_teachers = Teacher.objects.filter(id__in=submitted_teacher_ids)

    # Filter out teachers who already received feedback
    available_teachers = teachers.exclude(id__in=submitted_teacher_ids)

    return render(request, 'student_dashboard.html', {
        'student': student,
        'teachers': available_teachers,
        'submitted_teachers': submitted_teachers
    })


@login_required
@user_passes_test(lambda u: hasattr(u, 'teacher'))
def teacher_dashboard(request):
    teacher = request.user.teacher
    analysis = Analysis.objects.filter(teacher=teacher).order_by('-timestamp').first()
    context = {
        'teacher': teacher,
        'analysis': analysis,
        'overall_rating': analysis.overall_rating if analysis else 'N/A',
        'analysis_summary': analysis.summary if analysis else 'No analysis available yet.',
        'strengths': analysis.strengths.split('\n') if analysis else [],
        'improvement_areas': analysis.areas_for_improvement.split('\n') if analysis else [],
    }
    return render(request, 'teacher_dashboard.html', context)


# AI FUNCTIONS TO GENERATE FACULTY REVIEW

# Main function to generate analysis
@login_required
@user_passes_test(lambda u: hasattr(u, 'teacher'))
def generate_analysis(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    questions = Question.objects.all()
    feedbacks = Feedback.objects.filter(teacher=teacher)
    
    # For each question, gather the average of the students' opinions
    opinions = []
    for question in questions:
        question_feedback = feedbacks.filter(question=question)
        avg_opinion = question_feedback.aggregate(avg_value=Avg('selected_option__value'))['avg_value']
        opinions.append(avg_opinion or 0)

    # Generate analysis content using the Gemini API
    summary = generate_summary(questions, opinions)
    strengths = generate_strengths(questions, opinions)
    areas_for_improvement = generate_areas_for_improvement(questions, opinions)
    overall_rating = calculate_overall_score(opinions)

    # Save the analysis
    analysis = Analysis.objects.create(
        teacher=teacher,
        overall_rating=overall_rating,
        summary=summary,
        strengths=strengths,
        areas_for_improvement=areas_for_improvement,
    )
    
    # Redirect to the teacher dashboard or analysis review page
    return redirect('teacher_dashboard')


# AI function to generate summmary
def generate_summary(questions, opinions):
    model = genai.GenerativeModel('gemini-pro')
    template = """
    Provide a brief summary for the faculty based on the feedback received from students.
    The questions along with the corresponding ratings from 1 to 5 are given.
    Do not use any kind of formatting in your response. Also dont include headings.
    Just give a breif summary
    """
    prompt = template + "\n".join([f"Question: {question.text} Rating: {opinion}" for question, opinion in zip(questions, opinions)])
    response = model.generate_content(prompt)
    return response.text

# AI function to find strengths
def generate_strengths(questions, opinions):
    model = genai.GenerativeModel('gemini-pro')
    template = """
    List the strengths of the faculty based on the feedback received from students.
    The questions and corresponding ratings from 1 to 5 are provided.
    Do not use any kind of formatting in your response. Also dont include headings.
    Just list down the strengths one by one.
    """
    prompt = template + "\n".join([f"Question: {question.text} Rating: {opinion}" for question, opinion in zip(questions, opinions)])
    response = model.generate_content(prompt)
    return response.text

# AI function to suggest the areas to improve
def generate_areas_for_improvement(questions, opinions):
    model = genai.GenerativeModel('gemini-pro')
    template = """
    Provide areas for improvement for the faculty based on the feedback received from students.
    The questions and corresponding ratings from 1 to 5 are provided.
    Do not use any kind of formatting in your response. Also dont include headings.
    Just list down the areas for improvement one by one.
    """
    prompt = template + "\n".join([f"Question: {question.text} Rating: {opinion}" for question, opinion in zip(questions, opinions)])
    response = model.generate_content(prompt)
    return response.text

# Function to calculate the overall score out of 5
def calculate_overall_score(opinions):
    return sum(opinions) / len(opinions)

