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
    path('delete_professor/<int:professor_id>' , views.delete_professor , name="delete_professor"),
    
    path('pre_requirements' , views.sametimes , name="sametimes"),
    path('delete_sametime/<int:sametime_id>' , views.delete_sametime , name="delete_sametime"),
    path('add_sametime' , views.add_sametime , name="add_sametime"),
    
    path('c_to_p' , views.c_to_p , name="c_to_p"),
    path('add_c_to_p' , views.add_c_to_p , name="add_c_to_p"),
    path('delete_c_to_p/<int:c_to_p_id>' , views.delete_c_to_p , name="delete_c_to_p"),
    
    path('professors_limit' , views.professors_limit , name="professors_limit"),
    path('add_professors_limit' , views.add_professors_limit , name="add_professors_limit"),
    path('delete_professors_limit/<int:professors_limit_id>' , views.delete_professors_limit , name="delete_professors_limit"),
]