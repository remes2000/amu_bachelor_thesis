from django.db.models.functions import Concat
from django.db.models import Value
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.template import loader, RequestContext
from .models import User, Student, Lecturer, Thesis
from django.utils import timezone
from django.utils.http import urlencode


def login_redirect(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.user.role == User.SUPERUSER:
        return HttpResponseRedirect(reverse('admin:index'))
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:home'))


class StudentProfile(generic.DetailView):
    model = Student
    template_name = 'amu_bachelor_thesis_app/profile/student_profile.html'


class LecturerProfile(generic.DetailView):
    model = Lecturer
    template_name = 'amu_bachelor_thesis_app/profile/lecturer_profile.html'


class ManageThesis(generic.ListView):
    model = Thesis
    paginate_by = 10
    template_name = 'amu_bachelor_thesis_app/thesis/manage_thesis.html'

    def get_queryset(self):
        return Thesis.objects.filter(lecturer_id=self.request.user.id).order_by('-edited_at', '-created_at')


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


def edit_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if request.method == "GET":
        return render(request, 'amu_bachelor_thesis_app/thesis/edit_thesis.html', {'thesis': thesis})
    if request.method == "POST":
        title = request.POST.get('thesis_title')
        if not title:
            return HttpResponse('Title is required', 400)
        description = request.POST.get('thesis_description')
        thesis.title = title
        thesis.description = description
        thesis.edited_at = timezone.now()
        thesis.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))
    else:
        return HttpResponse('Method not allowed', status=405)


def create_thesis(request):
    if request.method == 'GET':
        template = loader.get_template('amu_bachelor_thesis_app/thesis/create_thesis.html')
        return HttpResponse(template.render(None, request))
    elif request.method == 'POST':
        title = request.POST.get('thesis_title')
        if not title:
            return HttpResponse('Title is required', 400)
        description = request.POST.get('thesis_description')
        new_thesis = Thesis(title=title, description=description, created_at=timezone.now())
        new_thesis.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))
    else:
        return HttpResponse('Method not allowed', status=405)


class ThesisView(generic.DetailView):
    model = Thesis
    template_name = "amu_bachelor_thesis_app/thesis/thesis.html"


def select_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if request.user.student.has_thesis():
        return HttpResponse('Student has thesis', status=401)
    thesis.student = request.user.student
    thesis.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


def unselect_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    thesis.student = None
    thesis.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


