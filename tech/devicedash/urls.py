from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("find", views.find, name="find"),
    path("admin_login", views.admin, name="admin"),
    path("add", views.add, name="add"),
    path("save", views.save, name="save"),
    path("all", views.all_phones, name="all"),
    path("search", views.search, name="search"),
    path("logout_view", views.logout_view, name="logout"),
    path("find/<str:id>", views.viewPhone, name="viewPhone")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
