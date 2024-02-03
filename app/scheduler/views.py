from django.shortcuts import render
from .models import Courses, Professors, SameTime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db.models import Q
from .Graph_Scheduling import Graph, InOrderSchedule

# Create your views here.


def index(request):
    all_professors = Professors.objects.values("name")
    courses = Courses.objects.values("course", "unit")
    return render(
        request,
        "scheduler/index.html",
        {"courses": courses, "professors": all_professors},
    )


@csrf_exempt
def schedule(request):
    if request.method == "POST":
        data = json.loads(request.body)
        selected_courses = data.get("selected_courses")  # list
        linked_courses_to_professors = data.get("linked_courses_to_professors")  # dic
        limited_professors = data.get("limited_professors")  # dic

        verified_linked_courses_to_professors = {}
        for l_c, l_p in linked_courses_to_professors.items():
            verified_linked_courses_to_professors[f"|{l_c}|"] = f"|{l_p}|"

        edges = []
        for course in selected_courses:
            for ch_course in selected_courses:
                if course != ch_course:
                    check_sametime = SameTime.objects.filter(
                        Q(course_1=course, course_2=ch_course)
                        | Q(course_1=ch_course, course_2=course)
                    )
                    if (
                        len(check_sametime) == 0
                        and ((f"|{ch_course}|", f"|{course}|") not in edges)
                        and ((f"|{course}|", f"|{ch_course}|") not in edges)
                    ):
                        edges.append((f"|{course}|", f"|{ch_course}|"))
        
        my_graph = Graph(edges=edges)
        colors = my_graph.color_graph_h()

        units = {}
        for course in selected_courses:
            unit = Courses.objects.filter(course=course).values_list("unit", flat=True)
            units[f"|{course}|"] = unit[0]

        s = InOrderSchedule(
            colors, units, verified_linked_courses_to_professors, limited_professors
        )
        s.assign_lessons()
        request.session.clear()
        request.session['schedule'] = s.schedule
        request.session['selected_courses'] = selected_courses
        request.session['lessons_with_no_time'] = s.lessons_with_no_time
        return JsonResponse({"status": "ok"})

    
def show_schedule(request):
    schedule = request.session['schedule']
    selected_courses = request.session['selected_courses']
    lessons_with_no_time = request.session['lessons_with_no_time']
    clear_schedule = {}
    clear_lessons_with_no_time = []
    for day, day_schedule in schedule.items():
        _day_schedule = {}
        for time, lessons in day_schedule.items():
            lessons_with_out_pipe = []
            for lesson in lessons:
                lessons_with_out_pipe.append(lesson.replace("|" , ""))
            _day_schedule[time] = lessons_with_out_pipe
        clear_schedule[day] = _day_schedule 
    for course in lessons_with_no_time:
        clear_lessons_with_no_time.append(course.replace("|",""))
    return render(request, "scheduler/show_schedule.html" , {"selected_courses": selected_courses , "schedule": clear_schedule , "lessons_with_no_time": clear_lessons_with_no_time})



def learn_more(request):
    return render(request , "scheduler/learn_more.html")