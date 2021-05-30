# AMU Bachelor Thesis
Django application for students and lecturers. Lecturers can add bachelor thesis topics and students can choose one of them. Students can also propose their own bachelor thesis topics - in that case lecturers can other accept or discard them. Application has built-in simple notification system. 
Whole app was created as "Internet Technologies" course final project at Adam Mickiewicz University. 
# Run app
Django version:
> python -c "import django; print(django.get_version())" 
> 
> 2.2.12

Startup:
> python manage.py makemigrations
> 
> python manage.py migrate
> 
> python manage.py runserver

Add first user:
> python manage.py createsuperuser

Tests:
> python manage.py test
