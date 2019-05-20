from calendar import Calendar, month_name

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime, now
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from toggl.TogglPy import Toggl

from ktools.models import TogglUser, TogglClient, TogglProject, TogglEntry


def index(request):
    context = {}
    return render(request, 'ktools/index.html', context)


def calendar_today(request):
    today = localtime(now()).date()
    calendar_url = reverse('calendar', kwargs={'year': today.year, 'month': today.month})
    return HttpResponseRedirect(calendar_url)


def calendar(request, year, month):
    prev_year = next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year = year + 1
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    context = {
        'month': month,
        'year': year,
        'calendar': Calendar().monthdayscalendar(year, month),
        'month_name': month_name[month],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'ktools/calendar.html', context)


######################################################################
# Toggl Views
######################################################################

@login_required
def toggl(request):
    toggl_clients = TogglClient.objects.all()
    context = {'toggl_clients': toggl_clients}
    return render(request, 'ktools/toggl.html', context)


@login_required
def toggl_client(request, client_id):
    client = get_object_or_404(TogglClient, id=client_id)
    projects = TogglProject.objects.filter(client=client)
    context = {
        'client': client,
        'projects': projects,
    }
    return render(request, 'ktools/toggl_client.html', context)
