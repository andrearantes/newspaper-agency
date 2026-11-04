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
    path("redactor/<int:pk>/delete/", views.RedactorDeleteView.as_view(),
         name="redactor-delete"),
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
    path("publications/<int:pk>/update/", views.NewspaperUpdateView.as_view(),
         name="newspaper-update"),
    path("publications/<int:pk>/delete/", views.NewspaperDeleteView.as_view(),
         name="newspaper-delete"),
    path("magazines/<int:pk>/update/", views.MagazineUpdateView.as_view(),
         name="magazine-update"),
    path("magazines/<int:pk>/delete/", views.MagazineDeleteView.as_view(),
         name="magazine-delete"),
    path("topics/<int:pk>/update/", views.TopicUpdateView.as_view(),
         name="topic-update"),
    path("topics/<int:pk>/delete/", views.TopicDeleteView.as_view(),
         name="topic-delete"),
    path("publications/<int:pk>/", views.NewspaperDetailView.as_view(),
         name="newspaper-detail"),
    path("magazines/<int:pk>/", views.MagazineDetailView.as_view(),
         name="magazine-detail"),
    path("redactors/<int:pk>/update/", views.RedactorUpdateView.as_view(),
         name="redactor-update"),
    path("topic/<int:pk>/detail/", views.TopicDetailView.as_view(),
         name="topic-detail"),
    path("redactors/<int:pk>/detail/", views.RedactorDetailView.as_view(),
         name="redactor-detail"),

]
