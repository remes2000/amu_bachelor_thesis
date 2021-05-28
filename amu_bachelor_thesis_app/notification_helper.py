from django.utils import timezone

from amu_bachelor_thesis_app.models import Notification


class NotificationHelper:
    @staticmethod
    def send_student_created_proposition_notification(thesis_proposition):
        notification = Notification(
            type=Notification.STUDENT_CREATED_PROPOSITION,
            date=timezone.now(),
            is_seen=False,
            thesis_proposition=thesis_proposition,
            student=thesis_proposition.student,
            recipient=thesis_proposition.lecturer.user)
        notification.save()

    @staticmethod
    def send_student_discard_proposition_notification(thesis_proposition):
        notification = Notification(
            type=Notification.STUDENT_DISCARDED_PROPOSITION,
            date=timezone.now(),
            is_seen=False,
            thesis_proposition=thesis_proposition,
            student=thesis_proposition.student,
            recipient=thesis_proposition.lecturer.user)
        notification.save()

    @staticmethod
    def send_student_edited_proposition_notification(thesis_proposition):
        notification = Notification(
            type=Notification.STUDENT_EDITED_PROPOSITION,
            date=timezone.now(),
            is_seen=False,
            thesis_proposition=thesis_proposition,
            student=thesis_proposition.student,
            recipient=thesis_proposition.lecturer.user)
        notification.save()

    @staticmethod
    def send_student_selected_thesis_notification(thesis):
        notification = Notification(
            type=Notification.STUDENT_SELECTED_THESIS,
            date=timezone.now(),
            is_seen=False,
            thesis=thesis,
            student=thesis.student,
            recipient=thesis.lecturer.user)
        notification.save()

    @staticmethod
    def send_student_unselected_thesis_notification(student, thesis):
        notification = Notification(
            type=Notification.STUDENT_UNSELECTED_THESIS,
            date=timezone.now(),
            is_seen=False,
            thesis=thesis,
            student=student,
            recipient=thesis.lecturer.user)
        notification.save()

    @staticmethod
    def send_lecturer_edited_thesis_notification(thesis):
        notification = Notification(
            type=Notification.LECTURER_EDITED_THESIS,
            date=timezone.now(),
            is_seen=False,
            thesis=thesis,
            lecturer=thesis.lecturer,
            recipient=thesis.student.user)
        notification.save()

    @staticmethod
    def send_lecturer_accepted_proposition_notification(thesis):
        notification = Notification(
            type=Notification.LECTURER_ACCEPTED_PROPOSITION,
            date=timezone.now(),
            is_seen=False,
            thesis=thesis,
            lecturer=thesis.lecturer,
            recipient=thesis.student.user)
        notification.save()

    @staticmethod
    def send_lecturer_discarded_proposition_notification(thesis_proposition):
        notification = Notification(
            type=Notification.LECTURER_DISCARDED_PROPOSITION,
            date=timezone.now(),
            is_seen=False,
            thesis_proposition=thesis_proposition,
            lecturer=thesis_proposition.lecturer,
            recipient=thesis_proposition.student.user)
        notification.save()

