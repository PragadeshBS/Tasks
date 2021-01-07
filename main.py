import os
from tkinter import *
import datetime
from tkcalendar import Calendar
from tkscrolledframe import ScrolledFrame

# program variables
window = Tk()
window.title("Tasks")
window.geometry("700x600")
window.configure(background="#33ffbd")
window.resizable(False, False)
data_files_parent_path = "C:/Tweaks/"
main_data_file_name = "data.txt"
tasks_data_file_name = "tasks.txt"
main_data_file = os.path.join(data_files_parent_path, main_data_file_name)
tasks_data_file = os.path.join(data_files_parent_path, tasks_data_file_name)
update_loop = True
time_greet_data = "Good morning"
current_time = datetime.datetime.now()
tasks_to_display = []
task_info_text = ""
pending_task_label = Label(window)
auto_sort = BooleanVar()
auto_sort.set(True)
font_style = "century gothic"
about_top = None

# data variables
user_name = "User"
no_tasks_pending = master_task_count = 0


class Task:

    def __init__(self, title, due_date, notes, t_id):
        self.title = title
        self.due_date = due_date.strftime('%a, %d %b %Y')
        self.notes = notes
        self.id = t_id
        self.is_done = IntVar()

    def form_string(self):
        # format of string - $t_id^^t_is_done^^t_title^^t_due_date^^t_notes
        # replace \n characters with ^ in notes

        formatted_notes = ""
        for i in self.notes:
            if i == "\n":
                formatted_notes += "^"
                continue
            formatted_notes += i

        final_string = f"${self.id}^^{self.is_done.get()}^^{self.title}^^{self.due_date}^^{formatted_notes}"
        return final_string


def auto_create_data_files_path():
    # return cases: 1 - created data file parent dir; -1 - OSError encountered
    global data_files_parent_path
    init_screen()

    try:
        os.mkdir(data_files_parent_path)
        return 1

    except OSError:
        return -1


def write_first_details():
    global user_name, master_task_count

    to_write = f"$user_name: {user_name}\n$master_task_count: {master_task_count}"

    with open(main_data_file, "w") as open_file:
        open_file.write(to_write)

    home_screen()


def first_launch_handler():
    global user_name
    init_screen()

    def place_submit_button():
        nonlocal submit_button
        submit_button.grid(row=4, column=4, columnspan=2, pady=20)

    def validate_name():
        global user_name
        nonlocal name_entry, submit_button
        to_check = name_entry.get()
        to_check = to_check.strip()
        if (len(to_check)) < 3 or (len(to_check) > 20):
            submit_button.grid_forget()
            short_m = Label(window, bg="#33ffbd", font=(font_style, '14', 'bold'),
                            text="Enter a name that is 3-20 characters in length", fg="#ff0000")
            short_m.grid(row=4, column=2, columnspan=8, pady=20)
            submit_button.after(2000, place_submit_button)
            short_m.after(2000, short_m.grid_remove)
            return
        user_name = to_check
        write_first_details()

    welcome_label = Label(window, text="Welcome to tasks!",
                          font=(font_style, 38, 'bold'), fg="#464646", bg="#33ffbd")
    welcome_label_2 = Label(window, pady=30, text="Task management, made easy",
                            font=(font_style, 18), fg="#d33200", bg="#33ffbd")

    name_label = Label(window, text="Enter your name to start ", font=('century gothic', 14), bg="#33ffbd")
    name_entry = Entry(window, font=('calibri', 12))

    submit_button = Button(window, cursor="hand2", text="Let's begin", activeforeground="#464646",
                           fg="#464646", font=(font_style, 14, 'bold'), activebackground="#ddfff4",
                           bg="#ddfff4", command=validate_name)

    welcome_label.grid(columnspan=8, row=0, ipadx=65, pady=(50, 0))
    welcome_label_2.grid(columnspan=8, row=1, ipadx=5)
    name_label.grid(row=2, column=4)
    name_entry.grid(row=2, column=5)
    submit_button.grid(row=4, column=4, columnspan=2, pady=20)


def about_screen():
    global about_top

    def about_done():
        global about_top
        about_top.destroy()

    if (not about_top) or (about_top.winfo_exists() == 0):
        about_top = Toplevel(window)
        about_top.geometry("300x200")
        about_top.resizable(False, False)
        Label(about_top, text="Tasks 1.0", font=('arial', 14)).grid(pady=20)
        Label(about_top, text="Build time: Jan 6 19:48", justify=LEFT).grid(sticky="nw")
        Button(about_top, text="OK", command=about_done).grid(padx=140, pady=20)


def add_task_screen():
    due_date = datetime.datetime.today().date()
    top = None
    window.title("Tasks - Add Task")

    def select_due_date():
        nonlocal due_date, top

        def cal_done(catch_null):
            nonlocal select_date_button, due_date
            due_date = cal.selection_get()
            select_date_button["text"] = due_date.strftime('%a, %d %b %Y')
            top.destroy()

        if not top:
            top = Toplevel(window)
            cal = Calendar(top, font="Arial 14", showweeknumbers=False, selectmode='day',
                           cursor="hand2", mindate=datetime.date.today())
            cal.pack(fill="both", expand=True)
            cal.bind("<<CalendarSelected>>", cal_done)

        elif top.winfo_exists() == 0:
            top = Toplevel(window)
            cal = Calendar(top, font="Arial 14", showweeknumbers=False, selectmode='day',
                           cursor="hand2", mindate=datetime.date.today())
            cal.pack(fill="both", expand=True)
            cal.bind("<<CalendarSelected>>", cal_done)

    def short_message(text):
        message = Label(window, text=text, bg="#eefff6", fg="#ff0000", font=('calibri', 16), wraplength=250)
        message.grid(row=4, column=1)
        message.after(2000, message.grid_remove)

    def validate_task():
        nonlocal due_date, task_title_entry, task_notes_entry, submit_button

        task_title = task_title_entry.get()
        task_title = task_title.strip()
        task_notes = task_notes_entry.get("1.0", "end-1c")
        task_notes = task_notes.strip()

        if (len(task_title) < 3) or (len(task_title) > 50):
            short_message("Set a task title that is 3-50 characters long")
            return

        if len(task_notes) > 250:
            short_message("Task notes cannot contain more than 250 characters")
            return

        if "^" in task_notes:
            short_message("Task notes cannot contain the character ^")
            return

        if not task_notes:
            task_notes = "No notes were set for this task"

        while task_notes.endswith("\n"):
            task_notes = task_notes[:len(task_notes)-1]

        create_task(task_title, due_date, task_notes)

    init_screen()

    Button(window, command=home_screen, activebackground="#d9e5ff", activeforeground="#565656",
           text="◄", font=("sans serif", 16, 'bold'), bg="#d9e5ff", fg="#565656", relief="flat",
           cursor="hand2").grid(sticky="w")

    Label(window, text="Set a title for your task: ", padx=20, bg="#eefff6", fg="#31442b",
          font=(font_style, 16)).grid(pady=(25, 25))
    task_title_entry = Entry(window, width=35, font=('calibri', 12), bg="#fff9e8")
    task_title_entry.grid(row=1, column=1, ipady=2)

    Label(window, text="Select a due date", padx=20, bg="#eefff6", fg="#31442b",
          font=(font_style, 16)).grid(pady=(50, 50))
    select_date_button = Button(window, relief="flat", text=due_date.strftime('%a, %d %b %Y'),
                                font=(font_style, 16), bg="#fff9e8", fg="#545454", activeforeground="#545454",
                                activebackground="#fff9e8", cursor="hand2", command=select_due_date)
    select_date_button.grid(row=2, column=1, pady=(50, 50))

    Label(window, text="Add notes to your task: ", padx=20, bg="#eefff6", fg="#31442b", font=(font_style, 16)).grid()
    # scroll = Scrollbar(window, orient=VERTICAL) scroll bar not needed currently
    # scroll.grid(row=3, column=2, ipady=35, rowspan=5)
    task_notes_entry = Text(window, wrap=WORD, height=10, font=('calibri', 12), width=35,
                            bg="#fff9e8")  # yscrollcommand=scroll.set
    task_notes_entry.grid(row=3, column=1)
    # scroll.config(command=task_notes_entry.yview)

    submit_button = Button(window, relief="flat", text="Add task", command=validate_task,
                           font=(font_style, 16), bg="#ffd9d9", fg="#292929", activeforeground="#292929",
                           activebackground="#ffd9d9", cursor="hand2")
    submit_button.grid(row=4, pady=50)


def write_task(task_string):
    global tasks_data_file
    with open(tasks_data_file, "r") as file:
        content = file.read()
    to_write = "\n"+task_string if content else task_string
    with open(tasks_data_file, "a") as file:
        file.write(to_write)


def remove_task_from_file(task_ids):
    global tasks_data_file
    with open(tasks_data_file, "r") as file:
        contents = file.readlines()
    with open(tasks_data_file, "w") as file:
        file.seek(0)
        for i in range(len(contents)):
            bits = contents[i].split("^^")
            if int(bits[0][1:]) in task_ids:
                continue
            file.write(contents[i])
        file.truncate()


def create_task(t_title, t_due_date_, t_notes):
    global master_task_count, no_tasks_pending, tasks_to_display
    master_task_count += 1
    no_tasks_pending += 1
    update_main_data()
    new_task = Task(t_title, t_due_date_, t_notes, master_task_count)
    formatted_task = new_task.form_string()
    write_task(formatted_task)
    tasks_to_display.append(new_task)
    home_screen()

    def short_message(text):
        message = Label(window, text=text, bg="#eefff6", fg="#007cff", font=('calibri', 16, 'bold'), wraplength=250)
        message.grid(row=1, column=1, columnspan=6)
        message.after(2000, message.grid_remove)

    short_message("Added task to list")


def update_main_data():
    global main_data_file, master_task_count, user_name
    to_write = f"$user_name: {user_name}\n$master_task_count: {master_task_count}"
    with open(main_data_file, "w") as file:
        file.write(to_write)


def reset_screen():
    window.title("Tasks - Reset Data")
    init_screen()
    Button(window, command=home_screen, activebackground="#ff0000", activeforeground="#ffffff", text="◄ Back",
           font=("sans serif", 16, 'bold'), bg="#ff0000", fg="#ffffff", relief="flat", cursor="hand2").grid(sticky="w")
    window.config(background="#ff0000")
    Label(window, bg="#ff0000", font=("calibri", 75), text="!", fg="white").grid(row=0)
    reset_label_text = "Data reset will permanently delete all details " \
                       "associated with the program. Be sure before you proceed."
    Label(window, font=('Arial', 14), text=reset_label_text, fg="white", wraplength=550,
          bg="#ff0000").grid(pady=(0, 100))
    Button(window, text="Reset data", cursor="hand2", font=(font_style, 12),
           activeforeground="#ffffff", activebackground="#ff0000", bg="#ff0000", fg="#ffffff",
           relief="flat", command=reset_data).grid()


def menu(action):
    # action set to 1 to makes menu visible, anything else makes it invisible/removes the menu
    if action == 1:
        menu_bar = Menu(window)
        file = Menu(menu_bar, tearoff=0)
        program_help = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file)
        menu_bar.add_cascade(label="Help", menu=program_help)
        file.add_command(label="Reset", command=reset_screen)
        file.add_command(label="Exit", command=window.destroy)
        program_help.add_command(label="About", command=about_screen)
        window.config(menu=menu_bar)
        return

    remove_menu = Menu(window)
    window.config(menu=remove_menu)


def time_greet():
    global time_greet_data, current_time

    if current_time.hour < 12:
        time_greet_data = "Good morning"
    elif current_time.hour < 16:
        time_greet_data = "Good afternoon"
    else:
        time_greet_data = "Good evening"


def clear_widgets():
    widgets = window.winfo_children()
    for widget in widgets:
        widget.grid_remove()


def update_index():

    def fast_update():

        global update_loop

        if update_loop:
            # to do every 5 second
            pass

        dummy1 = Label(window)
        dummy1.after(5000, fast_update)

    def slow_update():

        global update_loop

        if update_loop:
            # to do every minute
            time_greet()

        dummy2 = Label(window)
        dummy2.after(60000, slow_update)

    fast_update()
    slow_update()


def init_screen(back_button=False):
    clear_widgets()
    if back_button:
        Button(window, text="<---", command=home_screen).grid()


def popup(message, timeout=2000, font_color="Red"):
    popup_label = Label(window, text=message, wraplength=200, padx=20, fg=font_color, font=('arial', 11))
    popup_label.grid()
    popup_label.after(timeout, popup_label.grid_remove)


def reset_data():
    # reset all data files associated with the program
    with open(main_data_file, "w") as open_file:
        open_file.write("")
    with open(tasks_data_file, "w") as open_file:
        open_file.write("")
    init_screen()
    menu(0)
    window.config(background="#eefff6")
    Label(window, bg="#eefff6", fg="#31442b", wraplength=500, font=(font_style, 16),
          text="Program reset was successful, Restart program to see changes").grid(pady=(100, 10), padx=40)
    Button(window, text="Exit", font=(font_style, 16), activeforeground="#31442b", activebackground="#eefff6",
           command=window.destroy, fg="#ffffff", bg="#29ac69").grid()


def error(code, sub_code):
    # code 0 - critical error, stops the program from execution
    # code 1 - file corrupt error, notify user, reset data files and relaunch program
    if code == 0:
        init_screen()
        Label(window, text="Critical Error").grid()
        error_label_text = f"Error Code: {sub_code}\nWe've run into a critical error, something went very wrong :(" \
                           f"\nThis program will kill itself after 10 seconds"
        error_label = Label(window, text=error_label_text)
        error_label.grid()
        error_label.after(10000, window.destroy)


def format_text(length, text):
    word_arr = list(text)
    while len(word_arr) < length:
        word_arr.append(" ")
        word_arr.insert(0, " ")
    res = ""
    for letter in word_arr:
        res += letter
    return res


def update_task_status():
    global tasks_to_display, pending_task_label
    selections = []
    t_status = IntVar()

    for task in tasks_to_display:
        selections.append(task.is_done.get())

    for i in range(len(selections)):
        if selections[i] == 1:
            t_status.set(1)
        else:
            t_status.set(0)
        tasks_to_display[i].is_selected = t_status

    with open(tasks_data_file, "w") as file:
        file.write("")

    for i in tasks_to_display:
        str_task = i.form_string()
        write_task(str_task)

    home_screen()


def sort_tasks():
    global tasks_to_display, auto_sort

    if not auto_sort.get():
        return

    def calc_days_left(task):
        today_date = datetime.datetime.today()
        task_due = datetime.datetime.strptime(task.due_date, "%a, %d %b %Y")
        return abs((today_date - task_due).days)

    tasks_to_display.sort(key=calc_days_left)

    i = 0
    while i < len(tasks_to_display):
        count = 0
        while count < len(tasks_to_display)-i:
            if tasks_to_display[i].is_done.get() == 1:
                tasks_to_display.append(tasks_to_display.pop(i))
                count += 1
                continue
            break
        i += 1


def toggle_sort():
    global auto_sort
    init_screen(True)
    if auto_sort.get():
        popup("Auto")
    else:
        popup("Manual")


def list_tasks():
    global no_tasks_pending, tasks_to_display

    if not no_tasks_pending:
        return

    sort_tasks()

    task_table_start_row = 4
    task_no = 1
    task_table_start_column = 0
    current_row = task_table_start_row + 1
    current_column = task_table_start_column
    task_title = format_text(20, "Task")
    task_due_date = format_text(11, "Due")
    task_notes = format_text(32, "Notes")

    main_frame = Frame(window, width=690, height=320)
    main_frame.grid(columnspan=6)
    sf = ScrolledFrame(main_frame, width=680, height=310)
    sf.grid()
    sf.bind_arrow_keys(main_frame)
    sf.bind_scroll_wheel(main_frame)
    frame = sf.display_widget(Frame)
    Label(frame, text="Mark as done", fg="#317250", font=(font_style, 12)).grid(padx=(0, 5), row=task_table_start_row,
                                                                                column=task_table_start_column)
    Label(frame, text="No.", fg="#317250", font=(font_style, 12)).grid(row=task_table_start_row,
                                                                       column=task_table_start_column+1, padx=(5, 10))
    Label(frame, text=task_title, fg="#317250", font=(font_style, 12)).grid(row=task_table_start_row,
                                                                            column=task_table_start_column+2, padx=20)
    Label(frame, text=task_due_date, fg="#317250", font=(font_style, 12)).grid(row=task_table_start_row,
                                                                               column=task_table_start_column+3,
                                                                               padx=(20, 20))
    Label(frame, text=task_notes, fg="#317250", font=(font_style, 12)).grid(row=task_table_start_row,
                                                                            column=task_table_start_column+4,
                                                                            padx=(30, 0))

    for task in tasks_to_display:
        check_button = Checkbutton(frame, cursor="hand2", variable=task.is_done, command=update_task_status)
        if task.is_done.get() == 1:
            check_button.select()
        check_button.grid(row=current_row, column=task_table_start_column)
        Label(frame, text=task_no, font=('calibri', 11)).grid(row=current_row, column=current_column+1)
        Label(frame, text=task.title, wraplength=150, font=('calibri', 11)).grid(row=current_row,
                                                                                 column=current_column+2, padx=(0, 20))
        Label(frame, text=task.due_date, font=('calibri', 11)).grid(row=current_row, column=current_column+3,
                                                                    padx=(0, 20))
        notes_label = Label(frame, text=task.notes, wraplength=200, justify=CENTER, font=('calibri', 11))
        notes_label.grid(row=current_row, column=current_column+4, padx=(10, 0), pady=10)
        current_row += 1
        task_no += 1


def remove_tasks():
    global tasks_to_display, no_tasks_pending
    selections = []
    removed_task_ids = []

    for task in tasks_to_display:
        selections.append(task.is_done.get())

    for i in range(len(selections)):
        if selections[i] == 1:
            removed_task_ids.append(tasks_to_display[i].id)
            tasks_to_display[i] = -1

    tasks_to_display = [i for i in tasks_to_display if not i == -1]
    no_tasks_pending = len(tasks_to_display)
    remove_task_from_file(removed_task_ids)
    home_screen()

    def short_message(text):
        message = Label(window, text=text, bg="#eefff6", fg="#ff0000", font=('calibri', 16), wraplength=250)
        message.grid(row=1, column=1, columnspan=6)
        message.after(2000, message.grid_remove)

    if len(removed_task_ids) > 1:
        short_message("Removed selected tasks")
    elif len(removed_task_ids) == 1:
        short_message("Removed selected task")
    else:
        short_message("Mark a task as done to remove")


def pending_task_info():
    global tasks_to_display, task_info_text, pending_task_label
    pending_count = 0
    for i in tasks_to_display:
        if i.is_done.get() == 0:
            pending_count += 1
    if pending_count == 0:
        task_info_text = "You currently have no tasks. Enjoy a cup of coffee"
    elif pending_count == 1:
        task_info_text = "You currently have 1 task remaining"
    else:
        task_info_text = f"You currently have {pending_count} tasks remaining\nHere are" \
                         f" your tasks sorted based on the due dates"


def home_screen():
    # main screen of the program, displays greet message, tasks pending info if any
    global user_name, time_greet_data, tasks_to_display, task_info_text
    global pending_task_label
    window.config(background="#eefff6")
    window.title("Tasks")

    init_screen()
    menu(1)
    header_label = Label(window, text="Tasks", font=(font_style, 35), bg="#eefff6", fg="#716747")
    greet_label_text = f"{time_greet_data} {user_name}!"
    greet_label = Label(window, font=(font_style, 16), text=greet_label_text, bg="#eefff6", fg="#31442b")
    add_task_button = Button(window, command=add_task_screen, relief="flat", cursor="hand2", bg="#d9e5ff",
                             fg="#292929", activeforeground="#292929", activebackground="#d9e5ff",
                             text="Create a task", font=('calibri', 14))
    remove_task_button = Button(window, text="Remove completed tasks",
                                command=remove_tasks, relief="flat", cursor="hand2",
                                bg="#ffd9d9", fg="#292929", activeforeground="#292929",
                                activebackground="#ffd9d9", font=('calibri', 14))
    pending_task_info()
    pending_task_label = Label(window, text=task_info_text, font=(font_style, 11), bg="#eefff6")

    header_label.grid(padx=230, columnspan=8, pady=(0, 3))
    greet_label.grid(sticky="w", pady=(20, 20))
    pending_task_label.grid(columnspan=8)

    list_tasks()

    if tasks_to_display:
        add_task_button.grid(pady=20, columnspan=2)
        remove_task_button.grid(row=4, columnspan=4, column=1)
    else:
        add_task_button.grid(pady=20, columnspan=8)


def extract_tasks():
    # throw critical error if file corrupt - to be modified to a format error
    # extract tasks and add task object to tasks_to_display list
    global tasks_data_file, no_tasks_pending, tasks_to_display

    with open(tasks_data_file, "r") as file:
        content = file.readlines()

    if not len(content) == no_tasks_pending:
        error(0, "FILE_CORRUPT")
        return

    for i in content:
        task_sliced = i.split("^^")
        new_task_id = int(task_sliced[0][1:])
        new_task_is_done = int(task_sliced[1])
        new_task_title = task_sliced[2]
        new_task_dd = task_sliced[3]
        task_notes_in_file = task_sliced[4][:len(task_sliced[4])]
        if task_notes_in_file.endswith("\n"):
            task_notes_in_file = task_notes_in_file[:len(task_notes_in_file)-1]
        new_task_notes = ""
        for j in task_notes_in_file:
            if j == "^":
                new_task_notes += "\n"
                continue
            new_task_notes += j
        new_task_dd = datetime.datetime.strptime(new_task_dd, "%a, %d %b %Y")
        new_task = Task(new_task_title, new_task_dd, new_task_notes, new_task_id)

        task_status = IntVar()
        if new_task_is_done == 1:
            task_status.set(1)
        else:
            task_status.set(0)
        new_task.is_done = task_status

        tasks_to_display.append(new_task)


def extract_data():
    # return cases: 0 - File empty; 1 - Extracted data successfully and redirected to extract_tasks
    global main_data_file, user_name, master_task_count, tasks_data_file, no_tasks_pending

    with open(main_data_file, "r") as open_file:
        user_data = open_file.readlines()

    if not user_data:
        return 0

    if user_data:

        with open(tasks_data_file, "r") as open_file:
            task_content = open_file.readlines()

        user_name = user_data[0][12:len(user_data[0])-1]
        master_task_count = int(user_data[1][20:])

        if not task_content:
            no_tasks_pending = 0
        else:
            no_tasks_pending = len(task_content)
            extract_tasks()

    return 1


def initiate_data_files():
    # return cases: 1 - Created a new file; 0 - File already exists; -1 - Path does not exist
    global data_files_parent_path, main_data_file, tasks_data_file

    if os.path.isdir(data_files_parent_path):

        try:
            with open(main_data_file, "r"):
                pass
            with open(tasks_data_file, "r"):
                pass
            return 0

        except FileNotFoundError:
            with open(main_data_file, "a"):
                pass
            with open(tasks_data_file, "a"):
                pass
            return 1

    return -1


def main():
    # redirects to initiate_data_files to check and create data files if parent path exists
    # redirects to  auto_create_data_files_path to create parent path if possible
    # throws critical error if creation of parent path was not possible
    # redirects to first_launch_handler if no data was extracted after redirecting to extract_data
    # redirects to home_screen
    global data_files_parent_path

    if initiate_data_files() == -1:

        if auto_create_data_files_path() != -1:
            initiate_data_files()

        else:
            error(0, "FILE_INIT_FAILED")
            return

    if extract_data() == 0:
        first_launch_handler()
        return

    home_screen()


if __name__ == '__main__':  # starter function
    update_index()
    main()

window.mainloop()
