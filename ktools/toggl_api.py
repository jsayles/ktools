from operator import itemgetter

from django.conf import settings
from django.utils import timezone

from toggl.TogglPy import Toggl


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


    def getClients(self):
        clients = self.toggl.getClients()
        # return sorted(clients, key=itemgetter('at'), reverse=True)
        return clients

    def getClient(self, client_id):
        clients = self.toggl.getClient(id=client_id)
