import time
from datetime import datetime, timedelta
from operator import itemgetter

from django.conf import settings
from django.utils.timezone import localtime, now, make_aware

from toggl.TogglPy import Toggl, Endpoints

from ktools.models import TogglUser, TogglClient, TogglProject, TogglEntry


class TogglAPI:

    def __init__(self):
        self.users = []

        # Pull all Toggl users and connect up their API
        for u in TogglUser.objects.all():
            api = Toggl()
            api.setAuthCredentials(u.username, u.password)
            self.users.append({
                'user': u.user,
                'api': api,
            })

    def syncClientData(self, create_only=False):
        for u in self.users:
            toggl = u['api']

            # Pull all the clients, and projects for this user
            for c in toggl.getClients():
                client, created = TogglClient.objects.get_or_create(id=c['id'], name=c['name'])
                if not created and create_only:
                    # Skip pulling projects if we already had this client in the DB
                    continue

                # Pull all the projects for this client
                projects = toggl.getClientProjects(c['id'])
                if projects:
                    for p in projects:
                        project, created = TogglProject.objects.get_or_create(id=p['id'], client=client)
                        project.name = p['name']
                        project.is_active = p['active']
                        project.save()

            # Don't hit the API too hard
            time.sleep(1)

    def syncTimeEntries(self, start, end):
        for u in self.users:
            toggl = u['api']

            # Pull all the time entries for this user
            params = {'start_date':start.isoformat(), 'end_date':end.isoformat()}
            entries = toggl.request(Endpoints.TIME_ENTRIES, parameters=params)

            for e in entries:
                if not 'stop' in e:
                    # Skip entries currently in progress
                    continue
                if not 'pid' in e:
                    print("Found entry without a project.  Ignoring!:")
                    print(e)
                    continue
                project = TogglProject.objects.filter(id=e['pid']).first()
                if not project:
                    if syncClients:
                        self.syncClientData()
                    else:
                        raise Exception("Encountered missing project data!")

                entry, created = TogglEntry.objects.get_or_create(id=e['id'], project=project, uid=e['uid'])
                entry.start_ts = e['start']
                entry.end_ts = e['stop']
                entry.duration_sec = e['duration']
                if 'description' in e:
                    entry.description = e['description']
                entry.save()

            # Don't hit the API too hard
            time.sleep(1)

    def syncMonthlyEntries(self, year, month):
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        start = make_aware(datetime(year, month, 1))
        end = make_aware(datetime(next_year, next_month, 1))
        self.syncTimeEntries(start, end)

    def syncWeeklyEntries(self, year, month, day):
        start = make_aware(datetime(year, month, day))
        end = start + timedelta(days=1)
        start = start - timedelta(days=7)
        self.syncTimeEntries(start, end)

    def syncDailyEntries(self, year, month, day):
        start = make_aware(datetime(year, month, day))
        end = start + timedelta(days=1)
        self.syncTimeEntries(start, end)
