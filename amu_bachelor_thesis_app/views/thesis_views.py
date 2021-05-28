from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import Concat
from django.db.models import Value
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse
from django.template import loader, RequestContext
from django.utils import timezone
from amu_bachelor_thesis_app.models import Thesis
from amu_bachelor_thesis_app.notification_helper import NotificationHelper


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_lecturer()), name='dispatch')
class ManageThesis(generic.ListView):
    model = Thesis
    paginate_by = 10
    template_name = 'amu_bachelor_thesis_app/thesis/manage_thesis.html'

    def get_queryset(self):
        return Thesis.objects.filter(lecturer_id=self.request.user.id).order_by('-edited_at', '-created_at')


@method_decorator(login_required, name='dispatch')
class ThesisSearchEngine(generic.ListView):
    model = Thesis
    paginate_by = 15
    template_name = 'amu_bachelor_thesis_app/search_engine.html'

    def get_queryset(self):
        search_title = self.request.GET.get('thesis_title')
        if search_title is None:
            search_title = ''
        search_lecturer = self.request.GET.get('thesis_lecturer')
        if search_lecturer is None:
            search_lecturer = ''
        search_include_already_selected = self.request.GET.get('include_already_selected') == 'on'
        queryset = Thesis.objects.annotate(
            lecturer_name_with_degree=Concat('lecturer__degree', Value(' '),
                                             'lecturer__first_name', Value(' '),
                                             'lecturer__last_name')
        )
        if search_include_already_selected:
            return queryset.filter(
                title__icontains=search_title,
                lecturer_name_with_degree__icontains=search_lecturer)
        else:
            return queryset.filter(
                title__icontains=search_title,
                lecturer_name_with_degree__icontains=search_lecturer,
                student_id__isnull=True)


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def edit_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if thesis.lecturer != request.user.lecturer:
        return HttpResponse('Permission denied', 403)
    if request.method == "GET":
        return render(request, 'amu_bachelor_thesis_app/thesis/edit_thesis.html', {'thesis': thesis})
    if request.method == "POST":
        title = request.POST.get('thesis_title')
        if not title:
            return HttpResponse('Title is required', 400)
        description = request.POST.get('thesis_description')
        if not description:
            description = ''
        thesis.title = title
        thesis.description = description
        thesis.edited_at = timezone.now()
        thesis.save()
        if thesis.student:
            NotificationHelper.send_lecturer_edited_thesis_notification(thesis)
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))
    else:
        return HttpResponse('Method not allowed', status=405)


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def create_thesis(request):
    if request.method == 'GET':
        template = loader.get_template('amu_bachelor_thesis_app/thesis/create_thesis.html')
        return HttpResponse(template.render(None, request))
    elif request.method == 'POST':
        title = request.POST.get('thesis_title')
        if not title:
            return HttpResponse('Title is required', 400)
        description = request.POST.get('thesis_description')
        if not description:
            description = ''
        new_thesis = Thesis(title=title, description=description, created_at=timezone.now(), lecturer=request.user.lecturer)
        new_thesis.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))
    else:
        return HttpResponse('Method not allowed', status=405)


@method_decorator(login_required, name='dispatch')
class ThesisView(generic.DetailView):
    model = Thesis
    template_name = "amu_bachelor_thesis_app/thesis/thesis.html"


@login_required
@user_passes_test(lambda user: user.is_student())
def select_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if request.user.student.has_thesis():
        return HttpResponse('Student has thesis', status=400)
    if thesis.student is not None:
        return HttpResponse('Thesis is selected', status=400)
    request.user.student.discard_all_propositions()
    thesis.student = request.user.student
    thesis.save()
    NotificationHelper.send_student_selected_thesis_notification(thesis)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


@login_required
@user_passes_test(lambda user: user.is_student())
def unselect_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    student = thesis.student
    if thesis.student is None:
        return HttpResponse('Thesis is not selected by any student', status=400)
    if thesis.student != request.user.student:
        return HttpResponse('Permission denied', student=403)
    thesis.student = None
    thesis.save()
    NotificationHelper.send_student_unselected_thesis_notification(student, thesis)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def remove_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if thesis.lecturer != request.user.lecturer:
        return HttpResponse('Permission denied', 403)
    if thesis.student_id:
        return HttpResponse('Thesis has student', status=400)
    thesis.delete()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))