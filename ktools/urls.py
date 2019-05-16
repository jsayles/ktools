from django.urls import path
from django.contrib import admin

from ktools import views


urlpatterns = [
    path('', views.index, name='index'),
    path('toggl', views.toggl, name='toggl'),
    path('toggl/client/<client_id>', views.toggl_client, name='toggl_client'),

    path('admin/', admin.site.urls),

]
