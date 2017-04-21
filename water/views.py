from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Item
# Create your views here.


def index(request):
    items = Item.objects.all()
    return render(request, 'water/list.html', {
        'items': items,
        'error_message': "You didn't select a choice.",
    })
