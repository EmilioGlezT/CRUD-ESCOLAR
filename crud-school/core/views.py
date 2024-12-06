from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Enrollment
from .forms import StudentForm, SubjectForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')
    


class AlumnosListView(ListView):
    model = Student
    template_name="student_list.html"


# CRUD Alumnos
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')

# CRUD Materias (Similar lógica)
@login_required
def enroll_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        Enrollment.objects.create(student_id=student_id, subject_id=subject_id)
        return redirect('enrollment_list')

    students = Student.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'enroll_student.html', {'students': students, 'subjects': subjects})

@login_required
def grade_student(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        grade = request.POST.get('grade')
        enrollment.grade = grade
        enrollment.save()
        return redirect('enrollment_list')

    return render(request, 'grade_student.html', {'enrollment': enrollment})

# CRUD Materias
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/subject_form.html', {'form': form})

@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subjects/subject_form.html', {'form': form})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect('subject_list')


#Enrollment
@login_required
def enrollment_list(request):
    # Obtener todas las inscripciones y ordenarlas por materia
    enrollments = Enrollment.objects.all().order_by('subject__name')

    # Agrupar las inscripciones por materia
    grouped_enrollments = {}
    for enrollment in enrollments:
        if enrollment.subject.name not in grouped_enrollments:
            grouped_enrollments[enrollment.subject.name] = []
        grouped_enrollments[enrollment.subject.name].append(enrollment)

    return render(request, 'enrollment/enrollment_list.html', {'grouped_enrollments': grouped_enrollments})
