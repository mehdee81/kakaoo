import random
import copy
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
    def __init__(self, colors, vahed, teachers , all_teachers_limit_states):
        self.days = [
            "shanbe",
            "1 shanbe",
            "2 shanbe",
            "3 shanbe",
            "4 shanbe",
        ]
        self.times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.best_schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.vahed = vahed
        self.assigned = None
        self.teachers = teachers
        self.all_teachers_limit_states = all_teachers_limit_states
        self.zoj_fard = None
        
        colors = dict(sorted(colors.items(), key=lambda item: len(item[1]), reverse=True))
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
            k: colors[k] for k in sorted(score_of_colors, key=score_of_colors.get, reverse=True)
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
                    if course in assigned_lesson:
                        if ((assigned_lesson[-2:] == '_f' or assigned_lesson[-2:] == '_z') and (lesson[-2:] == '_f' or lesson[-2:] == '_z') and (teachers[lesson[:-2]] != teachers[assigned_lesson[:-2]])):
                            lesson = lesson[:-2] + assigned_lesson[-2:]
                        _append = True
                        break
                    if ((assigned_lesson[-2:] == '_f' or assigned_lesson[-2:] == '_z') and (lesson[-2:] == '_f' or lesson[-2:] == '_z')):
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
        all_teachers_limit_states = self.all_teachers_limit_states 
        score = 0
        temp_best_schedule = {day: {time: [] for time in self.times} for day in self.days}
        
        for teacher_limit_state in all_teachers_limit_states:
            _score = 0
            self.schedule = {day: {time: [] for time in self.times} for day in self.days}
            for color_of_lesson , group_lessons in self.lessons.items():
                for lesson in group_lessons:
                    lesson_vahed = self.vahed[lesson]
                    for day in self.days:
                        for time in self.times:
                            
                            teacher = teachers[lesson]
                            
                            if teacher not in teacher_limit_state:
                                teacher_can = True
                                pass
                            else:
                                if len(teacher_limit_state[teacher]) == 2:
                                    if teacher_limit_state[teacher] != [day , time]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                elif len(teacher_limit_state[teacher]) == 1:
                                    if teacher_limit_state[teacher] != [day]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                        
                                if teacher_limit_state[teacher] == [day , time]:
                                    teacher_can = True
                                    
                            if teacher_can:
                                if lesson_vahed == 3:
                                    if self.assigned == True and self.zoj_fard != None:
                                        self.zoj_fard = random.choice(["z", "f"])
                                    elif (self.assigned == False or self.assigned == None) and self.zoj_fard == None:
                                        self.zoj_fard = random.choice(["z", "f"])
                                        
                                    self.assign_lesson(f"{lesson}_{self.zoj_fard}", group_lessons, day, time)
                            
                            if self.assigned == True:
                                break       
                        if self.assigned == True:
                            break

            for color_of_lesson , group_lessons in self.lessons.items():
                for lesson in group_lessons:
                    lesson_vahed = self.vahed[lesson]
                    for day in self.days:
                        for time in self.times:
                        
                            teacher = teachers[lesson]
                            if teacher not in teacher_limit_state:
                                teacher_can = True
                                pass
                            else:
                                if len(teacher_limit_state[teacher]) == 2:
                                    if teacher_limit_state[teacher] != [day , time]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                elif len(teacher_limit_state[teacher]) == 1:
                                    if teacher_limit_state[teacher] != [day]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                        
                                if teacher_limit_state[teacher] == [day , time]:
                                    teacher_can = True

                            if teacher_can:
                                if lesson_vahed == 4:
                                    self.assign_lesson(lesson, group_lessons, day, time)
                                
                            if self.assigned == True:
                                break
                        if self.assigned == True:
                            break
            
            for day, day_schedule in self.schedule.items():            
                _score += len(day_schedule) ** 2

            if _score > score:
                temp_best_schedule = copy.deepcopy(self.schedule)
                score = _score
        
        self.schedule = temp_best_schedule
        self.best_schedule = copy.deepcopy(temp_best_schedule)
        
        pre_not_assigned_lessons = float('inf') 
        for teacher_limit_state in all_teachers_limit_states:
            self.schedule = copy.deepcopy(temp_best_schedule)   
            not_assigned_lessons = []
            
            for color_of_lesson , group_lessons in self.lessons.items():
                for lesson in group_lessons:
                    lesson_vahed = self.vahed[lesson]
                    
                    for day in self.days:
                        for time in self.times:
                            
                            teacher = teachers[lesson]
                            
                            if teacher not in teacher_limit_state:
                                teacher_can = True
                                pass
                            else:
                                if len(teacher_limit_state[teacher]) == 2:
                                    if teacher_limit_state[teacher] != [day , time]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                elif len(teacher_limit_state[teacher]) == 1:
                                    if teacher_limit_state[teacher] != [day]:
                                        if self.assigned == True:
                                            self.assigned = False
                                        teacher_can = False
                                        
                                if teacher_limit_state[teacher] == [day , time]:
                                    teacher_can = True
                                
                            if teacher_can:
                                self.assign_lesson(lesson, group_lessons, day, time)
                           
                            if self.assigned == True:
                                break
                        if self.assigned == True:
                            break
                        
                    if self.assigned == False:
                        not_assigned_lessons.append(f"{lesson}")
        
            if len(not_assigned_lessons) == 0 or len(not_assigned_lessons) < pre_not_assigned_lessons:
                self.best_schedule = copy.deepcopy(self.schedule)
                pre_not_assigned_lessons = len(not_assigned_lessons)
            else:
                pre_not_assigned_lessons = len(not_assigned_lessons)             
            

    def print_schedule(self):
        for day, day_schedule in self.best_schedule.items():
            print(day)
            for time, lessons in day_schedule.items():
                lessons_with_out_pipe = []
                for lesson in lessons:
                    lessons_with_out_pipe.append(lesson.replace("|" , ""))
                print(f'    {time}: {", ".join(lessons_with_out_pipe)}')
                