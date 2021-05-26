from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = 'amu_bachelor_thesis'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='amu_bachelor_thesis_app/home.html'), name='home'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
    path('student/<int:pk>/profile', views.StudentProfile.as_view(), name='student_profile'),
    path('lecturer/<int:pk>/profile', views.LecturerProfile.as_view(), name='lecturer_profile'),
    path('manage_thesis', views.ManageThesis.as_view(), name='manage_thesis'),
    path('thesis/create', views.create_thesis, name='create_thesis'),
    path('thesis/edit/<int:thesis_id>', views.edit_thesis, name="edit_thesis"),
    path('search_engine', views.ThesisSearchEngine.as_view(), name="search_engine"),
    path('thesis/<int:pk>', views.ThesisView.as_view(), name="thesis"),
    path('thesis/<int:thesis_id>/select', views.select_thesis, name="select_thesis"),
    path('thesis/<int:thesis_id>/unselect', views.unselect_thesis, name="unselect_thesis")
]