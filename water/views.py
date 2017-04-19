from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
# Create your views here.


def index(request):
    return render(request, 'water/list.html', {
        'poll': 'hi',
        'error_message': "You didn't select a choice.",
    })
