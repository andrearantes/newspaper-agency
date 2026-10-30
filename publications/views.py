from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from django.views import generic
from .models import (Redactor,
                     Topic,
                     Newspaper,
                     Magazine
                     )
from .forms import (RedactorSearchForm,
                    NewspaperSearchForm,
                    TopicSearchForm,
                    RedactorCreationForm,
                    MagazineSearchForm,
                    TopicForm,
                    NewspaperForm,
                    MagazineCreationForm
                    )


@login_required
def index(request):
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_magazines = Magazine.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers,
        "num_magazines": num_magazines,
        "num_visits": num_visits + 1,
    }
    return render(request, "newspaper/index.html", context=context)


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "newspaper/redactor_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        redactor_id = self.request.GET.get("redactor")

        if name:
            queryset = queryset.filter(Q(first_name__icontains=name)
                                       | Q(last_name__icontains=name)
                                       )

        if redactor_id:
            queryset = queryset.filter(id=redactor_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = RedactorSearchForm(self.request.GET)
        return context


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "newspaper/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Redactor"
        return context


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    template_name = "newspaper/redactor_confirm_delete.html"
    success_url = reverse_lazy("newspaper:redactor-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    fields = ["username",
              "email",
              "first_name",
              "last_name",
              "experience_years",
              "birth_date"
              ]
    template_name = "newspaper/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Redactor"
        return context


class RedactorDetailView(generic.DetailView):
    model = Redactor
    template_name = "newspaper/redactor_detail.html"
    success_url = reverse_lazy("newspaper:redactor-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TopicSearchForm(self.request.GET)
        return context


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "newspaper/topic_confirm_delete.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    template_name = "newspaper/topic_detail.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["redactors"] = self.object.redactors.all()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    template_name = "newspaper/newspaper_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get("date")
        if date:
            queryset = queryset.filter(publish_date=date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NewspaperSearchForm(self.request.GET)
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "newspaper/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class MagazineListView(LoginRequiredMixin, generic.ListView):
    model = Magazine
    context_object_name = "magazine_list"
    template_name = "newspaper/magazine_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = MagazineSearchForm(self.request.GET)
        context["num_magazines"] = Magazine.objects.count()
        return context


class MagazineCreateView(LoginRequiredMixin, generic.CreateView):
    model = Magazine
    form_class = MagazineCreationForm
    template_name = "newspaper/magazine_form.html"
    success_url = reverse_lazy("newspaper:magazine-list")


class MagazineUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Magazine
    form_class = MagazineCreationForm
    template_name = "newspaper/magazine_form.html"
    success_url = reverse_lazy("newspaper:magazine-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class MagazineDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Magazine
    template_name = "newspaper/magazine_confirm_delete.html"
    success_url = reverse_lazy("newspaper:magazine-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj


class MagazineDetailView(LoginRequiredMixin, generic.DetailView):
    model = Magazine
    template_name = "newspaper/magazine_detail.html"
    success_url = reverse_lazy("newspaper:magazine-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (obj.creator != self.request.user
                and not self.request.user.is_superuser):
            raise PermissionDenied
        return obj
