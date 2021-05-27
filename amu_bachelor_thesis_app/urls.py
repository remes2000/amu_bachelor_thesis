from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = 'amu_bachelor_thesis'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='amu_bachelor_thesis_app/home.html'), name='home'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
    path('student/<int:pk>', views.StudentProfile.as_view(), name='student_profile'),
    path('lecturer/<int:pk>', views.LecturerProfile.as_view(), name='lecturer_profile'),
    path('lecturer/<int:lecturer_id>/edit', views.edit_lecturer, name='edit_lecturer'),
    path('manage_thesis', views.ManageThesis.as_view(), name='manage_thesis'),
    path('thesis/create', views.create_thesis, name='create_thesis'),
    path('thesis/edit/<int:thesis_id>', views.edit_thesis, name="edit_thesis"),
    path('search_engine', views.ThesisSearchEngine.as_view(), name="search_engine"),
    path('thesis/<int:pk>', views.ThesisView.as_view(), name="thesis"),
    path('thesis/<int:thesis_id>/select', views.select_thesis, name="select_thesis"),
    path('thesis/<int:thesis_id>/unselect', views.unselect_thesis, name="unselect_thesis"),
    path('thesis/<int:thesis_id>/remove', views.remove_thesis, name="remove_thesis"),
    path('thesis_proposition/<int:pk>', views.ThesisPropositionView.as_view(), name="thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/accept', views.lecturer_accept_thesis_proposition, name="accept_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/discard', views.lecturer_discard_thesis_proposition, name="discard_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/discard_own', views.student_discard_own_thesis_proposition, name="discard_own_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/resend', views.student_resend_own_thesis_proposition, name="resend_thesis_proposition"),
    path('manage_thesis_propositions', views.ManageThesisPropositions.as_view(), name="manage_thesis_propositions"),
    path('thesis_proposition/create', views.create_thesis_proposition, name='create_thesis_proposition'),
    path('thesis_proposition/<int:thesis_proposition_id>/edit', views.edit_thesis_proposition, name='edit_thesis_proposition'),
    path('lecturer_manage_thesis_propositions', views.lecturer_manage_thesis_proposition, name='lecturer_manage_thesis_propositions'),
]