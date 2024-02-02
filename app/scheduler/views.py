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
        s.print_schedule()

        return JsonResponse({"status": "ok"})


