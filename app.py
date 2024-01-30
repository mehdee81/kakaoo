from tkinter import *
import sqlite3
from tkinter import ttk
from Graph_Scheduling import Graph, InOrderSchedule
import itertools


# --------------------------------------------------- Connect to DB ------------------------------------------
def sql_db():
    try:
        # Connect to the SQLite all_Courses_listbase
        db = sqlite3.connect("dbsql.sqlite3")
        cu = db.cursor()
        print("Connected to datebase!")
        return db, cu

    except sqlite3.Error as e:
        print("An error occurred while connecting to the datebase:", e)


# --------------------------------------------------- Main ---------------------------------------------------
main_window = Tk()
main_window.title("Graph scheduling")
main_window.geometry("1200x600")
main_window.minsize(1200, 600)
main_window.maxsize(1200, 600)
menubar = Menu(main_window)
listmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Pages", menu=listmenu)
listmenu.add_command(label="Professors")
listmenu.add_command(label="Courses")
listmenu.add_command(label="Prerequisites")
listmenu.add_command(label="Exit", command=main_window.quit)
menubar.add_command(label="About")
main_window.config(menu=menubar)
# --------------------------------------------------- Courses Frame ------------------------------------------
# Create Main Frame
main_frame = Frame(main_window)
main_frame.pack(fill=BOTH, expand=1)
# Create A canvas
main_canvas = Canvas(main_frame)
main_canvas.pack(side=LEFT, fill=BOTH, expand=True)
# Add scrollbar to the canvas
main_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
main_scrollbar.pack(side=RIGHT, fill=Y)
# configure the canvas
main_canvas.config(yscrollcommand=main_scrollbar.set)
main_canvas.bind(
    "<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)
# Create another frame inside  the canvas
second_main_frame = Frame(main_canvas)
# Add that new frame to a window the canvas
main_canvas.create_window((0, 0), window=second_main_frame, anchor="nw")

db, cu = sql_db()
all_Courses_list = cu.execute("SELECT course , vahed FROM courses")
all_Courses_list = all_Courses_list.fetchall()
db.close()

all_Courses_list_frame = Frame(
    second_main_frame, highlightthickness=1, highlightbackground="black"
)
all_Courses_list_frame.grid(padx=5, pady=10, column=0, row=0, sticky="n")
all_Courses_list_frame.config()
select_professors_frame = Frame(
    second_main_frame, highlightthickness=1, highlightbackground="black"
)
select_professors_frame.grid(padx=5, pady=10, column=1, row=0, sticky="n")
select_professors_frame.config()

selected_courses = []
professors_options = ["select"]
selected_professor = StringVar()
drop_down_professors = OptionMenu(select_professors_frame, selected_professor , *professors_options)
drop_down_professors.grid()

courses_options = ["select"]
selected_course_to_link_professor = StringVar()
drop_down_courses = OptionMenu(select_professors_frame, selected_course_to_link_professor, *courses_options)
drop_down_courses.grid()

linked_professors = {}
def link_course_to_professor(selected_course_to_link_professor, selected_professor):
    linked_professors[f"|{selected_course_to_link_professor}|"] = f"|{selected_professor}|"
  
linke_btn = Button(select_professors_frame , text="link" , command=link_course_to_professor)
linke_btn.grid()

def select_courses():
    global drop_down_professors
    global drop_down_courses
    global linke_btn
    selected_courses.clear()

    linked_professors.clear()
    for idx, (course, _) in enumerate(all_Courses_list):
        if checkbox_vars[idx].get():
            selected_courses.append(course)

    if len(selected_courses) > 0:
        Label(select_professors_frame , text="Select the professor and the course to link them together." , font=("tohama" , 15)).grid(column=0 , row=0)
        db, cu = sql_db()
        all_professors = cu.execute("SELECT name FROM Professors")
        all_professors = all_professors.fetchall()
        db.close()

        professors_options = []
        for professor in all_professors:
            professors_options.append(professor[0])
        
        Label(select_professors_frame , text="Professor:" , font=("tohama" , 10)).grid(column=0 , row=1)
        drop_down_professors.grid_forget()
        selected_professor = StringVar()
        selected_professor.set(all_professors[0][0])
        drop_down_professors = OptionMenu(select_professors_frame, selected_professor, *professors_options)
        drop_down_professors.grid(column=1 , row=1)
        
        
        courses_options = []
        for course in selected_courses:
            courses_options.append(course)
        Label(select_professors_frame , text="Course:" , font=("tohama" , 10)).grid(column=0 , row=2)
        drop_down_courses.grid_forget()
        selected_course_to_link_professor = StringVar()
        selected_course_to_link_professor.set(courses_options[0])
        drop_down_courses = OptionMenu(select_professors_frame, selected_course_to_link_professor, *courses_options)
        drop_down_courses.grid(column=1 , row=2)

        linke_btn.grid_forget()
        linke_btn = Button(select_professors_frame, text="link", command=lambda: link_course_to_professor(selected_course_to_link_professor.get(), selected_professor.get()))
        linke_btn.grid()

if len(all_Courses_list) == 0:
    Label(
        all_Courses_list_frame,
        text="There is not any courses.",
        font=("tohama", 12),
        fg="red",
    ).grid()
    Label(
        all_Courses_list_frame,
        text="Go to the pages, then courses and add some course.",
        font=("tohama", 12),
        fg="Green",
    ).grid()

else:
    checkbox_vars = []
    for idx, (course, vahed) in enumerate(all_Courses_list):
        var = BooleanVar(value=False)
        checkbox_vars.append(var)

        check_button = Checkbutton(
            all_Courses_list_frame, text=f"{course}: {vahed}", variable=var
        )
        check_button.grid(row=idx, column=0, sticky="w")

    Button(all_Courses_list_frame, text="Set", command=select_courses).grid()


main_window.mainloop()
