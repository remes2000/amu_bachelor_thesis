# Generated by Django 2.2.12 on 2021-05-27 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amu_bachelor_thesis_app', '0008_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='lecturer_id',
            new_name='lecturer',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='recipient_id',
            new_name='recipient',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='student_id',
            new_name='student',
        ),
    ]
