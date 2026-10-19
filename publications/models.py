from django.db import models
from django.contrib.auth.models import AbstractUser


class Redactor(AbstractUser):
    experience_years = models.IntegerField(default=0)
    birth_date = models.DateField(null=True, blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    comments = models.TextField()
    published_date = models.DateField()
    redactors = models.ManyToManyField(Redactor, related_name="publications")
    topics = models.ManyToManyField(Topic, related_name="publications")

    def __str__(self):
        return self.title


class Magazine(models.Model):
    title = models.CharField(max_length=255)
    comments = models.TextField()
    published_date = models.DateField()
    redactors = models.ManyToManyField(Redactor, related_name="magazines")
    topics = models.ManyToManyField(Topic, related_name="magazines")

    def __str__(self):
        return self.title
