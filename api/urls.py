from django.urls import path
from . import views


urlpatterns = [
    path("", views.api_overview, name="api-overview"),
    path("task-create/", views.task_create, name="task-create"),
    path("task-list/", views.task_list, name="task-list"),
]
