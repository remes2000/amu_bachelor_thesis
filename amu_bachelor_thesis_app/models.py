from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


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
        try:
            return self.thesis is not None
        except AttributeError:
            return False

    def discard_all_propositions(self):
        propositions_to_discard = ThesisProposition.objects.filter(student_id=self.user_id, is_active=True)
        for proposition in propositions_to_discard:
            proposition.is_active = False
            proposition.save()


class Thesis(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=4000, blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    edited_at = models.DateTimeField(null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, null=False)
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class ThesisProposition(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=4000, blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    edited_at = models.DateTimeField(null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False)

    def __str__(self):
        return self.title

    def get_thesis(self):
        return Thesis(title=self.title, description=self.description, created_at=timezone.now(), lecturer=self.lecturer, student=self.student)


class Notification(models.Model):
    STUDENT_CREATED_PROPOSITION = 1
    STUDENT_DISCARDED_PROPOSITION = 2
    STUDENT_EDITED_PROPOSITION = 3
    STUDENT_SELECTED_THESIS = 4
    STUDENT_UNSELECTED_THESIS = 5
    LECTURER_EDITED_THESIS = 51
    LECTURER_ACCEPTED_PROPOSITION = 52
    LECTURER_DISCARDED_PROPOSITION = 53

    TYPE_CHOICES = (
        (STUDENT_CREATED_PROPOSITION, 'STUDENT_CREATED_PROPOSITION'),
        (STUDENT_DISCARDED_PROPOSITION, 'STUDENT_DISCARDED_PROPOSITION'),
        (STUDENT_EDITED_PROPOSITION, 'STUDENT_EDITED_PROPOSITION'),
        (STUDENT_SELECTED_THESIS, 'STUDENT_SELECTED_THESIS'),
        (STUDENT_UNSELECTED_THESIS, 'STUDENT_UNSELECTED_THESIS'),
        (LECTURER_EDITED_THESIS, 'LECTURER_EDITED_THESIS'),
        (LECTURER_ACCEPTED_PROPOSITION, 'LECTURER_ACCEPTED_PROPOSITION'),
        (LECTURER_DISCARDED_PROPOSITION, 'LECTURER_DISCARDED_PROPOSITION')
    )

    date = models.DateTimeField(null=False)
    is_seen = models.BooleanField(null=False)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, blank=False, null=False)
    thesis = models.ForeignKey(Thesis, on_delete=models.SET_NULL, null=True)
    thesis_proposition = models.ForeignKey(ThesisProposition, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

