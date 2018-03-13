from django.shortcuts import render
from django.shortcuts import render, HttpResponse


def index(response):
    return HttpResponse('This is main page')
