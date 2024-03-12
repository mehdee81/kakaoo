import random
import time
import copy

class GPAscheduler:
    def __init__(
        self,
        all_courses,
        schedule,
        edges,
        unit,
        teachers,
        professors_limit_time,
        chromosomes,
    ):
        self.all_courses = all_courses
        self.edges = edges
        self.penalty = 0
        self.penalty_of_repeat_course = 27
        self.penalty_of_same_professor = 9
        self.penalty_of_limit_time = 3
        self.penalty_of_edge = 1
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]
        self.times = ["8:30", "10:30", "13:30", "15:30", "17:30"]
        self.main_schedule = copy.deepcopy(schedule)
        self.schedule = schedule
        self.best_schedule = None
        self.lowest_schedule_penalty = None
        self.assigned = None
        self.teachers = teachers
        self.professors_limit_time = professors_limit_time
        self.chromosomes = chromosomes
        self.unit = unit
        
        piped_units = {}
        for course, unit in self.unit.items():
            piped_units[f"|{course}|"] = unit
        self.unit = piped_units

        piped_teachers = {}
        for course, prof in self.teachers.items():
            piped_teachers[f"|{course}|"] = prof
        self.teachers = piped_teachers

    def assign_course(self, new_course, edges, day, time):
        assign = False
        teachers = self.teachers
            
        if len(self.schedule[day][time]) > 0:

            assigned_courses = self.schedule[day][time]
            assigned_courses_with_out_z_f = []
            for assigned_course in assigned_courses:
                if assigned_course[-2:] == "_f" or assigned_course[-2:] == "_z":
                    assigned_courses_with_out_z_f.append(assigned_course[:-2])
                else:
                    assigned_courses_with_out_z_f.append(assigned_course)
                    
            for i in range(len(assigned_courses_with_out_z_f)):
                if (assigned_courses_with_out_z_f[i],new_course) not in edges and (new_course,assigned_courses_with_out_z_f[i]) not in edges: # if they have not edge
                    if assigned_courses[i][-2:] == "_f" or assigned_courses[i][-2:] == "_z":
                        if new_course[-2:] == "_f" or new_course[-2:] == "_z":
                            if new_course[-2:] == assigned_courses[i][-2:]:
                                if teachers[new_course[:-2]] == teachers[assigned_courses[i][:-2]]:
                                    self.penalty += self.penalty_of_same_professor
                            
                            
                        elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                            if teachers[new_course] == teachers[assigned_courses[i][:-2]]:
                                self.penalty += self.penalty_of_same_professor
                            
                    
                    elif assigned_courses[i][-2:] != "_f" and assigned_courses[i][-2:] != "_z":
                        if new_course[-2:] != "_f" and new_course[-2:] != "_z":
                            if teachers[new_course] == teachers[assigned_courses[i]]:
                                self.penalty += self.penalty_of_same_professor
                            
                        elif new_course[-2:] == "_f" or new_course[-2:] == "_z":
                            if teachers[new_course[:-2]] == teachers[assigned_courses[i]]:
                                self.penalty += self.penalty_of_same_professor
                
                else: # if they have edge penalty += penalty_of_edge
                    if assigned_courses[i][-2:] == "_f" or assigned_courses[i][-2:] == "_z":
                        if new_course[-2:] == "_f" or new_course[-2:] == "_z":
                            if new_course[-2:] == assigned_courses[i][-2:]:
                                self.penalty += self.penalty_of_edge
                                if teachers[new_course[:-2]] == teachers[assigned_courses[i][:-2]]:
                                    self.penalty += self.penalty_of_same_professor
                            
                        elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                            self.penalty += self.penalty_of_edge
                            if teachers[new_course[:-2]] == teachers[assigned_courses[i][:-2]]:
                                self.penalty += self.penalty_of_same_professor
                            
                    
                    elif assigned_courses[i][-2:] != "_f" and assigned_courses[i][-2:] != "_z" :
                        if new_course[-2:] == "_f" or new_course[-2:] == "_z":
                            self.penalty += self.penalty_of_edge
                            if teachers[new_course[:-2]] == teachers[assigned_courses[i][:-2]]:
                                self.penalty += self.penalty_of_same_professor
                        
                        elif new_course[-2:] != "_f" and new_course[-2:] != "_z":
                            self.penalty += self.penalty_of_edge
                            if teachers[new_course[:-2]] == teachers[assigned_courses[i][:-2]]:
                                self.penalty += self.penalty_of_same_professor

            for assigned_course in self.schedule[day][time]:
                if new_course in assigned_course or assigned_course in new_course:
                    self.penalty += self.penalty_of_repeat_course
                
            self.schedule[day][time].append(new_course)    
        else:
            self.schedule[day][time].append(new_course)

    def assign_courses(self):
        teachers = self.teachers
        teachers_limit_state = self.professors_limit_time
      
        for course in self.all_courses:
            if course[-2:] == "_z" or course[-2:] == "_f": 
                teacher = teachers[course[:-2]]
            else:
                teacher = teachers[course]
                
            day = random.choice(self.days)
            time = random.choice(self.times)
            if teacher in teachers_limit_state: # if master has limit
                if [day, time] in teachers_limit_state[teacher]: # if master can be be in university in this section
                    
                    self.assign_course(
                        course,
                        self.edges,
                        day,
                        time,
                    )
                else:
                    self.assign_course(
                        course,
                        self.edges,
                        day,
                        time,
                    )
                    self.penalty += self.penalty_of_limit_time
            else:
                self.assign_course(
                    course,
                    self.edges,
                    day,
                    time,
                )

    def make_solution(self):
        all_results = []
        for i in range(1, self.chromosomes + 1):
            
            self.assign_courses()
            all_results.append(
                (
                    self.schedule,
                    self.penalty,
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
            
            self.schedule = copy.deepcopy(self.main_schedule)
            
            self.penalty = 0
        return all_results

    def fitness(self):
        all_results = self.make_solution()
        sorted_results = sorted(all_results, key=lambda x: x[1])
        self.best_schedule = sorted_results[0][0]
        self.lowest_schedule_penalty = sorted_results[0][1]

        for sorted_result in sorted_results[:10]:
            print("Penalty: ", sorted_result[1])

    def start(self):

        print(
            "Scheduling Started With",
            self.chromosomes,
            "chromosomes",
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


