from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, role, password):
        email = self.normalize_email(email)
        user = self.model(email=email, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email, role=User.SUPERUSER)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    LECTURER = 1
    STUDENT = 2
    SUPERUSER = 3

    ROLE_CHOICES = (
        (LECTURER, 'Lecturer'),
        (STUDENT, 'Student'),
        (SUPERUSER, 'Superuser')
    )

    objects = CustomUserManager()
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False)
    email = models.EmailField('email address', blank=False, null=False, unique=True)

    def __str__(self):
        if self.role == User.STUDENT:
            return str(self.student)
        if self.role == User.LECTURER:
            return str(self.lecturer)
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_student(self):
        return self.role == User.STUDENT

    def is_lecturer(self):
        return self.role == User.LECTURER

    @property
    def is_staff(self):
        return self.role == self.SUPERUSER

    @property
    def is_superuser(self):
        return self.role == self.SUPERUSER


class Lecturer(models.Model):
    first_name = models.CharField(max_length=180, blank=False, null=False)
    last_name = models.CharField(max_length=180, blank=False, null=False)
    degree = models.CharField(max_length=180, blank=True, null=True)
    interests = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def name_with_degree(self):
        return self.degree + ' ' + self.first_name + ' ' + self.last_name


class Student(models.Model):
    first_name = models.CharField(max_length=180, blank=False, null=False)
    last_name = models.CharField(max_length=180, blank=False, null=False)
    album_number = models.CharField(max_length=6, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_thesis(self):
        return self.thesis is not None


class Thesis(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=4000, blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    edited_at = models.DateTimeField(null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, null=False)
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
