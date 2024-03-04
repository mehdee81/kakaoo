import random
import time
class GAscheduler:
    def __init__(self, colors, unit, teachers, professors_limit_time, chromosomes, acceptable_interferences, courses_with_out_conditions):
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]
        self.times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.best_schedule = None
        self.lowest_lessons_with_no_section = None
        self.assigned = None
        self.teachers = teachers
        self.zoj_fard = None
        self.courses_with_no_section = []
        self.professors_limit_time = professors_limit_time
        self.chromosomes = chromosomes 
        self.acceptable_interferences = acceptable_interferences
        self.unit = unit
        self.courses_with_out_conditions = courses_with_out_conditions
        
        self.piped_courses_with_out_conditions = []
        for course in self.courses_with_out_conditions:
            self.piped_courses_with_out_conditions.append(f"|{course}|")
            
        self.courses_with_out_conditions = self.piped_courses_with_out_conditions
        

        self.courses = {}
        for color, courses in colors.items():
            _color = []
            for course in courses:
                _color.append(f"|{course}|")
            self.courses[color] = _color
        
        self.listed_all_courses = []
        for color, courses in self.courses.items():
            for course in courses:
                self.listed_all_courses.append(course)
        
        piped_units = {}
        for course, unit in self.unit.items():
            piped_units[f"|{course}|"] = unit
        self.unit = piped_units
        
        piped_teachers = {}
        for course, prof in self.teachers.items():
            piped_teachers[f"|{course}|"] =  prof
        self.teachers = piped_teachers
        
    def assign_lesson(self, lesson, group_lessons, day, time):
        assign = False
        teachers = self.teachers
        if len(self.schedule[day][time]) > 0:
            check_list = []
            assigned_lessons = self.schedule[day][time]
            for assigned_lesson in assigned_lessons:
                _append = False
                for course in group_lessons:
                    if course in assigned_lesson:  # اگر هم گروهی بودند
                        if (
                            (
                                assigned_lesson[-2:] == "_f"
                                or assigned_lesson[-2:] == "_z"
                            )
                            and (lesson[-2:] == "_f" or lesson[-2:] == "_z")
                            and (
                                teachers[lesson[:-2]] != teachers[assigned_lesson[:-2]]
                            )
                        ):
                            lesson = lesson[:-2] + assigned_lesson[-2:]
                        _append = True
                        if (
                            (
                                assigned_lesson[-2:] != "_f"
                                and assigned_lesson[-2:] != "_z"
                            )
                            and (lesson[-2:] != "_f" and lesson[-2:] != "_z")
                            and (teachers[lesson] == teachers[assigned_lesson])
                        ):
                            _append = False
                        if (
                            (
                                assigned_lesson[-2:] == "_f"
                                or assigned_lesson[-2:] == "_z"
                            )
                            and (lesson[-2:] == "_f" or lesson[-2:] == "_z")
                            and (
                                teachers[lesson[:-2]] == teachers[assigned_lesson[:-2]]
                            )
                        ):
                            if assigned_lesson[-2:] == "_f":
                                lesson = lesson[:-2] + "_z"
                            else:
                                lesson = lesson[:-2] + "_f"
                            _append = True
                        break
                    if (
                        assigned_lesson[-2:] == "_f" or assigned_lesson[-2:] == "_z"
                    ) and (lesson[-2:] == "_f" or lesson[-2:] == "_z"):
                        if assigned_lesson[-2:] == "_f":
                            lesson = lesson[:-2] + "_z"
                        else:
                            lesson = lesson[:-2] + "_f"
                check_list.append(_append)

            for check in range(len(check_list)):
                if check_list[check]:
                    assign = True
                else:
                    # اگر هم گروهی نبودند
                    if (
                        (lesson[-2:] == "_f" or lesson[-2:] == "_z")
                        and (
                            assigned_lessons[check][-2:] == "_f"
                            or assigned_lessons[check][-2:] == "_z"
                        )
                        and (lesson[-2:] != assigned_lessons[check][-2:])
                    ):
                        assign = True
                    else:
                        assign = False
                        break

            for assigned_lesson in self.schedule[day][time]:
                if lesson in assigned_lesson or assigned_lesson in lesson:
                    assign = False
                    break

        else:
            assign = True

        if assign == True:
            self.schedule[day][time].append(lesson)
            self.assigned = True
        else:
            self.assigned = False

    def assign_lessons(self):
        teachers = self.teachers
        teachers_limit_state = self.professors_limit_time
        _lessons_with_no_section = []
        
        for color_of_lesson, group_lessons in self.courses.items():
            for lesson in group_lessons:
                lesson_unit = self.unit[lesson]
                checked_sections = []
                teacher = teachers[lesson]
                if lesson_unit == 3:
                    while True:
                        day = random.choice(self.days)
                        time = random.choice(self.times)
                        if len(checked_sections) < len(self.days) * len(self.times):
                            if [day, time] not in checked_sections:
                                checked_sections.append([day, time])
                                if teacher in teachers_limit_state:
                                    if [day, time] in teachers_limit_state[teacher]:

                                        if (
                                            self.assigned == True
                                            and self.zoj_fard != None
                                        ):
                                            self.zoj_fard = random.choice(["z", "f"])
                                        elif (
                                            self.assigned == False
                                            or self.assigned == None
                                        ) and self.zoj_fard == None:
                                            self.zoj_fard = random.choice(["z", "f"])

                                        self.assign_lesson(
                                            f"{lesson}_{self.zoj_fard}",
                                            group_lessons,
                                            day,
                                            time,
                                        )
                                        if self.assigned == True:
                                            break

                                else:
                                    if self.assigned == True and self.zoj_fard != None:
                                        self.zoj_fard = random.choice(["z", "f"])
                                    elif (
                                        self.assigned == False or self.assigned == None
                                    ) and self.zoj_fard == None:
                                        self.zoj_fard = random.choice(["z", "f"])

                                    self.assign_lesson(
                                        f"{lesson}_{self.zoj_fard}",
                                        group_lessons,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break
                        else:
                            if self.assigned == False:
                                _lessons_with_no_section.append(
                                    f"{lesson}_{self.zoj_fard}"
                                )
                            break

        for color_of_lesson, group_lessons in self.courses.items():
            for lesson in group_lessons:
                lesson_unit = self.unit[lesson]
                checked_sections = []
                teacher = teachers[lesson]
                if lesson_unit == 4:
                    while True:
                        day = random.choice(self.days)
                        time = random.choice(self.times)
                        if len(checked_sections) < len(self.days) * len(self.times):
                            if [day, time] not in checked_sections:
                                checked_sections.append([day, time])
                                if teacher in teachers_limit_state:
                                    if [day, time] in teachers_limit_state[teacher]:

                                        self.assign_lesson(
                                            lesson,
                                            group_lessons,
                                            day,
                                            time,
                                        )
                                        if self.assigned == True:
                                            break

                                else:
                                    self.assign_lesson(
                                        lesson,
                                        group_lessons,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break
                        else:
                            if self.assigned == False:
                                _lessons_with_no_section.append(lesson)
                            break

        for color_of_lesson, group_lessons in self.courses.items():
            for lesson in group_lessons:
                lesson_unit = self.unit[lesson]
                checked_sections = []
                teacher = teachers[lesson]
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[teacher]:

                                    self.assign_lesson(
                                        lesson,
                                        group_lessons,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break

                            else:
                                self.assign_lesson(
                                    lesson,
                                    group_lessons,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(lesson)
                        break
            
        self.courses_with_no_section = _lessons_with_no_section
        
        for course in self.courses_with_out_conditions:
            course_teacher = teachers[course]
            group_lessons = self.listed_all_courses
            lesson_unit = self.unit[course]
            if lesson_unit == 3:
                checked_sections = []
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if course_teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[course_teacher]:

                                    if (
                                        self.assigned == True
                                        and self.zoj_fard != None
                                    ):
                                        self.zoj_fard = random.choice(["z", "f"])
                                    elif (
                                        self.assigned == False
                                        or self.assigned == None
                                    ) and self.zoj_fard == None:
                                        self.zoj_fard = random.choice(["z", "f"])

                                    self.assign_lesson(
                                        f"{course}_{self.zoj_fard}",
                                        group_lessons,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break

                            else:
                                if self.assigned == True and self.zoj_fard != None:
                                    self.zoj_fard = random.choice(["z", "f"])
                                elif (
                                    self.assigned == False or self.assigned == None
                                ) and self.zoj_fard == None:
                                    self.zoj_fard = random.choice(["z", "f"])

                                self.assign_lesson(
                                    f"{course}_{self.zoj_fard}",
                                    group_lessons,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(
                                f"{course}_{self.zoj_fard}"
                            )
                        break


            if lesson_unit == 4:
                checked_sections = []
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if course_teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[course_teacher]:

                                    self.assign_lesson(
                                        course,
                                        group_lessons,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break

                            else:
                                self.assign_lesson(
                                    course,
                                    group_lessons,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(course)
                        break
            
            checked_sections = []
            while True:
                day = random.choice(self.days)
                time = random.choice(self.times)
                if len(checked_sections) < len(self.days) * len(self.times):
                    if [day, time] not in checked_sections:
                        checked_sections.append([day, time])
                        if course_teacher in teachers_limit_state:
                            if [day, time] in teachers_limit_state[course_teacher]:

                                self.assign_lesson(
                                    course,
                                    group_lessons,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                        else:
                            self.assign_lesson(
                                course,
                                group_lessons,
                                day,
                                time,
                            )
                            if self.assigned == True:
                                break
                else:
                    if self.assigned == False:
                        _lessons_with_no_section.append(course)
                    break
            
    
    def make_solution(self):
        all_results = []
        for i in range(1, self.chromosomes+1):
            self.courses = list(self.courses.items())
            random.shuffle(self.courses)
            self.courses = dict(self.courses)
            self.assign_lessons()
            all_results.append(
                (
                    self.schedule,
                    self.courses_with_no_section,
                    len(self.courses_with_no_section),
                )
            )
            if len(self.courses_with_no_section) <= self.acceptable_interferences:
                self.schedule = {
                    day: {time: [] for time in self.times} for day in self.days
                }
                self.courses_with_no_section = []
                break
            if (i % 5000 == 0) and (i != 0):
                print(f"Chromosome {i}: Pausing for 3 seconds...")
                time.sleep(3)
            
            if i % 50000 == 0 and i != 0:
                print(f"Chromosome {i}: Pausing for 5 seconds...")
                time.sleep(5)
            
            if i % 500000 == 0 and i != 0:
                print(f"Chromosome {i}: Pausing for 10 seconds...")
                time.sleep(10)
            self.schedule = {
                day: {time: [] for time in self.times} for day in self.days
            }
            self.courses_with_no_section = []
        return all_results

    def fitness(self):
        all_results = self.make_solution()
        sorted_results = sorted(all_results, key=lambda x: x[2])
        self.best_schedule = sorted_results[0][0]
        self.lowest_lessons_with_no_section = sorted_results[0][1]

        for sorted_result in sorted_results[:10]:
            print("Courses with out section: ",sorted_result[2])

    def start(self):
        
        print("Scheduling Started With", self.chromosomes,"chromosomes", "and", self.acceptable_interferences, "Acceptable Interferences")
        start_time = time.time()
        self.fitness()
        
        end_time = time.time()
        elapsed_time = float(end_time - start_time)
        print("elapsed_time: ", elapsed_time, "Seconds")
        

    def print_schedule(self):
        for day, day_schedule in self.best_schedule.items():
            print(day)
            for time, lessons in day_schedule.items():
                lessons_with_out_pipe = []
                for lesson in lessons:
                    lessons_with_out_pipe.append(lesson.replace("|", ""))
                print(f'    {time}: {", ".join(lessons_with_out_pipe)}')