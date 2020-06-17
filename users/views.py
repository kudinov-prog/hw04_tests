from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm

from django.shortcuts import render, get_object_or_404


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
