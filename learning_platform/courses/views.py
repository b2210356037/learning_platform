from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Course, Lesson, Category
from .forms import CourseForm, LessonForm
from django.db.models import Q
from fuzzywuzzy import fuzz, process
from .models import Course, Lesson
from .forms import LessonForm

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('course_list')
        else:
            messages.error(request, "Invalid username or password.")
    #featured_courses = Course.objects.filter(featured=True)[:6]  #olmayan tablodan veri çekmeye çalışıyor
    categories = Category.objects.all()[:6]
    return render(request, 'home.html', {
        #'featured_courses': featured_courses, 
        'categories': categories,
    })

@login_required
def favorite_courses(request):
    favorite_courses = request.user.favorite_courses.all()
    return render(request, 'courses/favorite_courses.html', {'favorite_courses': favorite_courses})

@login_required
def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.favorites.filter(id=request.user.id).exists():
        course.favorites.remove(request.user)
    else:
        course.favorites.add(request.user)
    return redirect('course_detail', course_id=course_id)

@login_required
def course_list(request):
    search_term = request.GET.get('search', '')
    courses = Course.objects.all()

    if search_term:
        # Fuzzy search
        course_titles = courses.values_list('title', flat=True)
        matches = process.extract(search_term, course_titles, limit=10, scorer=fuzz.partial_ratio)
        matched_titles = [match[0] for match in matches if match[1] >= 45]  # 40% similarity threshold
        
        courses = courses.filter(Q(title__in=matched_titles) | Q(description__icontains=search_term))

    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    if request.user.is_student() or request.user.is_admin_user() or (request.user.is_tutor()):
        return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})
    else:
        messages.error(request, "You don't have permission to view this course.")
        return redirect('course_list')

@login_required
def create_course(request):
    if not request.user.is_tutor() and not request.user.is_admin_user():
        messages.error(request, "You don't have permission to create courses.")
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = request.user
            course.save()
            messages.success(request, "Course created successfully.")
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.is_admin_user() and (not request.user.is_tutor() or course.tutor != request.user):
        messages.error(request, "You don't have permission to delete this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        # Delete associated lessons
        course.lessons.all().delete()
        course.delete()
        messages.success(request, "Course and associated lessons deleted successfully.")
        return redirect('course_list')
    
    return render(request, 'courses/delete_course_confirm.html', {'course': course})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.is_admin_user() and (not request.user.is_tutor() or course.tutor != request.user):
        messages.error(request, "You don't have permission to edit this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'course': course})

@login_required
def create_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not (request.user.is_admin_user or (request.user.is_tutor and course.tutor == request.user)):
        messages.error(request, "You don't have permission to add lessons to this course.")
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added successfully.")
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {'form': form, 'course': course})

@login_required
def delete_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.user.is_admin_user or (request.user.is_tutor and course.tutor == request.user):
        if request.method == 'POST':
            lesson.delete()
            messages.success(request, f'Lesson "{lesson.title}" has been deleted.')
            return redirect('course_detail', course_id=course.id)
        else:
            return render(request, 'courses/delete_lesson_confirm.html', {'course': course, 'lesson': lesson})
    else:
        messages.error(request, 'You do not have permission to delete this lesson.')
        return redirect('course_detail', course_id=course.id)

def category_courses(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_courses.html', {'category': category, 'courses': courses})

@login_required
def edit_lesson(request, course_id ,lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if not request.user.is_admin_user() and (not request.user.is_tutor() or course.tutor != request.user):
        messages.error(request, "You don't have permission to edit this lesson.")
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully.")
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/edit_lesson.html', {'form': form, 'course': course, 'lesson': lesson})