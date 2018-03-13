from django.shortcuts import render
from django.shortcuts import render, HttpResponse

def training_detail(request, training_id):
    return HttpResponse('This is training {}'.format(training_id))
# Create your views here.
