from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib import messages

from .forms import NewCourseForm
from .models import GradeColumn

from students.models import Student
from courses.models import Course
# Create your views here.


def course_create(request):
    if request.method == 'POST':
        form = NewCourseForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect()
    else:
        form = NewCourseForm()
    return render(
        request,
        'course_create.html',
        {
            "form": form,
        }
    )


class CourseGradeView(DetailView):
    model = GradeColumn
    template_name = "course_grade.html"
    context_object_name = "grade"


def enroll_student_to_course(request, course_id, student_id):
    course = Course.objects.get(pk=course_id)
    student = Student.objects.get(pk=student_id)
    course.students.add(student)
    course.save()
    messages.success(request, 'The student is successfuly added.')
    return redirect('/')
