# Generated by Django 2.2.12 on 2021-05-27 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amu_bachelor_thesis_app', '0010_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='thesis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='amu_bachelor_thesis_app.Thesis'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='thesis_proposition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='amu_bachelor_thesis_app.ThesisProposition'),
        ),
    ]
