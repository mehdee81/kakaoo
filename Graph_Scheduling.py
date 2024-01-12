import random

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
        # تعداد رنگ‌ها را مشخص می‌کنیم
        num_colors = len(self.adj_dict)

        # رنگ هر node را مشخص می‌کنیم
        node_colors = {node: None for node in self.adj_dict}

        # تابع کمکی برای بررسی امکان رنگ‌آمیزی یک node با یک رنگ خاص
        def is_valid_color(node, color):
            for neighbor in self.adj_dict[node]:
                if node_colors[neighbor] == color:
                    return False
            return True

        # تابع بازگشتی برای رنگ‌آمیزی گراف
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

        # شروع رنگ‌آمیزی از node اول
        color_node(next(iter(self.adj_dict)), num_colors)

        output_dict = {}
        for key, value in node_colors.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict

                

class InOrderSchedule:
    def __init__(self, lessons, vahed, days, times , exception_lessons = None):
        self.lessons = lessons
        self.days = days
        self.times = times
        self.schedule = {day: {time: [] for time in self.times} for day in self.days}
        self.vahed = vahed
        self.assigned = None
        self.exception_lessons = exception_lessons
        self.zoj_fard = None
      
    def assign_lesson(self, lesson, group_lessons, day, time):
        assign = False
        if len(self.schedule[day][time]) > 0:
            check_list = []
            assigned_lessons = self.schedule[day][time]
            for assigned_lesson in assigned_lessons:
                _append = False
                for course in group_lessons:
                    if course in assigned_lesson:
                        if ((assigned_lesson[-2:] == '_f' or assigned_lesson[-2:] == '_z') and (lesson[-2:] == '_f' or lesson[-2:] == '_z')):
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
            # print(day , time , lesson ,group_lessons , course ,"-->", assigned_lesson , assign )

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
        
        ex_lessons = []
        if self.exception_lessons != None:
            for key , value in self.exception_lessons.items():
                ex_lessons.append(key)
                self.schedule[value[0]][value[1]] = [key]
        
        for color_of_lesson , group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_vahed = self.vahed[lesson]
                for day in self.days:
                    for time in self.times:
                        as_lesson = True                        
                        for ex in ex_lessons:
                            if lesson == ex[:-2]:
                                as_lesson = False
                                break
                        if as_lesson:  
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
                if self.assigned == False:
                    print("could not find place for ",lesson , ": 3 vahedi")
                    
                        

        for color_of_lesson , group_lessons in self.lessons.items():
            for lesson in group_lessons:
                lesson_vahed = self.vahed[lesson]
                for day in self.days:
                    for time in self.times:
                        number = 0    
                                    
                        for ex in ex_lessons:
                            if lesson == ex or lesson == ex[:-2]:
                                number += 1
                                
                        if number < 2:
                            if lesson_vahed == 4:
                                    self.assign_lesson(lesson, group_lessons, day, time)
                            
                        if self.assigned == True:
                            break
                    if self.assigned == True:
                        break
                if self.assigned == False:
                    print("could not find place for ",lesson , ": 4 vahedi")
                
        for color_of_lesson , group_lessons in self.lessons.items():
            for lesson in group_lessons:
                if lesson not in ex_lessons:
                    for day in self.days:
                        for time in self.times:
                            self.assign_lesson(lesson, group_lessons, day, time)
                            if self.assigned == True:
                                break
                        if self.assigned == True:
                            break
                if self.assigned == False:
                    print("could not find place for ",lesson , ": 1 vahedi")
                        
    def print_schedule(self):
        for day, day_schedule in self.schedule.items():
            print(day)
            for time, lessons in day_schedule.items():
                lessons_with_out_pipe = []
                for lesson in lessons:
                    lessons_with_out_pipe.append(lesson.replace("|" , ""))
                print(f'    {time}: {", ".join(lessons_with_out_pipe)}')
                