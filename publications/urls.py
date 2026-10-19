from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView


app_name = "newspaper"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", LoginView.as_view(
        template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/accounts/login/"),
         name="logout"),
    path("redactors/", views.RedactorListView.as_view(),
         name="redactor-list"),
    path("redactors/create/", views.RedactorCreateView.as_view(),
         name="redactor-create"),
    path("topics/", views.TopicListView.as_view(),
         name="topic-list"),
    path("topics/create/", views.TopicCreateView.as_view(),
         name="topic-create"),
    path("publications/", views.NewspaperListView.as_view(),
         name="newspaper-list"),
    path("publications/create/", views.NewspaperCreateView.as_view(),
         name="newspaper-create"),
    path("magazines/", views.MagazineListView.as_view(),
         name="magazine-list"),
    path("magazines/create/", views.MagazineCreateView.as_view(),
         name="magazine-create"),

]
