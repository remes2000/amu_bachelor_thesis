import datetime
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from amu_bachelor_thesis_app.models import Thesis, Lecturer, User, Student, ThesisProposition, Notification


def create_lecturer():
    user_email = str(uuid.uuid4()) + '@email.pl'
    user = User.objects.create(email=user_email, role=User.LECTURER)
    return Lecturer.objects.create(first_name="John", last_name="Test", degree="PhD",
                                   interests="NA", description="NA", user=user)


def create_student():
    user_email = str(uuid.uuid4()) + '@email.pl'
    user = User.objects.create(email=user_email, role=User.STUDENT)
    return Student.objects.create(first_name="John", last_name="Test", user=user)


def create_thesis(lecturer, student=None, title=str(uuid.uuid4()), created_at=timezone.now(), edited_at=timezone.now()):
    return Thesis.objects.create(title=title, created_at=created_at, edited_at=edited_at,
                                 lecturer=lecturer, student=student)


def create_thesis_proposition(student, lecturer, title=str(uuid.uuid4()), created_at=timezone.now(), edited_at=timezone.now(), is_active=True):
    return ThesisProposition.objects.create(title=title, created_at=created_at,
                                            edited_at=edited_at, lecturer=lecturer, student=student, is_active=is_active)


class ManageThesisViewTests(TestCase):
    def test_thesis_order(self):
        lecturer = create_lecturer()
        self.client.force_login(lecturer.user, backend=None)
        thesis1 = create_thesis(title="Thesis1",
                                created_at=timezone.now() - datetime.timedelta(days=5),
                                edited_at=timezone.now(), lecturer=lecturer)
        thesis2 = create_thesis(title="Thesis2",
                                created_at=timezone.now() - datetime.timedelta(days=4),
                                edited_at=timezone.now() - datetime.timedelta(minutes=15), lecturer=lecturer)
        thesis3 = create_thesis(title="Thesis3",
                                created_at=timezone.now(),
                                edited_at=None, lecturer=lecturer)
        response = self.client.get(reverse('amu_bachelor_thesis:manage_thesis'))
        query_set = response.context['page_obj']
        self.assertEqual(query_set[0].id, thesis1.id)
        self.assertEqual(query_set[1].id, thesis2.id)
        self.assertEqual(query_set[2].id, thesis3.id)

    def test_thesis_from_logged_lecturer(self):
        main_lecturer = create_lecturer()
        different_lecturer = create_lecturer()
        self.client.force_login(main_lecturer.user)
        create_thesis(title='MainLecturerThesis1', lecturer=main_lecturer)
        create_thesis(title='MainLecturerThesis2', lecturer=main_lecturer)
        not_included_thesis = create_thesis(title='DifferentLecturerThesis', lecturer=different_lecturer)
        response = self.client.get(reverse('amu_bachelor_thesis:manage_thesis'))
        query_set = response.context['page_obj']
        included_thesis_ids = map(lambda q: q.id, query_set)
        self.assertNotIn(not_included_thesis.id, included_thesis_ids)


class NotificationTests(TestCase):
    def test_student_create_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        self.client.force_login(student.user)
        self.client.post(reverse('amu_bachelor_thesis:create_thesis_proposition'), {
            'thesis_proposition_title': 'Test',
            'thesis_proposition_description': 'Description',
            'thesis_proposition_lecturer_id': lecturer.user.id
        })
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_CREATED_PROPOSITION,
                                                   thesis_proposition_id__isnull=False).first()
        self.assertIsNotNone(notification)

    def test_student_create_proposition_on_resend_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(student=student, lecturer=lecturer, is_active=False)
        self.client.force_login(student.user)
        self.client.get(reverse('amu_bachelor_thesis:resend_thesis_proposition', args=(thesis_proposition.id,)))
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_CREATED_PROPOSITION,
                                                   thesis_proposition_id__isnull=False).first()
        self.assertIsNotNone(notification)

    def test_student_discard_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(student=student, lecturer=lecturer)
        self.client.force_login(student.user)
        self.client.get(reverse('amu_bachelor_thesis:discard_own_thesis_proposition', args=(thesis_proposition.id,)))
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_DISCARDED_PROPOSITION,
                                                   thesis_proposition=thesis_proposition).first()
        self.assertIsNotNone(notification)

    def test_student_edited_active_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(student=student, lecturer=lecturer, is_active=True)
        self.client.force_login(student.user)
        self.client.post(reverse('amu_bachelor_thesis:edit_thesis_proposition', args=(thesis_proposition.id,)), {
            'thesis_proposition_title': 'random_title'
        })
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_EDITED_PROPOSITION,
                                                   thesis_proposition=thesis_proposition).first()
        self.assertIsNotNone(notification)

    def test_student_edited_inactive_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(student=student, lecturer=lecturer, is_active=False)
        self.client.force_login(student.user)
        self.client.post(reverse('amu_bachelor_thesis:edit_thesis_proposition', args=(thesis_proposition.id,)), {
            'thesis_proposition_title': 'random_title'
        })
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_EDITED_PROPOSITION,
                                                   thesis_proposition=thesis_proposition).first()
        self.assertIsNone(notification)

    def test_student_selected_thesis_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis = create_thesis(lecturer=lecturer)
        self.client.force_login(student.user)
        self.client.get(reverse('amu_bachelor_thesis:select_thesis', args=(thesis.id,)))
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_SELECTED_THESIS,
                                                   thesis=thesis).first()
        self.assertIsNotNone(notification)

    def test_student_unselected_thesis_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis = create_thesis(lecturer=lecturer, student=student)
        self.client.force_login(student.user)
        self.client.get(reverse('amu_bachelor_thesis:unselect_thesis', args=(thesis.id,)))
        notification = Notification.objects.filter(student=student, recipient=lecturer.user,
                                                   type=Notification.STUDENT_UNSELECTED_THESIS,
                                                   thesis=thesis).first()
        self.assertIsNotNone(notification)

    def test_lecturer_edited_selected_thesis_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis = create_thesis(lecturer=lecturer, student=student)
        self.client.force_login(lecturer.user)
        self.client.post(reverse('amu_bachelor_thesis:edit_thesis', args=(thesis.id,)), {
            'thesis_title': 'nowy tytuł'
        })
        notification = Notification.objects.filter(lecturer=lecturer, recipient=student.user,
                                                   type=Notification.LECTURER_EDITED_THESIS,
                                                   thesis=thesis).first()
        self.assertIsNotNone(notification)

    def test_lecturer_edited_unselected_thesis_notification(self):
        lecturer = create_lecturer()
        thesis = create_thesis(lecturer=lecturer)
        self.client.force_login(lecturer.user)
        self.client.post(reverse('amu_bachelor_thesis:edit_thesis', args=(thesis.id,)), {
            'thesis_title': 'nowy tytuł'
        })
        notification = Notification.objects.filter(lecturer=lecturer, recipient=None,
                                                   type=Notification.LECTURER_EDITED_THESIS,
                                                   thesis=thesis).first()
        self.assertIsNone(notification)

    def test_lecturer_accepted_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(lecturer=lecturer, student=student)
        self.client.force_login(lecturer.user)
        self.client.get(reverse('amu_bachelor_thesis:accept_thesis_proposition', args=(thesis_proposition.id,)))
        thesis = Thesis.objects.filter(title=thesis_proposition.title).first()
        notification = Notification.objects.filter(lecturer=lecturer, recipient=student.user,
                                                   type=Notification.LECTURER_ACCEPTED_PROPOSITION, thesis=thesis).first()
        self.assertIsNotNone(notification)

    def test_lecturer_accepted_proposition_notification(self):
        student = create_student()
        lecturer = create_lecturer()
        thesis_proposition = create_thesis_proposition(lecturer=lecturer, student=student)
        self.client.force_login(lecturer.user)
        self.client.get(reverse('amu_bachelor_thesis:discard_thesis_proposition', args=(thesis_proposition.id,)))
        notification = Notification.objects.filter(lecturer=lecturer, recipient=student.user,
                                                   type=Notification.LECTURER_DISCARDED_PROPOSITION,
                                                   thesis_proposition=thesis_proposition).first()
        self.assertIsNotNone(notification)

