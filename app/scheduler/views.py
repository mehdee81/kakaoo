from django.shortcuts import render, redirect
from .models import Courses, Professors, SameTime, Professors
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
        request.session["schedule"] = s.schedule
        request.session["selected_courses"] = selected_courses
        request.session["lessons_with_no_time"] = s.lessons_with_no_time
        return JsonResponse({"status": "ok"})


def show_schedule(request):
    schedule = request.session["schedule"]
    selected_courses = request.session["selected_courses"]
    lessons_with_no_time = request.session["lessons_with_no_time"]
    clear_schedule = {}
    clear_lessons_with_no_time = []
    for day, day_schedule in schedule.items():
        _day_schedule = {}
        for time, lessons in day_schedule.items():
            lessons_with_out_pipe = []
            for lesson in lessons:
                lessons_with_out_pipe.append(lesson.replace("|", ""))
            _day_schedule[time] = lessons_with_out_pipe
        clear_schedule[day] = _day_schedule
    for course in lessons_with_no_time:
        clear_lessons_with_no_time.append(course.replace("|", ""))
    return render(
        request,
        "scheduler/show_schedule.html",
        {
            "selected_courses": selected_courses,
            "schedule": clear_schedule,
            "lessons_with_no_time": clear_lessons_with_no_time,
        },
    )


def learn_more(request):
    return render(request, "scheduler/learn_more.html")


def courses(request):
    courses = Courses.objects.values("id", "course", "unit")
    return render(request, "scheduler/courses.html", {"courses": courses})


def add_course(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        course_unit = request.POST.get("Course_unit")
        course = Courses(course=course_name, unit=course_unit)
        course.save()
        return redirect("courses")
    else:
        return redirect("courses")


def delete_course(request, course_id, course_name):
    course = Courses.objects.get(id=course_id)
    course.delete()
    sametimes = SameTime.objects.filter(
        Q(course_1=course_name) | Q(course_2=course_name)
    )
    sametimes.delete()
    return redirect("courses")


def update_unit(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        new_unit_value = request.POST.get("Course_unit")
        course = Courses.objects.get(id=course_id)
        course.unit = new_unit_value  # Replace with the actual new unit value
        course.save()
        return redirect("courses")


def add_group(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        Course_goup_number = request.POST.get("Course_goup_number")
        main_course = Courses.objects.get(course=course_name)
        course = Courses.objects.filter(
            course=f"{course_name}_g{Course_goup_number}"
        ).all()
        if len(course) == 0:

            add_course = Courses(
                course=f"{course_name}_g{Course_goup_number}", unit=main_course.unit
            )
            add_course.save()

            sametimes = SameTime.objects.filter(
                Q(course_1=course_name) | Q(course_2=course_name)
            )

            linked_courses = []
            for sametime in sametimes:
                if sametime.course_1 != course_name:
                    linked_courses.append(sametime.course_1)
                if sametime.course_2 != course_name:
                    linked_courses.append(sametime.course_2)
            linked_courses.append(course_name)

            for l_c in linked_courses:
                add_course = SameTime(
                    course_1=f"{course_name}_g{Course_goup_number}", course_2=l_c
                )
                add_course.save()

    return redirect("courses")


def professors(request):
    professors = Professors.objects.values("id", "name")
    return render(request, "scheduler/professors.html", {"professors": professors})


def delete_professor(request, professor_id):
    prof = Professors.objects.get(id=professor_id)
    prof.delete()
    return redirect("professors")


def add_professor(request):
    if request.method == "POST":
        prof_name = request.POST.get("professor_name")
        prof = Professors(name=prof_name)
        prof.save()
    return redirect("professors")


def sametimes(request):
    courses = Courses.objects.values("id", "course", "unit")
    sametimes = SameTime.objects.values("id", "course_1", "course_2")
    return render(
        request,
        "scheduler/sametimes.html",
        {"courses": courses, "sametimes": sametimes},
    )
    
def delete_sametime(request, sametime_id):
    sametime = SameTime.objects.get(id=sametime_id)
    sametime.delete()
    return redirect("sametimes")

def add_sametime(request):
    if request.method == "POST":
        course_1 = request.POST.get("sametime_course_1")
        course_2 = request.POST.get("sametime_course_2")
        sametime = SameTime(course_1=course_1 , course_2=course_2)
        sametime.save()
    return redirect("sametimes")