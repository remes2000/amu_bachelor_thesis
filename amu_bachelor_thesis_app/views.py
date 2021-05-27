from django.db.models.functions import Concat
from django.db.models import Value
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.template import loader, RequestContext
from .models import User, Student, Lecturer, Thesis, ThesisProposition
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
    template_name = 'amu_bachelor_thesis_app/student/student_profile.html'


class LecturerProfile(generic.DetailView):
    model = Lecturer
    template_name = 'amu_bachelor_thesis_app/lecturer/lecturer_profile.html'


def edit_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
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
        if not description:
            description = ''
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
        if not description:
            description = ''
        new_thesis = Thesis(title=title, description=description, created_at=timezone.now(), lecturer=request.user.lecturer)
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
    request.user.student.discard_all_propositions()
    thesis.student = request.user.student
    thesis.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


def unselect_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    thesis.student = None
    thesis.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:thesis', args=(thesis_id,)))


def remove_thesis(request, thesis_id):
    thesis = get_object_or_404(Thesis, pk=thesis_id)
    if thesis.student_id:
        return HttpResponse('Thesis has student', status=401)
    thesis.delete()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis'))


class ManageThesisPropositions(generic.ListView):
    model = ThesisProposition
    paginate_by = 10
    template_name = 'amu_bachelor_thesis_app/thesis_proposition/manage_thesis_propositions.html'

    def get_queryset(self):
        return ThesisProposition.objects.filter(student_id=self.request.user.id).order_by('-edited_at', '-created_at')


def create_thesis_proposition(request):
    if request.method == 'GET':
        lecturers = Lecturer.objects.all()
        return render(request,
                      'amu_bachelor_thesis_app/thesis_proposition/create_thesis_proposition.html',
                      {'lecturers': lecturers})
    elif request.method == 'POST':
        if request.user.student.has_thesis():
            return HttpResponse("Student has thesis", 401)
        title = request.POST.get('thesis_proposition_title')
        if not title:
            return HttpResponse('Title is required', 400)
        lecturer_id = request.POST.get('thesis_proposition_lecturer_id')
        lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
        description = request.POST.get('thesis_description')
        if not description:
            description = ''
        new_thesis_proposition = ThesisProposition(title=title, description=description, created_at=timezone.now(),
                                                   lecturer=lecturer, student=request.user.student, is_active=True)
        new_thesis_proposition.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))
    else:
        return HttpResponse('Method not allowed', status=405)


def edit_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if request.method == 'GET':
        lecturers = Lecturer.objects.all()
        return render(request,
                      'amu_bachelor_thesis_app/thesis_proposition/edit_thesis_proposition.html',
                      {'lecturers': lecturers, 'thesis_proposition': thesis_proposition})
    elif request.method == 'POST':
        title = request.POST.get('thesis_proposition_title')
        if not title:
            return HttpResponse('Title is required', 400)
        description = request.POST.get('thesis_proposition_description')
        if not description:
            description = ''
        thesis_proposition.title = title
        thesis_proposition.description = description
        thesis_proposition.edited_at = timezone.now()
        thesis_proposition.save()
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))
    else:
        return HttpResponse('Method not allowed', status=405)


def lecturer_manage_thesis_proposition(request):
    lecturer = request.user.lecturer
    students = Student.objects.filter(thesisproposition__lecturer_id=lecturer, thesisproposition__is_active=True).distinct()
    thesis_propositions_dictionary = {}
    for student in students:
        thesis_propositions_dictionary[student.user_id] = ThesisProposition.objects.filter(student_id=student.user_id, lecturer_id=lecturer.user_id, is_active=True)
    template_name = 'amu_bachelor_thesis_app/thesis_proposition/lecturer_manage_thesis_propositions.html'
    return render(request, template_name, {
        'students': students,
        'thesis_propositions_dictionary': thesis_propositions_dictionary
    })


class ThesisPropositionView(generic.DetailView):
    model = ThesisProposition
    template_name = "amu_bachelor_thesis_app/thesis_proposition/thesis_proposition.html"
    context_object_name = 'thesis_proposition'


def lecturer_accept_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    student = thesis_proposition.student
    thesis = thesis_proposition.get_thesis()
    thesis.save()
    thesis_proposition.delete()
    student.discard_all_propositions()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:lecturer_manage_thesis_propositions'))


def lecturer_discard_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    thesis_proposition.is_active = False
    thesis_proposition.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:lecturer_manage_thesis_propositions'))


def student_discard_own_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    thesis_proposition.is_active = False
    thesis_proposition.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))


def student_resend_own_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if request.student.has_thesis():
        return HttpResponse("Student has thesis", 401)
    thesis_proposition.is_active = True
    thesis_proposition.save()
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))