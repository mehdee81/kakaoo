from django.shortcuts import render
from .models import Courses , Professors
# Create your views here.


def index(request):
    
    all_professors = Professors.objects.values("name")
    courses = Courses.objects.values('course', 'unit')
    return render(request, "scheduler/index.html", {"courses": courses , "professors" : all_professors})

