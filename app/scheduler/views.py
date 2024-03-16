from django.shortcuts import render, redirect
from .models import Courses, Professors, SameTime, Professors, CtoP, ProfessorsLimit
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db.models import Q
from .Graph import Graph
from .genetic_algorithm import GAscheduler
from .genetic_with_penalty import GPAscheduler
import random
import copy


# Create your views here.
def index(request):
    courses = Courses.objects.values("course", "unit")
    c_to_p = CtoP.objects.values("id", "course", "professor")
    # Add professor's name to each course
    for course in courses:
        for cp in c_to_p:
            if course["course"] == cp["course"]:
                course["professor"] = cp["professor"]
                break
        else:
            course["professor"] = "none"

    # Get all unique professor names in c_to_p
    professors = set(cp["professor"] for cp in c_to_p)
    return render(
        request,
        "scheduler/index.html",
        {"courses": courses, "professors": professors},
    )


@csrf_exempt
def schedule(request):
    if request.method == "POST":
        data = json.loads(request.body)
        selected_courses = data.get("selected_courses")  # list
        chromosomes = int(data.get("chromosomes"))  # integer
        penalty_chromosomes = int(data.get("penalty_chromosomes"))  # int
        courses_with_out_conditions = data.get("courses_with_out_conditions")  # str
        courses_with_out_conditions = (
            courses_with_out_conditions.replace(" ", "")
        ).split("-")
        profs_limit = ProfessorsLimit.objects.values("id", "professor", "day", "time")

        # Initialize an empty dictionary
        limited_professors = {}

        # Iterate over the queryset
        for prof in profs_limit:
            # If the professor is not in the dictionary, add them
            if prof["professor"] not in limited_professors:
                limited_professors[prof["professor"]] = []
            # Append the day and time to the professor's list
            limited_professors[prof["professor"]].append([prof["day"], prof["time"]])

        linked_courses_to_professors = {}

        verified_courses_with_out_conditions = []
        for course in courses_with_out_conditions:
            if course in selected_courses:
                verified_courses_with_out_conditions.append(course)
                selected_courses.remove(course)

        c_to_p = CtoP.objects.values("id", "course", "professor")
        for c_t_p in c_to_p:
            linked_courses_to_professors[c_t_p["course"]] = c_t_p["professor"]

        for course in selected_courses:
            if course not in linked_courses_to_professors:
                chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                random_prof = "".join(random.choice(chars) for _ in range(10))
                linked_courses_to_professors[course] = random_prof

        verified_linked_courses_to_professors = {}
        for l_c, l_p in linked_courses_to_professors.items():
            verified_linked_courses_to_professors[l_c] = l_p

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
                        and ((ch_course, course) not in edges)
                        and ((course, ch_course) not in edges)
                    ):
                        edges.append((course, ch_course))

        my_graph = Graph(edges=edges)
        colors = my_graph.color_graph_h()

        units = {}
        for course in selected_courses:
            unit = Courses.objects.filter(course=course).values_list("unit", flat=True)
            units[course] = unit[0]

        for course in verified_courses_with_out_conditions:
            unit = Courses.objects.filter(course=course).values_list("unit", flat=True)
            units[course] = unit[0]

        semesters = {}
        for course in selected_courses:
            semester = Courses.objects.filter(course=course).values_list(
                "semester", flat=True
            )
            semesters[course] = semester[0]

        for course in verified_courses_with_out_conditions:
            semester = Courses.objects.filter(course=course).values_list(
                "semester", flat=True
            )
            semesters[course] = semester[0]
        # ----------------------------------------------testing----------------------------------------------
        # print("colors=",colors)
        # print("units=",units)
        # print("semesters=",semesters)
        # print("verified_linked_courses_to_professors=",verified_linked_courses_to_professors)
        # print("limited_professors=",limited_professors)
        # print("chromosomes=",chromosomes)
        # print("verified_courses_with_out_conditions=",verified_courses_with_out_conditions)
        # ----------------------------------------------end testing------------------------------------------
        s = GAscheduler(
            colors,
            units,
            semesters,
            verified_linked_courses_to_professors,
            limited_professors,
            chromosomes,
            verified_courses_with_out_conditions,
        )
        s.start()

        request.session["schedule"] = copy.deepcopy(s.best_schedule)
        request.session["lessons_with_no_time"] = copy.deepcopy(
            s.lowest_lessons_with_no_section
        )

        request.session["selected_courses"] = selected_courses

        sp = GPAscheduler(
            s.lowest_lessons_with_no_section,
            s.best_schedule,
            edges,
            units,
            verified_linked_courses_to_professors,
            limited_professors,
            penalty_chromosomes,
        )
        sp.start()

        request.session["penalty_schedule"] = copy.deepcopy(sp.best_schedule)

        return JsonResponse({"status": "ok"})


def show_schedule(request):
    schedule = request.session["schedule"]
    penalty_schedule = request.session["penalty_schedule"]
    selected_courses = request.session["selected_courses"]
    lessons_with_no_time = request.session["lessons_with_no_time"]
    request.session.clear()

    clear_schedule = {}
    for day, day_schedule in schedule.items():
        _day_schedule = {}
        for time, lessons in day_schedule.items():
            lessons_with_out_pipe = []
            for lesson in lessons:
                lessons_with_out_pipe.append(lesson.replace("|", ""))
            _day_schedule[time] = lessons_with_out_pipe
        clear_schedule[day] = _day_schedule

    clear_penalty_schedule = {}
    for day, day_schedule in penalty_schedule.items():
        _day_schedule = {}
        for time, lessons in day_schedule.items():
            lessons_with_out_pipe = []
            for lesson in lessons:
                lessons_with_out_pipe.append(lesson.replace("|", ""))
            _day_schedule[time] = lessons_with_out_pipe
        clear_penalty_schedule[day] = _day_schedule

    clear_lessons_with_no_time = []
    for course in lessons_with_no_time:
        clear_lessons_with_no_time.append(course.replace("|", ""))

    return render(
        request,
        "scheduler/show_schedule.html",
        {
            "selected_courses": selected_courses,
            "schedule": clear_schedule,
            "lessons_with_no_time": clear_lessons_with_no_time,
            "clear_penalty_schedule": clear_penalty_schedule,
        },
    )


def learn_more(request):
    return render(request, "scheduler/learn_more.html")


def courses(request):
    courses = Courses.objects.values("id", "course", "semester", "unit").order_by("-id")
    return render(request, "scheduler/courses.html", {"courses": courses})


def add_course(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        course_name = course_name.replace("-", "_")
        course_unit = request.POST.get("Course_unit")
        Course_semester = request.POST.get("Course_semester")
        existing_record = Courses.objects.filter(course=course_name).exists()
        if not existing_record:
            course = Courses(
                course=course_name, semester=Course_semester, unit=course_unit
            )
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

    c_to_p = CtoP.objects.filter(course=course_name)
    c_to_p.delete()
    return redirect("courses")


def update_unit(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        new_unit_value = request.POST.get("Course_unit")
        course = Courses.objects.get(id=course_id)
        course.unit = new_unit_value  # Replace with the actual new unit value
        course.save()
        return redirect("courses")


def update_semester(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        new_semester_value = request.POST.get("Course_semester")
        course = Courses.objects.get(id=course_id)
        course.semester = new_semester_value  # Replace with the actual new unit value
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
    professors = Professors.objects.values("id", "name").order_by("-id")
    return render(request, "scheduler/professors.html", {"professors": professors})


def delete_professor(request, professor_id):
    prof = Professors.objects.get(id=professor_id)
    prof.delete()

    c_to_p = CtoP.objects.filter(professor=prof)
    c_to_p.delete()

    limit_prof = ProfessorsLimit.objects.filter(professor=prof)
    limit_prof.delete()
    return redirect("professors")


def add_professor(request):
    if request.method == "POST":
        prof_name = request.POST.get("professor_name")
        existing_record = Professors.objects.filter(name=prof_name).exists()
        if not existing_record:
            prof = Professors(name=prof_name)
            prof.save()
    return redirect("professors")


def sametimes(request):
    courses = Courses.objects.values("id", "course", "unit")
    sametimes = SameTime.objects.values("id", "course_1", "course_2").order_by("-id")
    return render(
        request,
        "scheduler/sametimes.html",
        {"courses": courses, "sametimes": sametimes},
    )


def add_sametime(request):
    if request.method == "POST":
        course_1 = request.POST.get("sametime_course_1")
        course_2 = request.POST.get("sametime_course_2")
        if course_1 != course_2:
            existing_record = SameTime.objects.filter(
                Q(course_1=course_1, course_2=course_2)
                | Q(course_1=course_2, course_2=course_1)
            ).exists()
            if not existing_record:
                sametime = SameTime(course_1=course_1, course_2=course_2)
                sametime.save()
    return redirect("sametimes")


def delete_sametime(request, sametime_id):
    sametime = SameTime.objects.get(id=sametime_id)
    sametime.delete()
    return redirect("sametimes")


def c_to_p(request):
    courses = Courses.objects.values("id", "course", "unit")
    professors = Professors.objects.values("id", "name")
    c_to_p = CtoP.objects.values("id", "course", "professor").order_by("-id")
    return render(
        request,
        "scheduler/c_to_p.html",
        {"courses": courses, "professors": professors, "c_to_p": c_to_p},
    )


def add_c_to_p(request):
    if request.method == "POST":
        course = request.POST.get("course")
        prof = request.POST.get("professor")
        all_c_to_p = CtoP.objects.values_list("course", flat=True)
        if course not in all_c_to_p:
            c_to_p = CtoP(course=course, professor=prof)
            c_to_p.save()
        return redirect("c_to_p")


def delete_c_to_p(request, c_to_p_id):
    c_to_p = CtoP.objects.get(id=c_to_p_id)
    c_to_p.delete()
    return redirect("c_to_p")


def professors_limit(request):
    c_to_p = CtoP.objects.values_list("professor", flat=True)
    # professors = Professors.objects.values("id", "name")
    profs_limit = ProfessorsLimit.objects.values(
        "id", "professor", "day", "time"
    ).order_by("-id")

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]
    times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
    schedule = {day: {time: [] for time in times} for day in days}

    for prof in profs_limit:
        schedule[prof["day"]][prof["time"]].append((prof["professor"], prof["id"]))

    # Filter the Professors querysetc_to_p = CtoP.objects.values_list('professor', flat=True)
    professors = Professors.objects.filter(name__in=c_to_p).values("id", "name")

    return render(
        request,
        "scheduler/professors_limit.html",
        {"professors": professors, "profs_limit": profs_limit, "schedule": schedule},
    )


def add_professors_limit(request):
    if request.method == "POST":
        prof = request.POST.get("prof")
        day = request.POST.get("day")
        time = request.POST.get("time")
        existing_record = ProfessorsLimit.objects.filter(
            professor=prof, day=day, time=time
        ).exists()
        if not existing_record:
            profs_limit = ProfessorsLimit(professor=prof, day=day, time=time)
            profs_limit.save()
        return redirect("professors_limit")


def delete_professors_limit(request, professors_limit_id):
    prof_limit = ProfessorsLimit.objects.get(id=professors_limit_id)
    prof_limit.delete()
    return redirect("professors_limit")
