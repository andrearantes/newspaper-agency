from django import forms
from .models import Redactor, Topic, Magazine, Newspaper
from django_countries.fields import CountryField


class RedactorSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )
    redactor = forms.ModelChoiceField(
        queryset=Redactor.objects.all(),
        required=False,
        label="Select Redactor",
        empty_label="All Redactors"
    )


class NewspaperSearchForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Date",
        widget=forms.TextInput(attrs={"placeholder": "Date of publication"})
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class RedactorCreationForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "format": "%d/%m/%Y"},
                               format="%d/%m/%Y"),
        input_formats=["%d/%m/%Y"],
        required=False
    )
    nationality = CountryField().formfield()

    class Meta:
        model = Redactor
        fields = "__all__"


class MagazineSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by title..."})
    )


class MagazineCreationForm(forms.ModelForm):
    nationality = CountryField().formfield()

    class Meta:
        model = Magazine
        fields = "__all__"
        exclude = ["creator"]
        widgets = {
            "publish_date": forms.TextInput(
                attrs={"placeholder": "dd/mm/yyyy"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["publish_date"].input_formats = ["%d/%m/%Y"]


class TopicForm(forms.ModelForm):
    nationality = CountryField().formfield()

    class Meta:
        model = Topic
        fields = "__all__"
        exclude = ["creator"]
        widgets = {
            "publish_date": forms.TextInput(
                attrs={"placeholder": "dd/mm/yyyy"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["publish_date"].input_formats = ["%d/%m/%Y"]


class NewspaperForm(forms.ModelForm):
    nationality = CountryField().formfield()

    class Meta:
        model = Newspaper
        fields = "__all__"
        exclude = ["creator"]
        widgets = {
            "publish_date": forms.TextInput(
                attrs={"placeholder": "dd/mm/yyyy"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["publish_date"].input_formats = ["%d/%m/%Y"]
