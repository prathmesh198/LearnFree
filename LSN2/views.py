from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import course as CourseModel
from .forms import LoginForm, UserForm, CourseForm
from django.contrib.auth import logout

def index(request):
    courses = CourseModel.objects.all()
    return render(request, 'index.html', {'courses': courses})


def login_view(request):

    if request.method == 'POST':

     
        if 'register' in request.POST:
            fullname = request.POST.get('fullname')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")

            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")

            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.first_name = fullname
                user.save()

                messages.success(request, "Account created successfully")

            return redirect('login')

      
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = authenticate(request, username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')

    return render(request, 'login.html', {
        'login_form': LoginForm(),
        'register_form': UserForm()
    })


def course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CourseForm()

    courses = CourseModel.objects.all()

    return render(request, 'index.html', {
        'form': form,
        'courses': courses
    })


def coursepage(request, id):
    course = CourseModel.objects.get(id=id)
    modules = course.modules.all()

    return render(request, 'course.html', {
        'course': course,
        'modules': modules,
        'progress': 0
    })






@login_required
def profile_view(request):
    user = request.user

   
    courses = CourseModel.objects.all()  
    completed_courses = 0
    certificates = []

    return render(request, 'profile.html', {
        'courses': courses,
        'completed_courses': completed_courses,
        'certificates': certificates
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def course_redirect(request):
    first_course = CourseModel.objects.first()
    return redirect('course', id=first_course.id)

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

from .models import course as CourseModel


@login_required
def generate_certificate(request, course_id):
    course = CourseModel.objects.get(id=course_id)

    # 🔹 Load certificate image
    img_path = os.path.join(settings.BASE_DIR, 'static', 'certificate.jpg')
    image = Image.open(img_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    # 🔹 User data
    fullname = request.user.first_name or request.user.username
    today = date.today().strftime("%d/%m/%Y")

    # 🔹 Fonts (IMPORTANT: path for Windows)
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_big = ImageFont.truetype(font_path, 50)
    font_medium = ImageFont.truetype(font_path, 28)

    width, height = image.size

    # 🔥 FUNCTION TO CENTER TEXT
    def center_text(text, y, font):
        text_width = draw.textlength(text, font=font)
        x = (width - text_width) / 2
        draw.text((x, y), text, fill="black", font=font)

    # =========================
    # 🎯 TEXT POSITIONS (FIXED)
    # =========================

    # ✅ NAME (correct position)
    center_text(fullname, 430, font_big)

    # ✅ "For his achievements..." (left aligned)
    draw.text(
        (width * 0.22, 480),
        "For his achievements and participation in",
        fill="black",
        font=font_medium
    )

    # ✅ COURSE NAME (centered on blank line)
    center_text(f"______{course.name}______", 500, font_medium)

    # ✅ "Held on"
    draw.text(
        (width * 0.30, 540),
        "Held on",
        fill="black",
        font=font_medium
    )

    # ✅ DATE (centered)
    center_text(f"______{today}______", 560, font_medium)

    # ✅ "by ______"
    draw.text(
        (width * 0.60, 540),
        "by __________",
        fill="black",
        font=font_medium
    )

    # 🔹 Return as JPG
    response = HttpResponse(content_type='image/jpeg')
    response['Content-Disposition'] = 'attachment; filename="certificate.jpg"'

    image.save(response, "JPEG")

    return response