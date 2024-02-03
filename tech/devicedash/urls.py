from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("find", views.find, name="find"),
    path("find/<str:id>", views.viewPhone, name="viewPhone")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
