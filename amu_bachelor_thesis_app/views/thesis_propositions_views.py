from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from amu_bachelor_thesis_app.models import ThesisProposition, Lecturer, Student
from amu_bachelor_thesis_app.notification_helper import NotificationHelper


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_student()), name='dispatch')
class ManageThesisPropositions(generic.ListView):
    model = ThesisProposition
    paginate_by = 10
    template_name = 'amu_bachelor_thesis_app/thesis_proposition/manage_thesis_propositions.html'

    def get_queryset(self):
        return ThesisProposition.objects.filter(student_id=self.request.user.id).order_by('-edited_at', '-created_at')


@login_required
@method_decorator(user_passes_test(lambda user: user.is_student()), name='dispatch')
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
        NotificationHelper.send_student_created_proposition_notification(new_thesis_proposition)
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))
    else:
        return HttpResponse('Method not allowed', status=405)


@login_required
@user_passes_test(lambda user: user.is_student())
def edit_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if thesis_proposition.student != request.user.student:
        return HttpResponse('Permission denied', 403)
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
        if thesis_proposition.is_active:
            NotificationHelper.send_student_edited_proposition_notification(thesis_proposition)
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))
    else:
        return HttpResponse('Method not allowed', status=405)


@login_required
@user_passes_test(lambda user: user.is_lecturer())
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


@method_decorator(login_required, name='dispatch')
class ThesisPropositionView(generic.DetailView):
    model = ThesisProposition
    template_name = "amu_bachelor_thesis_app/thesis_proposition/thesis_proposition.html"
    context_object_name = 'thesis_proposition'


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def lecturer_accept_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if thesis_proposition.lecturer != request.user.lecturer:
        return HttpResponse('Permission denied', 403)
    student = thesis_proposition.student
    thesis = thesis_proposition.get_thesis()
    thesis.save()
    thesis_proposition.delete()
    student.discard_all_propositions()
    NotificationHelper.send_lecturer_accepted_proposition_notification(thesis)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:lecturer_manage_thesis_propositions'))


@login_required
@user_passes_test(lambda user: user.is_lecturer())
def lecturer_discard_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if thesis_proposition.lecturer != request.user.lecturer:
        return HttpResponse('Permission denied', 403)
    thesis_proposition.is_active = False
    thesis_proposition.save()
    NotificationHelper.send_lecturer_discarded_proposition_notification(thesis_proposition)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:lecturer_manage_thesis_propositions'))


@login_required
@user_passes_test(lambda user: user.is_student())
def student_discard_own_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if thesis_proposition.student != request.user.student:
        return HttpResponse('Permission denied', 403)
    thesis_proposition.is_active = False
    thesis_proposition.save()
    NotificationHelper.send_student_discard_proposition_notification(thesis_proposition)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))


@login_required
@user_passes_test(lambda user: user.is_student())
def student_resend_own_thesis_proposition(request, thesis_proposition_id):
    thesis_proposition = get_object_or_404(ThesisProposition, pk=thesis_proposition_id)
    if thesis_proposition.student != request.user.student:
        return HttpResponse('Permission denied', 403)
    if request.user.student.has_thesis():
        return HttpResponse("Student has thesis", 401)
    thesis_proposition.is_active = True
    thesis_proposition.save()
    NotificationHelper.send_student_created_proposition_notification(thesis_proposition)
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:manage_thesis_propositions'))
