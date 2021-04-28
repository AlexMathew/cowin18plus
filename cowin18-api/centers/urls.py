from django.urls import path

from .views import CentersListView

urlpatterns = [
    path("centers/", CentersListView.as_view(), name="centers"),
]
