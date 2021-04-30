from django.urls import path

from .views import CentersListV1View

urlpatterns = [
    path("centers/", CentersListV1View.as_view(), name="centers"),
]
