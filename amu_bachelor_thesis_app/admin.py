from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.core.exceptions import ValidationError

from .models import User, Lecturer, Student


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'role')


class StudentInline(admin.TabularInline):
    model = Student


class LecturerInline(admin.TabularInline):
    model = Lecturer


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'role',)
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'role',)}),
    )
    inlines = [StudentInline, LecturerInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password', 'password_confirm'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'role')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.unregister(Group)