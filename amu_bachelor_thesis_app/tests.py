import datetime
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from amu_bachelor_thesis_app.models import Thesis, Lecturer, User


def create_lecturer():
    user_email = str(uuid.uuid4()) + '@email.pl'
    user = User.objects.create(email=user_email, role=User.LECTURER)
    return Lecturer.objects.create(first_name="John", last_name="Test", degree="PhD",
                                   interests="NA", description="NA", user=user)


def create_thesis(title, lecturer, created_at=timezone.now(), edited_at=timezone.now()):
    return Thesis.objects.create(title=title, created_at=created_at, edited_at=edited_at, lecturer=lecturer)


class ManageThesisViewTests(TestCase):
    def test_thesis_order(self):
        lecturer = create_lecturer()
        self.client.force_login(lecturer.user, backend=None)
        thesis1 = create_thesis("Thesis1",
                                created_at=timezone.now() - datetime.timedelta(days=5),
                                edited_at=timezone.now(), lecturer=lecturer)
        thesis2 = create_thesis("Thesis2",
                                created_at=timezone.now() - datetime.timedelta(days=4),
                                edited_at=timezone.now() - datetime.timedelta(minutes=15), lecturer=lecturer)
        thesis3 = create_thesis("Thesis3",
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
        create_thesis('MainLecturerThesis1', main_lecturer)
        create_thesis('MainLecturerThesis2', main_lecturer)
        not_included_thesis = create_thesis('DifferentLecturerThesis', different_lecturer)
        response = self.client.get(reverse('amu_bachelor_thesis:manage_thesis'))
        query_set = response.context['page_obj']
        included_thesis_ids = map(lambda q: q.id, query_set)
        self.assertNotIn(not_included_thesis.id, included_thesis_ids)
