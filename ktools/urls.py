from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from ktools import views


urlpatterns = [
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),

    path('', views.index, name='index'),
    path('toggl', views.toggl, name='toggl'),
    path('toggl/client/<client_id>', views.toggl_client, name='toggl_client'),

    path('admin/', admin.site.urls),

]
