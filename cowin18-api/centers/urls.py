from django.urls import path

from .views import CentersListView, DistrictsListView

urlpatterns = [
    path("districts/", DistrictsListView.as_view(), name="districts"),
    path("centers/", CentersListView.as_view(), name="centers"),
]
