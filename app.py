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
        print("Connected to the all_Courses_listbase!")
        return db, cu

    except sqlite3.Error as e:
        print("An error occurred while connecting to the all_Courses_listbase:", e)
db , cu = sql_db()
# --------------------------------------------------- Main ---------------------------------------------------
main_window = Tk()
main_window.title("Graph scheduling")
main_window.geometry("1200x600")
main_window.minsize(1200, 600)
main_window.maxsize(1200, 600)
menubar = Menu(main_window)
listmenu = Menu(menubar , tearoff=0)
menubar.add_cascade(label="Pages",menu=listmenu)
listmenu.add_command(label="Professors")
listmenu.add_command(label="Courses")
listmenu.add_command(label="Prerequisites")
listmenu.add_command(label="Exit" , command=main_window.quit)
menubar.add_command(label="About")
main_window.config(menu = menubar)


# Create Main Frame
main_frame = Frame(main_window)
main_frame.pack(fill=BOTH , expand=1)
# Create A canvas 
main_canvas = Canvas(main_frame)
main_canvas.pack(side=LEFT , fill=BOTH , expand=True)
# Add scrollbar to the canvas
main_scrollbar = Scrollbar(main_frame, orient=VERTICAL , command=main_canvas.yview)
main_scrollbar.pack(side=RIGHT , fill=Y)
# configure the canvas
main_canvas.config(yscrollcommand=main_scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion = main_canvas.bbox("all")))
# Create another frame inside  the canvas
second_main_frame = Frame(main_canvas)
# Add that new frame to a window the canvas
main_canvas.create_window((0,0), window=second_main_frame, anchor="nw")

all_Courses_list = cu.execute("SELECT course , vahed FROM courses")
all_Courses_list = all_Courses_list.fetchall()

all_Courses_list_frame = Frame(second_main_frame, highlightthickness=1, highlightbackground="black")
all_Courses_list_frame.grid(padx=10, pady=10)
all_Courses_list_frame.config(width=600, height=300)

if len(all_Courses_list) == 0:
    there_is_not_course_label = Label(all_Courses_list_frame, text="There is not any courses.", font=("tohama", 12), fg="red")
    there_is_not_course_label.grid()
else:
    checkbox_vars = []
    for idx, (course, vahed) in enumerate(all_Courses_list):
        var = BooleanVar(value=False)
        checkbox_vars.append(var)

        check_button = Checkbutton(all_Courses_list_frame, text= f"{course}: {vahed}", variable=var)
        check_button.grid(row=idx, column=0, sticky="w")

        
db.close()
main_window.mainloop()