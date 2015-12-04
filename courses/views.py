from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages

from .forms import NewCourseForm, GradeForm


from students.models import Student
from courses.models import Course, CourseAnnouncement, Grade, GradeColumn
# Create your views here.


def course_create(request):
    if request.method == 'POST':
        form = NewCourseForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("/")
    else:
        form = NewCourseForm()
    return render(
        request,
        'course_create.html',
        {
            "form": form,
        }
    )


def list_course_grade_column(request, course_id):
    course_obj = get_object_or_404(Course, pk=course_id)
    qs = course_obj.gradecolumn_set.all()

    return render(request, "course_grade.html",
        {
            'course': course_obj,
            'gradecolumns': qs,
        }
    )


def enroll_student_to_course(request, course_id, student_id):
    course = Course.objects.get(pk=course_id)
    student = Student.objects.get(pk=student_id)
    course.students.add(student)
    course.save()
    messages.success(request, 'The student is successfuly added.')
    return redirect('/')

def post_student_grade(request, course_id, student_id, gradecolumn_id):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('/')
    else:
        form = GradeForm(initial={'column': gradecolumn_id,
                                  'student': student_id})
    return render(
        request,
        'post_student_grade.html',
        {
            'form': form,
            'course_id': course_id,
            'student_id': student_id,
            'gradecolumn_id': gradecolumn_id,
        }
    )
def list_student_grade(request, course_id, student_id):
    course_obj = get_object_or_404(Course, pk=course_id)
    gradecolumns = course_obj.gradecolumn_set.all()
    student = get_object_or_404(Student, pk=student_id)
    grades = student.grade_set.all()
    grade = get_list_or_404(Grade, student__course=course_id)

    student_grade_value = []
    student_grade_column = []
    for g in gradecolumns:
        student_grade_column.append(g.name)
    return render(
        request,
        'list_student_grade.html',
        {

            'course_id': course_id,
            'student_id': student_id,
            'student_grade_column': student_grade_column,
            'student': student,
            'grades': grades
        }
    )

def instructor_view_course_stundets_announcments(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = Student.objects.filter(course__pk=course_id)
    announcments = CourseAnnouncement.objects.filter(course__pk=course_id)
    return render(request, "course_details_announcments.html",
                  {
                      'course': course,
                      'students': students,
                      'announcments': announcments
                  }
                  )
