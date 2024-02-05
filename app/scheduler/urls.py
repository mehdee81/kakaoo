from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("schedule/", views.schedule),
    path("show_schedule/", views.show_schedule, name="show_schedule"),
    path("learn_more/", views.learn_more, name="learn_more"),
    path("courses/", views.courses, name="courses"),
    path("add_course/", views.add_course, name="add_course"),
    path(
        "delete_course/<int:course_id>/<str:course_name>",
        views.delete_course,
        name="delete_course",
    ),
    path("update_unit", views.update_unit, name="update_unit"),
    path('add_group' , views.add_group , name="add_group"),
    path('professors' , views.professors , name="professors"),
    path('add_professor' , views.add_professor , name="add_professor"),
    path('delete_professor/<int:professor_id>' , views.delete_professor , name="delete_professor")
]
