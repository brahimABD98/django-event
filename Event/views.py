from django.shortcuts import HttpResponse, render
from django.shortcuts import render
# listview createview deleteview
from django.views.generic import ListView

from .models import Event


# Create your views here.
def index(request):
    return HttpResponse("Bonjour")


def index_param(request, param):
    return HttpResponse(f"bonjour {param}")


def affiche(request):
    evt = Event.objects.all()
    # resultat = '-----'.join(
    #     e.title for e in evt
    # )
    # return HttpResponse(resultat)
    # context = {'ee': evt}
    return render(request, "Event/affiche.html", {'ee': evt})


class AfficheGeneric(ListView):
    model = Event
    template_name = "Event/affiche.html"
    context_object_name = 'ee'
    ordering = ['-adescription']
    fields = "__all__"


def detail(request, title):
    event = Event.objects.get(title=title)
    return render(request, 'Event/detail.html', {'ee': event})
