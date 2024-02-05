from django.db import models

class Professors(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Courses(models.Model):
    course = models.CharField(max_length=200)
    unit = models.IntegerField()

    def __str__(self):
        return self.course, self.unit
    
class SameTime(models.Model):
    course_1 = models.CharField(max_length=200)
    course_2 = models.CharField(max_length=200)

    def __str__(self):
        return self.course_1 , self.course_2
