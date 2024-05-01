import random
import time
import copy


class GAscheduler:
    def __init__(
        self,
        colors,
        fields,
        unit,
        semesters,
        teachers,
        professors_limit_time,
        chromosomes,
        courses_with_out_conditions,
        cpu_protector,
    ):
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
        self.penalty = 0
        self.penalty_of_edge = 1
        self.best_penalty = 0
        self.penalty_history = []
        self.assigned = None
        self.teachers = teachers
        self.zoj_fard = None
        self.courses_with_no_section = []
        self.professors_limit_time = professors_limit_time
        self.chromosomes = chromosomes
        self.unit = unit
        self.courses_with_out_conditions = courses_with_out_conditions
        self.cpu_protector = cpu_protector
        self.semesters = semesters
        self.fields = fields

        self.piped_courses_with_out_conditions = []
        for course in self.courses_with_out_conditions:
            self.piped_courses_with_out_conditions.append(f"|{course}|")

        self.courses_with_out_conditions = self.piped_courses_with_out_conditions

        self.colors = {}
        for color, courses in colors.items():
            _color = []
            for course in courses:
                _color.append(f"|{course}|")
            self.colors[color] = _color

        self.courses = []
        self.group_courses = {}

        for color, courses in self.colors.items():
            _grp_course = courses
            for course in courses:
                self.courses.append(course)
                self.group_courses[course] = _grp_course

        self.listed_all_courses = self.courses

        for course in self.courses_with_out_conditions:
            self.listed_all_courses.append(course)

        for course in self.courses_with_out_conditions:
            if course in self.courses:
                self.courses.remove(course)

        piped_fields = {}
        for course, field in self.fields.items():
            piped_fields[f"|{course}|"] = field
        self.fields = piped_fields

        _fields = {}
        for course, field in self.fields.items():
            _fields[f"{course}"] = field
            _fields[f"{course}_f"] = field
            _fields[f"{course}_z"] = field
        self.fields = _fields

        piped_units = {}
        for course, unit in self.unit.items():
            piped_units[f"|{course}|"] = unit
        self.unit = piped_units

        piped_semesters = {}
        for course, semester in self.semesters.items():
            piped_semesters[f"|{course}|"] = semester
        self.semesters = piped_semesters

        piped_teachers = {}
        for course, prof in self.teachers.items():
            piped_teachers[f"|{course}|"] = prof
        self.teachers = piped_teachers

        self.courses_number = 0
        for course in self.listed_all_courses:
            if self.unit[course] == 3:
                self.courses_number += 2
            elif self.unit[course] == 4:
                self.courses_number += 2
            else:
                self.courses_number += 1

    def assign_lesson(self, new_course, group_courses, day, time):
        assign = False
        teachers = self.teachers

        if len(self.schedule[day][time]) > 0:
            check_list = []
            fields = self.fields
            assigned_courses = self.schedule[day][time]
            _append = False
            change_z_f = 0
            for assigned_course in assigned_courses:
                fields_new_course = fields[new_course]
                fields_assigned_course = fields[assigned_course]

                for course in group_courses:

                    if (course in assigned_course) or (
                        (fields_new_course != fields_assigned_course)
                        and (
                            fields_new_course != "both"
                            and fields_assigned_course != "both"
                        )
                    ):
                        if assigned_course[-2:] == "_f" or assigned_course[-2:] == "_z":
                            if new_course[-2:] == "_f" or new_course[-2:] == "_z":
                                if (
                                    teachers[new_course[:-2]]
                                    != teachers[assigned_course[:-2]]
                                ):
                                    new_course = new_course[:-2] + assigned_course[-2:]
                                    _append = True
                                elif (
                                    teachers[new_course[:-2]]
                                    == teachers[assigned_course[:-2]]
                                ):
                                    if assigned_course[-2:] == new_course[-2:]:
                                        if change_z_f < 1:
                                            if assigned_course[-2:] == "_f":
                                                new_course = new_course[:-2] + "_z"
                                            else:
                                                new_course = new_course[:-2] + "_f"
                                            _append = True
                                            change_z_f += 1
                                        else:
                                            _append = False
                                    else:
                                        _append = True
                            elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                                if (
                                    teachers[new_course]
                                    == teachers[assigned_course[:-2]]
                                ):
                                    _append = False
                                else:
                                    _append = True

                        elif (
                            assigned_course[-2:] != "_f"
                            and assigned_course[-2:] != "_z"
                        ):
                            if new_course[-2:] != "_f" and new_course[-2:] != "_z":
                                if teachers[new_course] == teachers[assigned_course]:
                                    _append = False
                                else:
                                    _append = True
                            elif new_course[-2:] == "_f" or new_course[-2:] == "_z":
                                if (
                                    teachers[new_course[:-2]]
                                    == teachers[assigned_course]
                                ):
                                    _append = False
                                else:
                                    _append = True
                        break
                    else:
                        _append = False

                check_list.append(_append)

            if False in check_list:  # if they are not in a same group
                for check in range(len(check_list)):
                    if check_list[check] == False:
                        if (
                            assigned_courses[check][-2:] == "_f"
                            or assigned_courses[check][-2:] == "_z"
                        ):
                            if new_course[-2:] == "_f" or new_course[-2:] == "_z":

                                if assigned_courses[check][-2:] == new_course[-2:]:
                                    if (
                                        teachers[assigned_courses[check][:-2]]
                                        != teachers[new_course[:-2]]
                                    ):
                                        self.penalty_history.append((day,time,new_course))
                                        self.penalty += self.penalty_of_edge
                                        assign = True
                                    else:
                                        assign = False
                                        break
                                else:
                                    if (
                                        teachers[assigned_courses[check][:-2]]
                                        != teachers[new_course[:-2]]
                                    ):
                                        assign = True
                                    else:
                                        assign = False
                                        break

                            elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                                if (
                                    teachers[assigned_courses[check][:-2]]
                                    != teachers[new_course]
                                ):
                                    self.penalty_history.append((day,time,new_course))
                                    self.penalty += self.penalty_of_edge
                                    assign = True
                                else:
                                    assign = False
                                    break

                        elif (
                            assigned_courses[check][-2:] != "_f"
                            and assigned_courses[check][-2:] != "_z"
                        ):
                            if new_course[-2:] == "_f" or new_course[-2:] == "_z":

                                if (
                                    teachers[assigned_courses[check]]
                                    != teachers[new_course[:-2]]
                                ):
                                    self.penalty_history.append((day,time,new_course))
                                    self.penalty += self.penalty_of_edge
                                    assign = True
                                else:
                                    assign = False
                                    break

                            elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                                if (
                                    teachers[assigned_courses[check]]
                                    != teachers[new_course]
                                ):
                                    self.penalty_history.append((day,time,new_course))
                                    self.penalty += self.penalty_of_edge
                                    assign = True
                                else:
                                    assign = False
                                    break
            else:
                assign = True

            for assigned_course in self.schedule[day][time]:
                if new_course in assigned_course or assigned_course in new_course:
                    assign = False
                    break

        else:
            assign = True

        if assign == True:
            self.schedule[day][time].append(new_course)
            self.assigned = True
        else:
            self.assigned = False

    def assign_lessons(self, courses, group_courses):
        teachers = self.teachers
        teachers_limit_state = self.professors_limit_time
        _lessons_with_no_section = []

        for course in courses:
            course_unit = self.unit[course]
            checked_sections = []
            teacher = teachers[course]
            if course_unit == 3:
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[teacher]:

                                    if self.assigned == True and self.zoj_fard != None:
                                        self.zoj_fard = random.choice(["z", "f"])
                                    elif (
                                        self.assigned == False or self.assigned == None
                                    ) and self.zoj_fard == None:
                                        self.zoj_fard = random.choice(["z", "f"])

                                    self.assign_lesson(
                                        f"{course}_{self.zoj_fard}",
                                        group_courses[course],
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
                                    group_courses[course],
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(f"{course}_{self.zoj_fard}")
                        break

        for course in courses:

            coures_unit = self.unit[course]
            checked_sections = []
            teacher = teachers[course]
            if coures_unit == 4:
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[teacher]:

                                    self.assign_lesson(
                                        course,
                                        group_courses[course],
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break

                            else:
                                self.assign_lesson(
                                    course,
                                    group_courses[course],
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(course)
                        break

        for course in courses:

            course_unit = self.unit[course]
            checked_sections = []
            teacher = teachers[course]
            while True:
                day = random.choice(self.days)
                time = random.choice(self.times)
                if len(checked_sections) < len(self.days) * len(self.times):
                    if [day, time] not in checked_sections:
                        checked_sections.append([day, time])
                        if teacher in teachers_limit_state:
                            if [day, time] in teachers_limit_state[teacher]:

                                self.assign_lesson(
                                    course,
                                    group_courses[course],
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break

                        else:
                            self.assign_lesson(
                                course,
                                group_courses[course],
                                day,
                                time,
                            )
                            if self.assigned == True:
                                break
                else:
                    if self.assigned == False:
                        _lessons_with_no_section.append(course)
                    break

        for new_course in self.courses_with_out_conditions:
            new_course_teacher = teachers[new_course]
            semesters = self.semesters
            new_course_group = []
            for course in courses:
                if semesters[new_course] != semesters[course]:
                    new_course_group.append(course)

            new_course_unit = self.unit[new_course]
            if new_course_unit == 3:
                checked_sections = []
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if new_course_teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[
                                    new_course_teacher
                                ]:

                                    if self.assigned == True and self.zoj_fard != None:
                                        self.zoj_fard = random.choice(["z", "f"])
                                    elif (
                                        self.assigned == False or self.assigned == None
                                    ) and self.zoj_fard == None:
                                        self.zoj_fard = random.choice(["z", "f"])

                                    self.assign_lesson(
                                        f"{new_course}_{self.zoj_fard}",
                                        new_course_group,
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
                                    f"{new_course}_{self.zoj_fard}",
                                    new_course_group,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(
                                f"{new_course}_{self.zoj_fard}"
                            )
                        break

            if new_course_unit == 4:
                checked_sections = []
                while True:
                    day = random.choice(self.days)
                    time = random.choice(self.times)
                    if len(checked_sections) < len(self.days) * len(self.times):
                        if [day, time] not in checked_sections:
                            checked_sections.append([day, time])
                            if new_course_teacher in teachers_limit_state:
                                if [day, time] in teachers_limit_state[
                                    new_course_teacher
                                ]:

                                    self.assign_lesson(
                                        new_course,
                                        new_course_group,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break

                            else:
                                self.assign_lesson(
                                    new_course,
                                    new_course_group,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                    else:
                        if self.assigned == False:
                            _lessons_with_no_section.append(new_course)
                        break

            checked_sections = []
            while True:
                day = random.choice(self.days)
                time = random.choice(self.times)
                if len(checked_sections) < len(self.days) * len(self.times):
                    if [day, time] not in checked_sections:
                        checked_sections.append([day, time])
                        if new_course_teacher in teachers_limit_state:
                            if [day, time] in teachers_limit_state[new_course_teacher]:

                                self.assign_lesson(
                                    new_course,
                                    new_course_group,
                                    day,
                                    time,
                                )
                                if self.assigned == True:
                                    break
                        else:
                            self.assign_lesson(
                                new_course,
                                new_course_group,
                                day,
                                time,
                            )
                            if self.assigned == True:
                                break
                else:
                    if self.assigned == False:
                        _lessons_with_no_section.append(new_course)
                    break

        self.courses_with_no_section = _lessons_with_no_section

    def make_solution(self):
        solutions = []
        for i in range(1, self.chromosomes + 1):
            courses = self.courses
            group_courses = self.group_courses
            self.assign_lessons(courses, group_courses)
            solutions.append(
                (
                    self.schedule,
                    self.courses_with_no_section,
                    len(self.courses_with_no_section) + self.penalty,
                    self.penalty_history,
                )
            )

            if (i % 5000 == 0) and (i != 0):
                if self.cpu_protector == "on":
                    print(f"Chromosome {i}: Pausing for 3 seconds...")
                    time.sleep(3)
                else:
                    print(f"Chromosome {i}")

            if i % 50000 == 0 and i != 0:
                if self.cpu_protector == "on":
                    print(f"Chromosome {i}: Pausing for 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Chromosome {i}")

            if i % 500000 == 0 and i != 0:
                if self.cpu_protector == "on":
                    print(f"Chromosome {i}: Pausing for 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"Chromosome {i}")

            self.schedule = {
                day: {time: [] for time in self.times} for day in self.days
            }
            self.penalty = 0
            self.penalty_history = []
            self.courses_with_no_section = []
        return solutions

    def mutation(self, solutions):
        print("-------------------------------------------mutation started-------------------------------------------")
        new_chromosomes = []
        
        for i in range(5000):
            sorted_solutions = sorted(solutions, key=lambda x: x[2])
            rankedSoulutions = sorted_solutions[:10]
            for solution, courses_with_no_section, penalty, penalty_history in rankedSoulutions:
                # Copy the solution to avoid modifying the original
                mutated_solution = copy.deepcopy(solution)
                
                # Select two random days
                selected_days = random.sample(self.days, 3)
                
                # Set the new schedule
                self.schedule = mutated_solution
                self.penalty = penalty
                
                # Append the courses of the selected days to selected_courses
                selected_courses = []
                for day in selected_days:
                    for tm in self.times:
                        selected_courses.extend(mutated_solution[day][tm])
                        
                
                selected_courses = selected_courses + courses_with_no_section
                random.shuffle(selected_courses)
                
                # Decrasing the penalty of leassons that removed
                for course in selected_courses:
                    for day in selected_days:
                        for tm in self.times:
                            if (day, tm, course) in penalty_history:
                                self.penalty = self.penalty-1 
                
                
                # Clear the courses from the selected days
                for day in selected_days:
                    for tm in self.times:
                        mutated_solution[day][tm] = []
                    
                
                teachers = self.teachers
                teachers_limit_state = self.professors_limit_time
                _lessons_with_no_section = []

                for course in selected_courses:
                    checked_sections = []
                    if course[-2:] == "_f" or course[-2:] == "_z": 
                        teacher = teachers[course[:-2]]
                    else:
                        teacher = teachers[course]
                        
                    group_courses = self.group_courses
                    
                    while True:
                        day = random.choice(self.days)
                        time = random.choice(self.times)
                        if len(checked_sections) < len(self.days) * len(self.times):
                            if [day, time] not in checked_sections:
                                checked_sections.append([day, time])
                                if teacher in teachers_limit_state:
                                    if [day, time] in teachers_limit_state[teacher]:
                                        
                                        if course[-2:] == "_f" or course[-2:] == "_z":
                                            group_course = group_courses[course[:-2]]
                                            course = f"{course[:-2]}{random.choice(['_f','_z'])}"
                                        else:
                                            group_course = group_courses[course]
                                            
                                        self.assign_lesson(
                                            course,
                                            group_course,
                                            day,
                                            time,
                                        )
                                        if self.assigned == True:
                                            break

                                else:
                                    
                                    if course[-2:] == "_f" or course[-2:] == "_z": 
                                        group_course = group_courses[course[:-2]]
                                        course = f"{course[:-2]}{random.choice(['_f','_z'])}"
                                    else:
                                        group_course = group_courses[course]
                                        
                                    self.assign_lesson(
                                        course,
                                        group_course,
                                        day,
                                        time,
                                    )
                                    if self.assigned == True:
                                        break
                        else:
                            if self.assigned == False:
                                _lessons_with_no_section.append(course)
                            break
                        
                # self.courses_with_no_section = _lessons_with_no_section
                
                # Add the mutated solution to the new generation
                new_chromosomes.append((mutated_solution, _lessons_with_no_section, self.penalty, self.penalty_history))
                self.penalty_history = []
            if i < 100:
                print(f"New Gen Penalty[{i}]: ", sorted(new_chromosomes, key=lambda x: x[2])[0][2])
                
            elif i % 100 ==  0 and i != 0:
                print(f"New Gen Penalty[{i}]: ", sorted(new_chromosomes, key=lambda x: x[2])[0][2])
            
            solutions = sorted(solutions, key=lambda x: x[2])
            # Remove the last 10 chromosomes
            solutions = solutions[:-len(new_chromosomes)]
            solutions += new_chromosomes
        return new_chromosomes
    
    def start(self):

        print(
            "Scheduling Started With",
            self.chromosomes,
            "chromosomes",
            "and",
            self.courses_number,
            "Courses",
        )
        start_time = time.time()

        solutions = self.make_solution()
        new_chromosomes = self.mutation(solutions)
        sorted_chromosomes = sorted(new_chromosomes, key=lambda x: x[2])

        self.best_schedule = sorted_chromosomes[0][0]
        self.lowest_lessons_with_no_section = sorted_chromosomes[0][1]
        self.best_penalty = sorted_chromosomes[0][2]

        for sorted_result in sorted_chromosomes[:10]:
            print("Penalty of New Chromosomes: ", sorted_result[2])

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


# ---------------------------------------------------start and debug---------------------------------------------------
# colors= {0: ['mabahes_1'], 1: ['mabahes_2'], 2: ['jabr'], 3: ['kargah_barname_nevisi'], 4: ['kargah_barname_nevisi_pishrafte', 'kargah_barname_nevisi_pishrafte_g2', 'mabani_computer'], 5: ['sakhteman_dade', 'bazyabi', 'gosaste'], 6: ['az_electriki'], 7: ['az_assembly', 'memari'], 8: ['az_memari', 'az_memari_g2'], 9: ['paygah_dade'], 10: ['mabani_hoosh_mohasebati', 'tarahi_algorithm'], 11: ['elm_robot'], 12: ['nazarie_bazi'], 13: ['web_manayi'], 14: ['mohasebat_elmi'], 15: ['barname_nevisi_pishrafte', 'narm_1'], 16: ['zaban_takhasosi', 'ravesh_pajoohesh'], 17: ['nazarie_zaban'], 18: ['compiler'], 19: ['az_system', 'az_system_g2'], 20: ['shabake', 'amar'], 21: ['az_shabake', 'az_shabake_g2'], 22: ['az_madar_e'], 23: ['ravesh_amari'], 24: ['system_amel'], 25: ['mabani_oloom_riazi'], 26: ['mabani_analyze_riazi'], 27: ['mabani_analyze_jabr'], 28: ['mabani_trakibiat'], 29: ['riazi_1'], 30: ['riazi_2']}
# fields= {'mabahes_1': 'both', 'mabahes_2': 'both', 'jabr': 'both', 'kargah_barname_nevisi': 'both', 'kargah_barname_nevisi_pishrafte': 'both', 'kargah_barname_nevisi_pishrafte_g2': 'both', 'sakhteman_dade': 'both', 'az_electriki': 'first', 'az_assembly': 'first', 'az_memari': 'first', 'az_memari_g2': 'first', 'paygah_dade': 'both', 'bazyabi': 'first', 'mabani_hoosh_mohasebati': 'first', 'elm_robot': 'first', 'nazarie_bazi': 'both', 'web_manayi': 'first', 'mohasebat_elmi': 'first', 'mabani_computer': 'both', 'barname_nevisi_pishrafte': 'both', 'tarahi_algorithm': 'both', 'zaban_takhasosi': 'both', 'nazarie_zaban': 'both', 'memari': 'both', 'narm_1': 'both', 'compiler': 'first', 'az_system': 'first', 'az_system_g2': 'first', 'shabake': 'both', 'amar': 'first', 'gosaste': 'first', 'ravesh_pajoohesh': 'both', 'az_shabake': 'first', 'az_shabake_g2': 'first', 'az_madar_e': 'first', 'ravesh_amari': 'both', 'system_amel': 'both', 'mabani_oloom_riazi': 'second', 'mabani_analyze_riazi': 'second', 'mabani_analyze_jabr': 'second', 'mabani_trakibiat': 'second', 'riazi_1': 'both', 'riazi_2': 'both'}
# units= {'mabahes_1': 3, 'mabahes_2': 3, 'jabr': 3, 'kargah_barname_nevisi': 1, 'kargah_barname_nevisi_pishrafte': 1, 'kargah_barname_nevisi_pishrafte_g2': 1, 'sakhteman_dade': 3, 'az_electriki': 1, 'az_assembly': 1, 'az_memari': 1, 'az_memari_g2': 1, 'paygah_dade': 3, 'bazyabi': 3, 'mabani_hoosh_mohasebati': 3, 'elm_robot': 3, 'nazarie_bazi': 3, 'web_manayi': 3, 'mohasebat_elmi': 3, 'mabani_computer': 3, 'barname_nevisi_pishrafte': 3, 'tarahi_algorithm': 3, 'zaban_takhasosi': 3, 'nazarie_zaban': 3, 'memari': 3, 'narm_1': 3, 'compiler': 3, 'az_system': 1, 'az_system_g2': 1, 'shabake': 3, 'amar': 3, 'gosaste': 3, 'ravesh_pajoohesh': 2, 'az_shabake': 1, 'az_shabake_g2': 1, 'az_madar_e': 1, 'ravesh_amari': 1, 'system_amel': 3, 'mabani_oloom_riazi': 4, 'mabani_analyze_riazi': 4, 'mabani_analyze_jabr': 4, 'mabani_trakibiat': 4, 'riazi_1': 4, 'riazi_2': 4}
# semesters= {'mabahes_1': 8, 'mabahes_2': 8, 'jabr': 4, 'kargah_barname_nevisi': 1, 'kargah_barname_nevisi_pishrafte': 2, 'kargah_barname_nevisi_pishrafte_g2': 2, 'sakhteman_dade': 3, 'az_electriki': 3, 'az_assembly': 7, 'az_memari': 4, 'az_memari_g2': 4, 'paygah_dade': 5, 'bazyabi': 6, 'mabani_hoosh_mohasebati': 6, 'elm_robot': 6, 'nazarie_bazi': 8, 'web_manayi': 8, 'mohasebat_elmi': 2, 'mabani_computer': 1, 'barname_nevisi_pishrafte': 2, 'tarahi_algorithm': 4, 'zaban_takhasosi': 5, 'nazarie_zaban': 4, 'memari': 4, 'narm_1': 4, 'compiler': 8, 'az_system': 5, 'az_system_g2': 5, 'shabake': 6, 'amar': 3, 'gosaste': 2, 'ravesh_pajoohesh': 6, 'az_shabake': 6, 'az_shabake_g2': 6, 'az_madar_e': 3, 'ravesh_amari': 3, 'system_amel': 5, 'mabani_oloom_riazi': 1, 'mabani_analyze_riazi': 2, 'mabani_analyze_jabr': 3, 'mabani_trakibiat': 4, 'riazi_1': 1, 'riazi_2': 2}
# verified_linked_courses_to_professors= {'mabahes_1': 'dr_nadjafi', 'mabahes_2': 'dr_khosravi', 'jabr': 'dr_amooshahi', 'kargah_barname_nevisi': 'dr_farangi', 'kargah_barname_nevisi_pishrafte': 'dr_khalili', 'kargah_barname_nevisi_pishrafte_g2': 'dr_khalili', 'sakhteman_dade': 'dr_rahimkhani', 'az_electriki': 'dr_ataollah', 'az_assembly': 'mohandes_rajabi', 'az_memari': 'dr_rasooli', 'az_memari_g2': 'dr_rasooli', 'paygah_dade': 'dr_khalili', 'bazyabi': 'dr_khosravi', 'mabani_hoosh_mohasebati': 'dr_khosravi', 'elm_robot': 'dr_rasooli', 'nazarie_bazi': 'dr_nadjafi', 'web_manayi': 'dr_khosravi', 'mohasebat_elmi': 'dr_rahimkhani', 'mabani_computer': 'dr_farangi', 'barname_nevisi_pishrafte': 'dr_khalili', 'tarahi_algorithm': 'dr_doostali', 'zaban_takhasosi': 'dr_nadjafi', 'nazarie_zaban': 'dr_rahimkhani', 'memari': 'dr_rasooli', 'narm_1': 'dr_khosravi', 'compiler': 'dr_doostali', 'shabake': 'mohandes_rajabi', 'amar': 'dr_mirzargar', 'gosaste': 'dr_nadjafi', 'ravesh_pajoohesh': 'dr_nadjafi', 'az_shabake': 'mohandes_rajabi', 'az_shabake_g2': 'dr_farangi', 'az_system': 'mahdi_rezaie', 'az_system_g2': 'mahdi_rezaie', 'az_madar_e': 'dr_ataollah', 'ravesh_amari': 'dr_heydari', 'system_amel': 'dr_doostali', 'mabani_oloom_riazi': 'dr_mirzargar', 'mabani_analyze_jabr': 'dr_mirzargar', 'mabani_analyze_riazi': 'dr_heydari', 'mabani_trakibiat': 'dr_soofi', 'riazi_1': 'dr_soofi', 'riazi_2': 'dr_amooshahi'}
# limited_professors= {'dr_khosravi': [['Tuesday', '8:30'], ['Tuesday', '10:30'], ['Tuesday', '13:30'], ['Tuesday', '15:30'], ['Tuesday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Thursday', '8:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30'], ['Thursday', '17:30']], 'dr_nadjafi': [['Tuesday', '10:30'], ['Tuesday', '13:30'], ['Tuesday', '15:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30']], 'dr_mirzargar': [['Monday', '8:30'], ['Monday', '10:30'], ['Friday', '8:30'], ['Friday', '10:30'], ['Tuesday', '8:30'], ['Tuesday', '10:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30']], 'dr_rahimkhani': [['Monday', '8:30'], ['Monday', '10:30'], ['Monday', '13:30'], ['Monday', '15:30'], ['Tuesday', '8:30'], ['Tuesday', '13:30'], ['Tuesday', '10:30'], ['Tuesday', '15:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30']], 'dr_khalili': [['Friday', '8:30'], ['Friday', '10:30'], ['Friday', '13:30'], ['Friday', '15:30'], ['Friday', '17:30'], ['Thursday', '8:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30'], ['Thursday', '17:30']], 'dr_farangi': [['Monday', '17:30'], ['Tuesday', '17:30'], ['Wednesday', '17:30'], ['Thursday', '17:30'], ['Friday', '17:30']], 'dr_doostali': [['Friday', '8:30'], ['Friday', '10:30'], ['Friday', '13:30'], ['Friday', '15:30'], ['Friday', '17:30']], 'mohandes_rajabi': [['Monday', '17:30'], ['Monday', '15:30'], ['Friday', '15:30'], ['Friday', '17:30']], 'dr_rasooli': [['Monday', '8:30'], ['Monday', '10:30'], ['Monday', '13:30'], ['Monday', '15:30'], ['Monday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Wednesday', '17:30']], 'dr_amooshahi': [['Monday', '8:30'], ['Monday', '10:30'], ['Tuesday', '10:30'], ['Wednesday', '10:30'], ['Thursday', '8:30'], ['Thursday', '10:30']], 'dr_ataollah': [['Tuesday', '8:30'], ['Tuesday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '17:30']], 'mahdi_rezaie': [['Tuesday', '15:30'], ['Tuesday', '17:30'], ['Wednesday', '15:30'], ['Wednesday', '17:30'], ['Thursday', '15:30'], ['Thursday', '17:30']], 'dr_heydari': [['Monday', '8:30'], ['Monday', '10:30'], ['Tuesday', '8:30'], ['Tuesday', '10:30'], ['Tuesday', '13:30'], ['Tuesday', '15:30'], ['Tuesday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30']], 'dr_soofi': [['Tuesday', '17:30'], ['Wednesday', '17:30'], ['Thursday', '17:30']]}
# chromosomes= 600
# verified_courses_with_out_conditions= []
# cpu_protector= "on"

# s = GAscheduler(
#     colors,
#     fields,
#     units,
#     semesters,
#     verified_linked_courses_to_professors,
#     limited_professors,
#     chromosomes,
#     verified_courses_with_out_conditions,
#     cpu_protector
# )
# s.start()
# ---------------------------------------------------end debuging------------------------------------------------------
