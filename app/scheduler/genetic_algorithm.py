import random
import time


class GAscheduler:
    def __init__(
        self,
        colors,
        unit,
        semesters,
        teachers,
        professors_limit_time,
        chromosomes,
        courses_with_out_conditions,
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
        self.assigned = None
        self.teachers = teachers
        self.zoj_fard = None
        self.courses_with_no_section = []
        self.professors_limit_time = professors_limit_time
        self.chromosomes = chromosomes
        self.unit = unit
        self.courses_with_out_conditions = courses_with_out_conditions
        self.semesters = semesters
        
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
                
        for course in self.courses_with_out_conditions:
            self.listed_all_courses.append(course)

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
                self.courses_number+=2
            elif self.unit[course] == 4:
                self.courses_number+=2
            else:
                self.courses_number+=1
                
    def assign_lesson(self, lesson, group_lessons, day, time):
        assign = False
        teachers = self.teachers

        if len(self.schedule[day][time]) > 0:
            check_list = []
            assigned_courses = self.schedule[day][time]

            _append = False
            change_z_f = 0
            for assigned_course in assigned_courses:
                for course in group_lessons:
                    if course in assigned_course:  # if they are in a same group
                        if assigned_course[-2:] == "_f" or assigned_course[-2:] == "_z":
                            if lesson[-2:] == "_f" or lesson[-2:] == "_z":
                                if (
                                    teachers[lesson[:-2]]
                                    != teachers[assigned_course[:-2]]
                                ):
                                    lesson = lesson[:-2] + assigned_course[-2:]
                                    _append = True
                                elif (
                                    teachers[lesson[:-2]]
                                    == teachers[assigned_course[:-2]]
                                ):
                                    if assigned_course[-2:] == lesson[-2:]:
                                        if change_z_f < 1:
                                            if assigned_course[-2:] == "_f":
                                                lesson = lesson[:-2] + "_z"
                                            else:
                                                lesson = lesson[:-2] + "_f"
                                            _append = True
                                            change_z_f += 1
                                        else:
                                            _append = False
                                    else:
                                        _append = True
                            elif lesson[-2:] != "_f" and lesson[-2:] != "_z":
                                if teachers[lesson] == teachers[assigned_course[:-2]]:
                                    _append = False
                                else:
                                    _append = True

                        elif (
                            assigned_course[-2:] != "_f"
                            and assigned_course[-2:] != "_z"
                        ):
                            if lesson[-2:] != "_f" and lesson[-2:] != "_z":
                                if teachers[lesson] == teachers[assigned_course]:
                                    _append = False
                                else:
                                    _append = True
                            elif lesson[-2:] == "_f" or lesson[-2:] == "_z":
                                if teachers[lesson[:-2]] == teachers[assigned_course]:
                                    _append = False
                                else:
                                    _append = True
                        break
                    else:
                        _append = False

                check_list.append(_append)
            
            change_z_f = 0

            if False in check_list:  # if they are not in a same group
                for check in range(len(check_list)):
                    if check_list[check] == False:
                        if (
                            assigned_courses[check][-2:] == "_f"
                            or assigned_courses[check][-2:] == "_z"
                        ):
                            if lesson[-2:] == "_f" or lesson[-2:] == "_z":
                                if change_z_f < 1:
                                    if assigned_courses[check][-2:] == "_f":
                                        lesson = lesson[:-2] + "_z"
                                    else:
                                        lesson = lesson[:-2] + "_f"
                                    assign = True
                                    change_z_f += 1
                                else:
                                    assign = False
                                    break
                            elif lesson[-2:] != "_f" and lesson[-2:] != "_z":
                                assign = False
                                break

                        elif (
                            assigned_courses[check][-2:] != "_f"
                            and assigned_courses[check][-2:] != "_z"
                        ):
                            if lesson[-2:] == "_f" or lesson[-2:] == "_z":
                                assign = False
                                break

                            elif lesson[-2:] != "_f" and lesson[-2:] != "_z":
                                assign = False
                                break
            else:
                assign = True

            for assigned_course in self.schedule[day][time]:
                if lesson in assigned_course or assigned_course in lesson:
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

        for course in self.courses_with_out_conditions:
            course_teacher = teachers[course]
            semesters = self.semesters
            group_lessons = []
            for group_course in self.listed_all_courses:
                if semesters[group_course] != semesters[course]:
                    group_lessons.append(group_course)
            
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
                            _lessons_with_no_section.append(f"{course}_{self.zoj_fard}")
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

        self.courses_with_no_section = _lessons_with_no_section

    def make_solution(self):
        all_results = []
        for i in range(1, self.chromosomes + 1):
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
            print("Courses with out section: ", sorted_result[2])

    def start(self):

        print(
            "Scheduling Started With",
            self.chromosomes,
            "chromosomes",
            "and",
            self.courses_number,
            "Courses"
        )
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





# ---------------------------------------------------test and debug--------------------------------------------------- 
# colors= {0: ['mabahes_1'], 1: ['mabahes_2'], 2: ['jabr'], 3: ['kargah_barname_nevisi'], 4: ['kargah_barname_nevisi_pishrafte', 'kargah_barname_nevisi_pishrafte_g2', 'mabani_computer'], 5: ['sakhteman_dade', 'bazyabi', 'gosaste'], 6: ['az_electriki'], 7: ['az_assembly', 'memari'], 8: ['az_memari', 'az_memari_g2'], 9: ['paygah_dade'], 10: ['mabani_hoosh_mohasebati', 'tarahi_algorithm'], 11: ['elm_robot'], 12: ['nazarie_bazi'], 13: ['web_manayi'], 14: ['mohasebat_elmi'], 15: ['barname_nevisi_pishrafte', 'narm_1'], 16: ['zaban_takhasosi', 'ravesh_pajoohesh'], 17: ['nazarie_zaban'], 18: ['compiler'], 19: ['az_system', 'az_system_g2'], 20: ['shabake', 'amar'], 21: ['az_shabake', 'az_shabake_g2']}
# units= {'mabahes_1': 3, 'mabahes_2': 3, 'jabr': 3, 'kargah_barname_nevisi': 1, 'kargah_barname_nevisi_pishrafte': 1, 'kargah_barname_nevisi_pishrafte_g2': 1, 'sakhteman_dade': 3, 'az_electriki': 1, 'az_assembly': 1, 'az_memari': 1, 'az_memari_g2': 1, 'paygah_dade': 3, 'bazyabi': 3, 'mabani_hoosh_mohasebati': 3, 'elm_robot': 3, 'nazarie_bazi': 3, 'web_manayi': 3, 'mohasebat_elmi': 3, 'mabani_computer': 3, 'barname_nevisi_pishrafte': 3, 'tarahi_algorithm': 3, 'zaban_takhasosi': 3, 'nazarie_zaban': 3, 'memari': 3, 'narm_1': 3, 'compiler': 3, 'az_system': 1, 'az_system_g2': 1, 'shabake': 3, 'amar': 3, 'gosaste': 3, 'ravesh_pajoohesh': 2, 'az_shabake': 1, 'az_shabake_g2': 1}
# semesters= {'mabahes_1': 8, 'mabahes_2': 8, 'jabr': 4, 'kargah_barname_nevisi': 1, 'kargah_barname_nevisi_pishrafte': 2, 'kargah_barname_nevisi_pishrafte_g2': 2, 'sakhteman_dade': 3, 'az_electriki': 3, 'az_assembly': 7, 'az_memari': 4, 'az_memari_g2': 4, 'paygah_dade': 5, 'bazyabi': 6, 'mabani_hoosh_mohasebati': 6, 'elm_robot': 6, 'nazarie_bazi': 8, 'web_manayi': 8, 'mohasebat_elmi': 2, 'mabani_computer': 1, 'barname_nevisi_pishrafte': 2, 'tarahi_algorithm': 4, 'zaban_takhasosi': 5, 'nazarie_zaban': 4, 'memari': 4, 'narm_1': 4, 'compiler': 8, 'az_system': 5, 'az_system_g2': 5, 'shabake': 6, 'amar': 3, 'gosaste': 2, 'ravesh_pajoohesh': 6, 'az_shabake': 6, 'az_shabake_g2': 6}
# verified_linked_courses_to_professors= {'mabahes_1': 'dr_nadjafi', 'mabahes_2': 'dr_khosravi', 'jabr': 'dr_amooshahi', 'kargah_barname_nevisi': 'dr_farangi', 'kargah_barname_nevisi_pishrafte': 'dr_khalili', 'kargah_barname_nevisi_pishrafte_g2': 'dr_khalili', 'sakhteman_dade': 'dr_rahimkhani', 'az_electriki': 'dr_ataollah', 'az_assembly': 'mohandes_rajabi', 'az_memari': 'dr_rasooli', 'az_memari_g2': 'dr_rasooli', 'paygah_dade': 'dr_khalili', 'bazyabi': 'dr_khosravi', 'mabani_hoosh_mohasebati': 'dr_khosravi', 'elm_robot': 'dr_rasooli', 'nazarie_bazi': 'dr_nadjafi', 'web_manayi': 'dr_khosravi', 'mohasebat_elmi': 'dr_rahimkhani', 'mabani_computer': 'dr_farangi', 'barname_nevisi_pishrafte': 'dr_khalili', 'tarahi_algorithm': 'dr_doostali', 'zaban_takhasosi': 'dr_nadjafi', 'nazarie_zaban': 'dr_rahimkhani', 'memari': 'dr_rasooli', 'narm_1': 'dr_khosravi', 'compiler': 'dr_doostali', 'shabake': 'mohandes_rajabi', 'amar': 'dr_mirzargar', 'gosaste': 'dr_nadjafi', 'ravesh_pajoohesh': 'dr_nadjafi', 'az_shabake': 'mohandes_rajabi', 'az_shabake_g2': 'dr_farangi', 'az_system': 'mahdi_rezaie', 'az_system_g2': 'mahdi_rezaie'}
# limited_professors= {'dr_khosravi': [['Tuesday', '8:30'], ['Tuesday', '10:30'], ['Tuesday', '13:30'], ['Tuesday', '15:30'], ['Tuesday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Wednesday', '17:30'], ['Thursday', '8:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30'], ['Thursday', '17:30']], 'dr_nadjafi': [['Tuesday', '10:30'], ['Tuesday', '13:30'], ['Tuesday', '15:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30']], 'dr_mirzargar': [['Monday', '8:30'], ['Monday', '10:30'], ['Friday', '8:30'], ['Friday', '10:30'], ['Tuesday', '8:30'], ['Tuesday', '10:30']], 'dr_rahimkhani': [['Monday', '8:30'], ['Monday', '10:30'], ['Monday', '13:30'], ['Monday', '15:30'], ['Monday', '17:30'], ['Tuesday', '8:30'], ['Tuesday', '13:30'], ['Tuesday', '10:30'], ['Tuesday', '15:30'], ['Tuesday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Wednesday', '17:30']], 'dr_khalili': [['Friday', '8:30'], ['Friday', '10:30'], ['Friday', '13:30'], ['Friday', '15:30'], ['Friday', '17:30'], ['Thursday', '8:30'], ['Thursday', '10:30'], ['Thursday', '13:30'], ['Thursday', '15:30'], ['Thursday', '17:30']], 'dr_farangi': [['Monday', '17:30'], ['Tuesday', '17:30'], ['Wednesday', '17:30'], ['Thursday', '17:30'], ['Friday', '17:30']], 'dr_doostali': [['Friday', '8:30'], ['Friday', '10:30'], ['Friday', '13:30'], ['Friday', '15:30'], ['Friday', '17:30']], 'mohandes_rajabi': [['Monday', '17:30'], ['Monday', '15:30'], ['Friday', '15:30'], ['Friday', '17:30']], 'dr_rasooli': [['Monday', '8:30'], ['Monday', '10:30'], ['Monday', '13:30'], ['Monday', '15:30'], ['Monday', '17:30'], ['Wednesday', '8:30'], ['Wednesday', '10:30'], ['Wednesday', '13:30'], ['Wednesday', '15:30'], ['Wednesday', '17:30']]}
# chromosomes= 1
# verified_courses_with_out_conditions= []


# s = GAscheduler(
#     colors,
#     units,
#     semesters,
#     verified_linked_courses_to_professors,
#     limited_professors,
#     chromosomes,
#     verified_courses_with_out_conditions,
# )
# s.start()