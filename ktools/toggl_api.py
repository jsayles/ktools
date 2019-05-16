from operator import itemgetter

from django.conf import settings
from django.utils import timezone

from toggl.TogglPy import Toggl, Endpoints

from ktools.models import TogglClient, TogglProject, TogglEntry


class TogglAPI:

    def __init__(self):
        self.toggl_account = getattr(settings, 'TOGGL_ACCOUNT', None)
        if self.toggl_account is None:
            raise ImproperlyConfigured("Please set your TOGGL_ACCOUNT setting.")

        self.toggl_password = getattr(settings, 'TOGGL_PASSWORD', None)
        if self.toggl_password is None:
            raise ImproperlyConfigured("Please set your TOGGL_PASSWORD setting.")

        self.toggl = Toggl()
        self.toggl.setAuthCredentials(self.toggl_account, self.toggl_password)

    def syncClients(self):
        for c in self.toggl.getClients():
            client, created = TogglClient.objects.get_or_create(id=c['id'], name=c['name'])
            projects = self.toggl.getClientProjects(c['id'])
            if projects:
                for p in projects:
                    project, created = TogglProject.objects.get_or_create(id=p['id'], client=client)
                    if created:
                        project.name = p['name']
                        project.is_active = p['active']
                        project.save()

    def getTimeEntries(self):
        for e in self.toggl.request(Endpoints.TIME_ENTRIES):
            print(e)
            project = TogglProject.objects.filter(id=e['pid']).first()
            entry, created = TogglEntry.objects.get_or_create(id=e['id'], project=project, uid=e['uid'])
            if created:
                entry.start_ts = e['start']
                entry.end_ts = e['stop']
                entry.duration_sec = e['duration']
                if 'description' in e:
                    entry.description = e['description']
                entry.save()
