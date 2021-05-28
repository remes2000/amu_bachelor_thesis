from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import thesis_views, thesis_propositions_views, notifications_views, lecturer_views, students_views, \
    auth_views

app_name = 'amu_bachelor_thesis'
urlpatterns = [
    path('', TemplateView.as_view(template_name='amu_bachelor_thesis_app/home.html'), name='home'),
    # AUTH ROUTES
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_redirect', auth_views.login_redirect, name='login_redirect'),
    # STUDENT ROUTES
    path('student/<int:pk>', students_views.StudentProfile.as_view(), name='student_profile'),
    # LECTURER ROUTES
    path('lecturer/<int:pk>', lecturer_views.LecturerProfile.as_view(), name='lecturer_profile'),
    path('lecturer/edit', lecturer_views.edit_lecturer, name='edit_lecturer'),
    # THESIS ROUTES
    path('manage_thesis', thesis_views.ManageThesis.as_view(), name='manage_thesis'),
    path('thesis/create', thesis_views.create_thesis, name='create_thesis'),
    path('thesis/edit/<int:thesis_id>', thesis_views.edit_thesis, name="edit_thesis"),
    path('search_engine', thesis_views.ThesisSearchEngine.as_view(), name="search_engine"),
    path('thesis/<int:pk>', thesis_views.ThesisView.as_view(), name="thesis"),
    path('thesis/<int:thesis_id>/select', thesis_views.select_thesis, name="select_thesis"),
    path('thesis/<int:thesis_id>/unselect', thesis_views.unselect_thesis, name="unselect_thesis"),
    path('thesis/<int:thesis_id>/remove', thesis_views.remove_thesis, name="remove_thesis"),
    # THESIS PROPOSITION ROUTES
    path('thesis_proposition/<int:pk>', thesis_propositions_views.ThesisPropositionView.as_view(), name="thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/accept', thesis_propositions_views.lecturer_accept_thesis_proposition, name="accept_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/discard', thesis_propositions_views.lecturer_discard_thesis_proposition, name="discard_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/discard_own', thesis_propositions_views.student_discard_own_thesis_proposition, name="discard_own_thesis_proposition"),
    path('thesis_proposition/<int:thesis_proposition_id>/resend', thesis_propositions_views.student_resend_own_thesis_proposition, name="resend_thesis_proposition"),
    path('manage_thesis_propositions', thesis_propositions_views.ManageThesisPropositions.as_view(), name="manage_thesis_propositions"),
    path('thesis_proposition/create', thesis_propositions_views.create_thesis_proposition, name='create_thesis_proposition'),
    path('thesis_proposition/<int:thesis_proposition_id>/edit', thesis_propositions_views.edit_thesis_proposition, name='edit_thesis_proposition'),
    path('lecturer_manage_thesis_propositions', thesis_propositions_views.lecturer_manage_thesis_proposition, name='lecturer_manage_thesis_propositions'),
    # NOTIFICATION ROUTES
    path('notifications', notifications_views.NotificationsView.as_view(), name='notifications'),
    path('notifications/history', notifications_views.NotificationsHistoryView.as_view(), name='notifications_history'),
    path('notifications_getcounter', notifications_views.notifications_get_counter, name='notifications_get_counter')
]