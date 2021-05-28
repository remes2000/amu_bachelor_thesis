from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from amu_bachelor_thesis_app.models import Student


@method_decorator(login_required, name='dispatch')
class StudentProfile(generic.DetailView):
    model = Student
    template_name = 'amu_bachelor_thesis_app/student/student_profile.html'
