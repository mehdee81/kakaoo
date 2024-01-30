from django.shortcuts import render
# from . models import Course
# Create your views here.


def index(request):
    data = {
    'one': '1',
    'two': '2'
    }
    return render(request, "scheduler/index.html", data)
