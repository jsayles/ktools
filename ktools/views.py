from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from toggl.TogglPy import Toggl


######################################################################
# Helper Methods
######################################################################


def get_toggl_api():
    toggl_account = getattr(settings, 'TOGGL_ACCOUNT', None)
    if toggl_account is None:
        raise ImproperlyConfigured("Please set your TOGGL_ACCOUNT setting.")

    toggl_password = getattr(settings, 'TOGGL_PASSWORD', None)
    if toggl_password is None:
        raise ImproperlyConfigured("Please set your TOGGL_PASSWORD setting.")

    toggl = Toggl()
    toggl.setAuthCredentials(toggl_account, toggl_password)
    return toggl


######################################################################
# Main Views
######################################################################

def index(request):
    context = {}
    return render(request, 'ktools/index.html', context)


######################################################################
# Toggl Views
######################################################################

@login_required
def toggl(request):
    toggl_clients = get_toggl_api().getClients()
    context = {'toggl_clients': toggl_clients}
    return render(request, 'ktools/toggl.html', context)


@login_required
def toggl_client(request, client_id):
    api = get_toggl_api()
    client = api.getClient(id=client_id)
    projects = api.getClientProjects(client_id)
    context = {
        'client': client,
        'projects': projects,
    }
    return render(request, 'ktools/toggl_client.html', context)
