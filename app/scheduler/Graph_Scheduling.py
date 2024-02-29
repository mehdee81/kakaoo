import random
import copy
import itertools


class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.adj_dict = {}
        self.create_adj_dict()

    def create_adj_dict(self):
        for start, dist in self.edges:
            if start in self.adj_dict:
                self.adj_dict[start].append(dist)
            else:
                self.adj_dict[start] = [dist]

        for dist, start in self.edges:
            if start in self.adj_dict:
                self.adj_dict[start].append(dist)
            else:
                self.adj_dict[start] = [dist]

    # harisane
    def color_graph_h(self):
        num_colors = len(self.adj_dict.keys())
        colors = {node: None for node in self.adj_dict.keys()}
        for node in self.adj_dict.keys():
            available_colors = set(range(num_colors)) - set(
                colors[nei] for nei in self.adj_dict[node] if colors[nei] is not None
            )
            if available_colors:
                colors[node] = min(available_colors)

        output_dict = {}
        for key, value in colors.items():
            if value in output_dict:
                output_dict[value].append(key)
            else:
                output_dict[value] = [key]
        return output_dict

    # backtracking
    def color_graph_b(self):

        num_colors = len(self.adj_dict)

        node_colors = {node: None for node in self.adj_dict}

        def is_valid_color(node, color):
            for neighbor in self.adj_dict[node]:
                if node_colors[neighbor] == color:
                    return False
            return True

        def color_node(node, color):
            if color > num_colors:
                return False

            if node_colors[node] is not None:
                return True

            for i in range(1, color + 1):
                if is_valid_color(node, i):
                    node_colors[node] = i
                    if all(
                        color_node(neighbor, color) for neighbor in self.adj_dict[node]
                    ):
                        return True
                    node_colors[node] = None

            return False

        color_node(next(iter(self.adj_dict)), num_colors)

        output_dict = {}
        for key, value in node_colors.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict


class InOrderSchedule:
    def __init__(self, colors, vahed, teachers, professors_limit_time):
        self.days = [
            "shanbe",
            "1 shanbe",
            "2 shanbe",
            "3 shanbe",
            "4 shanbe",
        ]
        self.times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.vahed = vahed
        self.assigned = None
        self.teachers = teachers
        self.zoj_fard = None
        self.lessons_with_no_time = []
        self.professors_limit_time = professors_limit_time
        colors = dict(
            sorted(colors.items(), key=lambda item: len(item[1]), reverse=True)
        )
        score_of_colors = {}
        for number, list in colors.items():
            score = 0
            for lesson in list:
                s = vahed[lesson]
                if vahed[lesson] == 4:
                    s = s - 1
                score += s
            score_of_colors[number] = score

        self.lessons = {
            k: colors[k]
            for k in sorted(score_of_colors, key=score_of_colors.get, reverse=True)
        }

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
        _lessons_with_no_time = []
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_unit = self.vahed[lesson]
                for day in self.days:
                    teacher = teachers[lesson]
                    if teacher in teachers_limit_state:
                        if day in teachers_limit_state[teacher]:
                            for time in self.times:
                                if lesson_unit == 3:
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
                            if self.assigned == True:
                                break
                    else:
                        for time in self.times:
                            if lesson_unit == 3:
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
                        if self.assigned == True:
                            break

                if self.assigned == False:
                    _lessons_with_no_time.append(lesson)

        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_unit = self.vahed[lesson]
                for day in self.days:
                    teacher = teachers[lesson]
                    if teacher in teachers_limit_state:
                        if day in teachers_limit_state[teacher]:
                            for time in self.times:
                                if lesson_unit == 4:
                                    self.assign_lesson(lesson, group_lessons, day, time)

                                if self.assigned == True:
                                    break
                            if self.assigned == True:
                                break
                    else:
                        for time in self.times:
                            if lesson_unit == 4:
                                self.assign_lesson(lesson, group_lessons, day, time)

                            if self.assigned == True:
                                break
                        if self.assigned == True:
                            break

                if self.assigned == False:
                    _lessons_with_no_time.append(lesson)

        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                for day in self.days:
                    teacher = teachers[lesson]
                    if teacher in teachers_limit_state:
                        if day in teachers_limit_state[teacher]:
                            for time in self.times:
                                self.assign_lesson(lesson, group_lessons, day, time)
                                if self.assigned == True:
                                    break
                            if self.assigned == True:
                                break
                    else:
                        for time in self.times:
                            self.assign_lesson(lesson, group_lessons, day, time)
                            if self.assigned == True:
                                break
                        if self.assigned == True:
                            break

                if self.assigned == False:
                    _lessons_with_no_time.append(lesson)

        self.lessons_with_no_time = _lessons_with_no_time

    def print_schedule(self):
        for day, day_schedule in self.schedule.items():
            print(day)
            for time, lessons in day_schedule.items():
                lessons_with_out_pipe = []
                for lesson in lessons:
                    lessons_with_out_pipe.append(lesson.replace("|", ""))
                print(f'    {time}: {", ".join(lessons_with_out_pipe)}')


class GAschedule:
    def __init__(self, colors, vahed, teachers, professors_limit_time):
        self.days = [
            "shanbe",
            "1 shanbe",
            "2 shanbe",
            "3 shanbe",
            "4 shanbe",
        ]
        self.times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.vahed = vahed
        self.assigned = None
        self.teachers = teachers
        self.zoj_fard = None
        self.lessons_with_no_time = []
        self.professors_limit_time = professors_limit_time
        colors = dict(
            sorted(colors.items(), key=lambda item: len(item[1]), reverse=True)
        )
        score_of_colors = {}
        for number, list in colors.items():
            score = 0
            for lesson in list:
                s = vahed[lesson]
                if vahed[lesson] == 4:
                    s = s - 1
                score += s
            score_of_colors[number] = score

        self.lessons = {
            k: colors[k]
            for k in sorted(score_of_colors, key=score_of_colors.get, reverse=True)
        }

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
        _lessons_with_no_time = []

        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_unit = self.vahed[lesson]
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
                                _lessons_with_no_time.append(f"{lesson}_{self.zoj_fard}")
                            break

        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_unit = self.vahed[lesson]
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
                                _lessons_with_no_time.append(lesson)
                            break

        for color_of_lesson, group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_unit = self.vahed[lesson]
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
                            _lessons_with_no_time.append(lesson)
                        break

        self.lessons_with_no_time = _lessons_with_no_time

    def print_schedule(self):
        for day, day_schedule in self.schedule.items():
            print(day)
            for time, lessons in day_schedule.items():
                lessons_with_out_pipe = []
                for lesson in lessons:
                    lessons_with_out_pipe.append(lesson.replace("|", ""))
                print(f'    {time}: {", ".join(lessons_with_out_pipe)}')
