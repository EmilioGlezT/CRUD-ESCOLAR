from django import forms
from .models import Student, Subject
from django.contrib.auth.models import User


# class StudentForm(forms.ModelForm):
#     # Campos adicionales para el usuario
#     username = forms.CharField(label='Nombre de usuario')
#     email = forms.EmailField(label='Correo electrónico')
#     password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

#     class Meta:
#         model = Student
#         fields = ['user', 'student_id']
#         exclude = ['user']  # Reemplaza con los campos de tu modelo Student

#     def save(self, commit=True):
#         # Crear usuario asociado
#         user = User(
#             username=self.cleaned_data['username'],
#             email=self.cleaned_data['email']
#         )
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()

#         # Crear estudiante asociado al usuario
#         student = super().save(commit=False)
#         student.user = user
#         if commit:
#             student.save()
#         return student
# class StudentForm(forms.ModelForm):
#     # Campos adicionales para el usuario
#     username = forms.CharField(label='Nombre de usuario')
#     email = forms.EmailField(label='Correo electrónico')
#     password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)

#     class Meta:
#         model = Student
#         fields = ['user', 'student_id']
#         exclude = ['user']  # Reemplaza con los campos de tu modelo Student

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Si estamos editando un estudiante, pre-cargamos los datos del usuario
#         if self.instance and self.instance.user:
#             self.fields['username'].initial = self.instance.user.username
#             self.fields['email'].initial = self.instance.user.email

#     def save(self, commit=True):
#         # Obtener el objeto User asociado al estudiante
#         user = self.instance.user if self.instance and self.instance.user else User()

#         # Si se proporcionaron nuevos datos de usuario, actualízalos
#         if self.cleaned_data['username']:
#             user.username = self.cleaned_data['username']
#         if self.cleaned_data['email']:
#             user.email = self.cleaned_data['email']
#         if self.cleaned_data.get('password'):
#             user.set_password(self.cleaned_data['password'])

#         if commit:
#             user.save()

#         # Crear o actualizar el estudiante
#         student = super().save(commit=False)
#         student.user = user
#         if commit:
#             student.save()

#         return student

class StudentForm(forms.ModelForm):
    # Campos adicionales para el usuario
    username = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = Student
        fields = ['user', 'student_id']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo intentar acceder al usuario si ya existe
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Si es un nuevo estudiante, el 'user' estará vacío.
        user = self.instance.user if self.instance and self.instance.pk else None

        # Si no existe un 'user', crear uno nuevo
        if not user:
            user = User()

        # Si se proporcionaron nuevos datos de usuario, actualizarlos
        if self.cleaned_data['username']:
            user.username = self.cleaned_data['username']
        if self.cleaned_data['email']:
            user.email = self.cleaned_data['email']
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        # Crear o actualizar el estudiante
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()

        return student


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
