# Generated by Django 2.2.12 on 2021-05-26 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amu_bachelor_thesis_app', '0006_thesisproposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesisproposition',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amu_bachelor_thesis_app.Student'),
        ),
    ]
