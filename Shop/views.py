from django.shortcuts import render

# Create your views here.
from django.views import generic


class MainPageView(generic.TemplateView):
    template_name = 'index.html'

