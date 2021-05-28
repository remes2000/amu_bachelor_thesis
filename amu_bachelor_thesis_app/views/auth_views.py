from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from amu_bachelor_thesis_app.models import User


@login_required
def login_redirect(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.user.role == User.SUPERUSER:
        return HttpResponseRedirect(reverse('amu_bachelor_thesis:home'))
    return HttpResponseRedirect(reverse('amu_bachelor_thesis:search_engine'))


