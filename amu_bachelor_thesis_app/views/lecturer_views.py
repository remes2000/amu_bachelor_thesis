from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from amu_bachelor_thesis_app.models import Lecturer


@method_decorator(login_required, name='dispatch')
class LecturerProfile(generic.DetailView):
    model = Lecturer
    template_name = 'amu_bachelor_thesis_app/lecturer/lecturer_profile.html'


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def edit_lecturer(request):
    lecturer = request.user.lecturer
    if request.method == 'GET':
        return render(request, 'amu_bachelor_thesis_app/lecturer/edit_lecturer.html', {'lecturer': lecturer})
    elif request.method == 'POST':
        lecturer_degree = request.POST.get('lecturer_degree')
        lecturer_description = request.POST.get('lecturer_description')
        lecturer_interests = request.POST.get('lecturer_interests')
        lecturer.degree = lecturer_degree
        lecturer.description = lecturer_description
        lecturer.interests = lecturer_interests
        lecturer.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:lecturer_profile', args=(lecturer.user_id,)))
    else:
        return HttpResponse('Method not allowed', status=405)