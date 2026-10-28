from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Redactor(AbstractUser):
    experience_years = models.IntegerField(default=0)
    birth_date = models.DateField(null=True, blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    redactors = models.ManyToManyField(Redactor, related_name="topics")
    creator = models.ForeignKey(
        Redactor,
        on_delete=models.CASCADE,
        related_name="created_topic",
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("newspaper:topic-detail", args=[self.pk])


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    comments = models.TextField()
    published_date = models.DateField()
    redactors = models.ManyToManyField(Redactor, related_name="publications")
    topics = models.ManyToManyField(Topic, related_name="publications")
    creator = models.ForeignKey(
        Redactor,
        on_delete=models.CASCADE,
        related_name="created_newspapers",
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newspaper:newspaper-detail", args=[self.pk])


class Magazine(models.Model):
    title = models.CharField(max_length=255)
    comments = models.TextField()
    published_date = models.DateField()
    redactors = models.ManyToManyField(Redactor, related_name="magazines")
    topics = models.ManyToManyField(Topic, related_name="magazines")
    creator = models.ForeignKey(
        Redactor,
        on_delete=models.CASCADE,
        related_name="created_magazines",
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newspaper:magazine-detail", args=[self.pk])
