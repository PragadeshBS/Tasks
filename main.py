from os import mkdir, getcwd, path
from tkinter import *
import tkinter.ttk
from datetime import datetime, date
from tkcalendar import Calendar
from tkscrolledframe import ScrolledFrame
import urllib.request
import urllib.error
import webbrowser

# program variables
latest_program_version = 2.0
user_program_version = 2.0
to_update = False
window = Tk()
window.title("Tasks")
window.geometry("1000x600")
window.configure(background="#ffffff")
window.resizable(False, False)
data_files_parent_path = getcwd()
icon_file_name = "logo.png"
icon_file = path.join(data_files_parent_path, icon_file_name)
logo = PhotoImage(file=icon_file)
window.iconphoto(True, logo)
main_data_file_name = "data.txt"
tasks_data_file_name = "tasks.txt"
main_data_file = path.join(data_files_parent_path, main_data_file_name)
tasks_data_file = path.join(data_files_parent_path, tasks_data_file_name)
update_loop = True
time_greet_data = "Good morning"
current_time = datetime.now()
tasks_to_display = []
task_info_text = ""
pending_task_label = Label(window)
font_style = "century gothic"
about_top = top = None
sort_method = IntVar()  # 0 - auto; 1 - manual
user_name_var = StringVar()
move_done_to_end = IntVar()
move_done_to_end.set(1)
task_highlighting = IntVar()
task_highlighting.set(1)
check_update_at_startup = IntVar()
check_update_at_startup.set(1)

# images/icons
up_arrow_image = PhotoImage(file="uparrow.png")
down_arrow_image = PhotoImage(file="downarrow.png")
top_arrow_image = PhotoImage(file="toparrow.png")
bottom_arrow_image = PhotoImage(file="bottomarrow.png")
back_button_image = PhotoImage(file="backarrow.png")
done_button_image = PhotoImage(file="done.png")
start_button_image = PhotoImage(file="start.png")
add_new_image = PhotoImage(file="addnew.png")
delete_image = PhotoImage(file="delete.png")
create_image = PhotoImage(file="create.png")
edit_done_image = PhotoImage(file="editdone.png")
reset_image = PhotoImage(file="reset.png")
exit_image = PhotoImage(file="exit.png")
small_done_image = PhotoImage(file="smalldone.png")
refresh_image = PhotoImage(file="refresh.png")
refresh_2_image = PhotoImage(file="refresh2.png")

# data variables
user_name = ""
no_tasks_pending = master_task_count = 0


user_name_var.set(user_name)


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

    def get_id(self):
        return self.id


def appearance_settings_screen():
    init_screen()

    back_button = Button(window, command=home_screen, activebackground="#ffffff", activeforeground="#565656",
                         image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff",
                         fg="#d33200", relief="flat", cursor="hand2")

    back_button.grid(sticky="nw")

    header_label = Label(window, text="Appearance Settings", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=300, pady=(0, 20))

    task_highlighting_cb = Checkbutton(window, text="Highlight tasks that are due in the next 3 days",
                                       variable=task_highlighting,
                                       font=(font_style, 16), command=update_main_data,
                                       bg="#ffffff", relief="flat", highlightthickness=0)
    task_highlighting_cb.grid(columnspan=10, pady=(30, 0))


def sort_settings_screen(first_run=False):
    global sort_method
    init_screen()

    back_button = Button(window, command=home_screen, activebackground="#ffffff", activeforeground="#565656",
                         image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff",
                         fg="#31442b", relief="flat", cursor="hand2")

    if first_run:
        back_button.config(command=first_launch_handler)
    back_button.grid(sticky="nw")

    header_label = Label(window, text="Task Sort Settings", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))

    if first_run:
        header_label.config(text="One last step to make your experience better...", font=(font_style, 28))
        header_label.grid(row=0, columnspan=5, padx=(60, 0), pady=(0, 20), sticky="n")

    else:
        header_label.grid(row=0, columnspan=10, padx=(200, 0), pady=(0, 20))

    Label(window, text="Choose how we should sort your tasks before listing them for you",
          padx=20, bg="#ffffff", fg="#565656",
          font=(font_style, 16)).grid(pady=(25, 25), columnspan=10, padx=(150, 0))

    sort_methods = ["Auto sort tasks based on due dates assigned", "Manually sort tasks"]
    if not first_run:
        sort_methods[1] = "Manually sort tasks"

    for i in range(len(sort_methods)):
        rad_btn = Radiobutton(window, text=sort_methods[i], variable=sort_method,
                              value=i, bg="#ffffff", activebackground="#ffffff",
                              command=update_main_data, font=(font_style, 11))
        rad_btn.grid(columnspan=8, column=2, pady=(15, 15), sticky="w")

    if first_run:
        tip_label = Label(window, text="Tip: You can change this anytime from the edit menu",
                          font=(font_style, 13), bg="#ffffff")
        tip_label.grid(columnspan=5, pady=(10, 50), sticky="w", column=1)
        submit_button = Button(window, cursor="hand2", image=start_button_image, text="Let's Start  ",
                               font=(font_style, 20, 'bold'), activebackground="#ffffff",
                               bg="#ffffff", command=write_first_details, relief="flat",
                               compound=RIGHT)
        submit_button.grid(columnspan=5)

    if not first_run:
        move_to_end_cb = Checkbutton(window, text="Move completed tasks to end of list", variable=move_done_to_end,
                                     font=(font_style, 12), command=update_main_data,
                                     bg="#ffffff", relief="flat", highlightthickness=0)
        move_to_end_cb.grid(columnspan=8, pady=(30, 0), column=2)


def about_screen():
    global about_top, user_program_version

    if (not about_top) or (about_top.winfo_exists() == 0):
        about_top = Toplevel(window)
        about_top.config(background="#ffffff")
        # about_top.iconbitmap(icon_file)
        about_top.geometry("300x200")
        about_top.title("Tasks - About")
        about_top.resizable(False, False)
        Label(about_top, text=f"Tasks {user_program_version}", font=('arial', 14), bg="#ffffff").grid(pady=20)
        Label(about_top, text="Pragadesh BS", bg="#ffffff", justify=LEFT).grid(sticky="nw")
        Button(about_top, image=small_done_image, command=about_top.destroy, activebackground="#ffffff",
               bg="#ffffff", relief="flat", cursor="hand2").grid(padx=140, pady=20)


def add_task_screen():
    due_date = datetime.today().date()
    window.title("Tasks - Add Task")

    def select_due_date():
        nonlocal due_date
        global top

        def cal_done(catch_null):
            nonlocal select_date_button, due_date
            print(catch_null) if False else None
            due_date = cal.selection_get()
            select_date_button["text"] = due_date.strftime('%a, %d %b %Y')
            top.destroy()

        if not top or top.winfo_exists() == 0:
            top = Toplevel(window)
            top.geometry("450x300")
            # top.iconbitmap(icon_file)
            top.resizable(False, False)
            cal = Calendar(top, font="Arial 14", showweeknumbers=False, selectmode='day',
                           cursor="hand2", mindate=date.today(), background="#ffffff", foreground="#565656",
                           bordercolor="#ffffff", headersbackground="#fff9f9", headersforeground="#292929",
                           disableddaybackground="#dbdbdb", weekendbackground="#f8f8f8",
                           othermonthbackground="#dbdbdb", othermonthwebackground="#dbdbdb",
                           disableddayforeground="#f3f3f3", selectbackground="#ff6f6f", year=int(due_date.year),
                           month=int(due_date.month), day=int(due_date.day),
                           othermonthforeground="#3a3a3a", weekendforeground="#3a3a3a",
                           othermonthweforeground="#3a3a3a")
            cal.pack(fill="both", expand=True)
            cal.bind("<<CalendarSelected>>", cal_done)

    def place_submit_button():
        nonlocal submit_button
        submit_button.grid(row=4, pady=50, columnspan=10)

    def short_message(text):
        nonlocal submit_button
        submit_button.grid_forget()
        message = Label(window, text=text, bg="#ffffff", fg="#ff0000", font=('calibri', 16), wraplength=250)
        message.grid(row=4, columnspan=10, pady=50)
        message.after(2000, message.grid_remove)
        message.after(2000, place_submit_button)

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

    Button(window, command=home_screen, activebackground="#ffffff",
           image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff", relief="flat",
           cursor="hand2").grid(sticky="nw")

    header_label = Label(window, text="Add task", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=400, pady=(0, 20))

    Label(window, text="Set a title for your task", padx=100, bg="#ffffff", fg="#31442b",
          font=(font_style, 16)).grid(pady=(25, 25))
    task_title_entry = Entry(window, width=35, font=('calibri', 12), bg="#fff9f9", relief="flat")
    task_title_entry.grid(row=1, column=1, ipady=2)

    Label(window, text="Select a due date", padx=100, bg="#ffffff", fg="#31442b",
          font=(font_style, 16)).grid(pady=(50, 50))
    select_date_button = Button(window, relief="flat", text=due_date.strftime('%a, %d %b %Y'),
                                font=('calibri', 16), bg="#fff9f9", fg="#545454", activeforeground="#545454",
                                activebackground="#fff9f9", cursor="hand2", command=select_due_date)
    select_date_button.grid(row=2, column=1, pady=(50, 50))

    Label(window, text="Add notes to your task\n(Optional)", padx=20, bg="#ffffff",
          fg="#31442b", font=(font_style, 16)).grid()
    task_notes_entry = Text(window, wrap=WORD, height=10, font=('calibri', 12), width=35,
                            bg="#fff9f9", relief="flat")
    task_notes_entry.grid(row=3, column=1, padx=100)

    submit_button = Button(window, relief="flat", text="  Add task", command=validate_task,
                           font=(font_style, 16), bg="#ffffff", fg="#292929", activeforeground="#292929",
                           activebackground="#ffffff", cursor="hand2", image=create_image,
                           compound=LEFT)
    place_submit_button()


def write_task(task_string):
    global tasks_data_file
    with open(tasks_data_file, "r") as file:
        content = file.read()
    to_write = task_string
    if content:
        if content[-1][-1] != "\n":
            to_write = "\n"+task_string
    # print("yes" if content[-1][-1] == "\n" else "no")
    # to_write = "\n"+task_string if content else task_string
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


def create_task(t_title, t_due_date, t_notes, edited=False, complete=False, edited_t_id=1):
    global master_task_count, no_tasks_pending, tasks_to_display
    master_task_count += 1
    no_tasks_pending += 1
    update_main_data()
    if not edited:
        new_task = Task(t_title, t_due_date, t_notes, master_task_count)
    else:
        new_task = Task(t_title, t_due_date, t_notes, edited_t_id)
    if complete:
        new_task.is_done.set(1)
    formatted_task = new_task.form_string()
    write_task(formatted_task)
    tasks_to_display.append(new_task)
    home_screen()

    def short_message(text):
        message = Label(window, text=text, bg="#ffffff", fg="#007cff", font=('calibri', 16, 'bold'), wraplength=250)
        message.grid(row=1, column=1, columnspan=6)
        message.after(2000, message.grid_remove)

    if not edited:
        short_message("Added task to list")
    else:
        short_message("Task has been modified")


def update_main_data():
    global main_data_file, master_task_count, user_name, sort_method
    global move_done_to_end, task_highlighting, user_program_version

    to_write = f"$user_name: {user_name}\n$master_task_count: {master_task_count}" \
               f"\n$sort_method: {sort_method.get()}\n$move_done_to_end: {move_done_to_end.get()}" \
               f"\n$task_highlighting: {task_highlighting.get()}" \
               f"\n$check_update_at_startup: {check_update_at_startup.get()}" \
               f"\n$program_version: {user_program_version}"

    with open(main_data_file, "w") as file:
        file.write(to_write)


def reset_screen():
    window.title("Tasks - Reset Data")
    menu(0)
    init_screen()
    Button(window, command=home_screen, activebackground="#fff8f8", image=back_button_image,
           font=("sans serif", 16, 'bold'), bg="#fff8f8",
           relief="flat", cursor="hand2").grid(row=0, sticky="nw")
    window.config(background="#fff8f8")
    exclamation_label = Label(window, bg="#fff8f8", font=("calibri", 150), text="!", fg="#FF5733")
    exclamation_label.grid(row=0, pady=(0, 60), padx=(300, 0), rowspan=8, column=1)
    reset_label_text = "Data reset will permanently delete all details " \
                       "associated with the program. Be sure before you proceed."
    Label(window, font=('Arial', 14), text=reset_label_text, fg="#4d4d4d", wraplength=550,
          bg="#fff8f8").grid(pady=(0, 100), padx=200, columnspan=8)
    Button(window, text="  Reset data", cursor="hand2", font=(font_style, 12), image=reset_image,
           activeforeground="#4d4d4d", activebackground="#fff8f8", bg="#fff8f8", fg="#4d4d4d",
           relief="flat", command=reset_data, compound=LEFT).grid(column=1, columnspan=5)


def clear_widgets():
    widgets = window.winfo_children()
    for widget in widgets:
        if not type(widget) == tkinter.Toplevel:
            widget.grid_remove()


def init_screen():
    clear_widgets()


def reset_data():
    # reset all data files associated with the program
    with open(main_data_file, "w") as open_file:
        open_file.write("")
    with open(tasks_data_file, "w") as open_file:
        open_file.write("")
    init_screen()
    menu(0)
    window.config(background="#ffffff")
    Label(window, bg="#ffffff", fg="#31442b", wraplength=600, font=("century gothic", 16),
          text="Program reset was successful, Restart program to see changes").grid(pady=(60, 0), padx=200)
    Button(window, text="Exit  ", font=("calibri", 16), activeforeground="#646464", activebackground="#ffffff",
           command=window.destroy, fg="#646464", cursor="hand2", bg="#ffffff", relief="flat",
           image=exit_image, compound=RIGHT).grid(pady=(100, 0))


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
    # selections = []
    # t_status = IntVar()

    # for task in tasks_to_display:
    #    selections.append(task.is_done.get())

    with open(tasks_data_file, "w") as file:
        file.write("")

    for i in tasks_to_display:
        str_task = i.form_string()
        write_task(str_task)

    home_screen()


def change_task_details(task_id):
    init_screen()

    for task in tasks_to_display:

        if task.id == task_id:
            t_title = StringVar()
            t_title.set(task.title)
            t_dd = datetime.strptime(task.due_date, "%a, %d %b %Y")
            t_notes = task.notes

            if task.is_done.get() == 1:
                t_done = True
            else:
                t_done = False

            if t_notes == "No notes were set for this task":
                t_notes = ""
            break

    else:
        error(1, "FILE_CORRUPT")
        return

    window.title("Tasks - Edit Task")

    def select_due_date():
        nonlocal t_dd
        global top

        def cal_done(catch_null):
            nonlocal select_date_button, t_dd
            print(catch_null) if False else None
            t_dd = cal.selection_get()
            select_date_button["text"] = t_dd.strftime('%a, %d %b %Y')
            top.destroy()

        if not top or top.winfo_exists() == 0:
            top = Toplevel(window)
            top.geometry("450x300")
            # top.iconbitmap(icon_file)
            top.resizable(False, False)
            cal = Calendar(top, font="Arial 14", showweeknumbers=False, selectmode='day',
                           cursor="hand2", mindate=date.today(), background="#ffffff", foreground="#565656",
                           bordercolor="#ffffff", headersbackground="#d9e5ff", headersforeground="#292929",
                           disableddaybackground="#8c8c8c", weekendbackground="#f5f5f5",
                           othermonthbackground="#dbdbdb", othermonthwebackground="#dbdbdb",
                           disableddayforeground="#f3f3f3", selectbackground="#ff9e9e", year=int(t_dd.year),
                           month=int(t_dd.month), day=int(t_dd.day))
            cal.pack(fill="both", expand=True)
            cal.bind("<<CalendarSelected>>", cal_done)

    def place_submit_button():
        nonlocal submit_button
        submit_button.grid(row=4, pady=50, columnspan=10)

    def short_message(text):
        nonlocal submit_button
        submit_button.grid_forget()
        message = Label(window, text=text, bg="#ffffff", fg="#ff0000", font=('calibri', 16), wraplength=250)
        message.grid(row=4, columnspan=10, pady=50)
        message.after(2000, message.grid_remove)
        message.after(2000, place_submit_button)

    def validate_task():
        nonlocal t_dd, task_title_entry, task_notes_entry, submit_button

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
            task_notes = task_notes[:len(task_notes) - 1]

        remove_old_task()
        create_task(task_title, t_dd, task_notes, edited=True, complete=t_done, edited_t_id=task_id)

    def remove_old_task():
        nonlocal task_id
        for i in range(len(tasks_to_display)):
            if tasks_to_display[i].id == task_id:
                remove_task_from_file([task_id])
                tasks_to_display.pop(i)
                break

    Button(window, command=home_screen, activebackground="#ffffff",
           image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff", relief="flat",
           cursor="hand2").grid(sticky="nw")

    header_label = Label(window, text="Edit task", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=400, pady=(0, 20))

    Label(window, text="Title ", bg="#ffffff", fg="#31442b",
          font=(font_style, 16)).grid(pady=(25, 25), padx=(200, 0))
    task_title_entry = Entry(window, width=35, font=('calibri', 12), bg="#fff9f9", textvariable=t_title,
                             relief="flat")
    task_title_entry.grid(row=1, column=1, ipady=2, padx=(200, 0))

    Label(window, text="Due date", bg="#ffffff", fg="#31442b",
          font=(font_style, 16)).grid(pady=(50, 50), padx=(200, 0))
    select_date_button = Button(window, relief="flat", text=t_dd.strftime('%a, %d %b %Y'),
                                font=('calibri', 16), bg="#fff9f9", fg="#545454", activeforeground="#545454",
                                activebackground="#fff9f9", cursor="hand2", command=select_due_date)
    select_date_button.grid(row=2, column=1, pady=(50, 50), padx=(200, 0))

    Label(window, text="Notes\n(Optional)", bg="#ffffff", fg="#31442b",
          font=(font_style, 16)).grid(padx=(200, 0))
    task_notes_entry = Text(window, wrap=WORD, height=10, font=('calibri', 12), width=35,
                            bg="#fff9f9", relief="flat")
    task_notes_entry.insert("1.0", t_notes)
    task_notes_entry.grid(row=3, column=1, padx=(200, 0))

    submit_button = Button(window, relief="flat", text="  Update task", command=validate_task,
                           font=(font_style, 16), bg="#ffffff", fg="#292929", activeforeground="#292929",
                           activebackground="#ffffff", cursor="hand2", image=edit_done_image,
                           compound=LEFT)
    place_submit_button()


def calc_days_left(task):
    today_date = datetime.today()
    task_due = datetime.strptime(task.due_date, "%a, %d %b %Y")
    return -(today_date - task_due).days


def sort_tasks():
    global tasks_to_display, sort_method

    if sort_method.get() == 0:
        tasks_to_display.sort(key=calc_days_left)
    elif sort_method.get() == 1:
        tasks_to_display.sort(key=Task.get_id, reverse=True)

    i = 0

    # setting back completed tasks
    if move_done_to_end.get() == 1:
        while i < len(tasks_to_display):

            count = 0

            while count < len(tasks_to_display)-i:

                if tasks_to_display[i].is_done.get() == 1:
                    tasks_to_display.append(tasks_to_display.pop(i))
                    count += 1
                    continue

                break

            i += 1


def move_task(t_id, direction):
    global tasks_to_display, sort_method

    if sort_method.get() != 1:
        return

    for index, task in enumerate(tasks_to_display):
        if task.id == t_id:
            break

    else:
        error(3, "TASK_SORT_ERROR")
        return

    if direction == -1:
        if index > 0:
            tasks_to_display[index].id, tasks_to_display[index-1].id = tasks_to_display[index-1].id, \
                                                                       tasks_to_display[index].id
            update_task_status()
            return

    if direction == 0:
        if index > 0:
            while index > 0:
                tasks_to_display[index].id, tasks_to_display[index-1].id = tasks_to_display[index-1].id, \
                                                                           tasks_to_display[index].id
                index -= 1
                sort_tasks()
            update_task_status()
            return

    if direction == 1:
        if index < len(tasks_to_display)-1:
            tasks_to_display[index].id, tasks_to_display[index+1].id = tasks_to_display[index+1].id, \
                                                                       tasks_to_display[index].id
            update_task_status()
            return

    if direction == 2:
        if index < len(tasks_to_display)-1:
            while index < len(tasks_to_display)-1:
                tasks_to_display[index].id, tasks_to_display[index + 1].id = tasks_to_display[index + 1].id, \
                                                                             tasks_to_display[index].id
                index += 1
                sort_tasks()
            update_task_status()
        return


def list_tasks():
    global no_tasks_pending, tasks_to_display, task_highlighting

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
    priority = format_text(9, "Priority")
    number_header = format_text(11, "No.")
    mad_label_text = format_text(14, "Mark as done")

    main_frame = tkinter.ttk.Frame(window, width=990, height=320)
    main_frame.grid(columnspan=6)
    sf = ScrolledFrame(main_frame, width=980, height=310)
    sf.grid()
    sf.bind_arrow_keys(main_frame)
    sf.bind_scroll_wheel(main_frame)
    frame = sf.display_widget(Frame)

    mad_label = Label(frame, text=mad_label_text, fg="#317250", font=(font_style, 12))
    mad_label.grid(row=task_table_start_row, column=task_table_start_column)

    num_label = Label(frame, text=number_header, fg="#317250", font=(font_style, 12))
    num_label.grid(row=task_table_start_row, column=task_table_start_column+1)

    column_no = 1

    if sort_method.get() == 1:
        priority_label = Label(frame, text=priority, fg="#317250", font=(font_style, 12))
        priority_label.grid(row=task_table_start_row, column=task_table_start_column + 2, columnspan=2)
        column_no = 3

    t_title_label = Label(frame, text=task_title, fg="#317250", font=(font_style, 12))
    t_title_label.grid(row=task_table_start_row, column=task_table_start_column+column_no+1)

    dd_label = Label(frame, text=task_due_date, fg="#317250", font=(font_style, 12))
    dd_label.grid(row=task_table_start_row, column=task_table_start_column+column_no+2)

    notes_label = Label(frame, text=task_notes, fg="#317250", font=(font_style, 12))
    notes_label.grid(row=task_table_start_row, column=task_table_start_column+column_no+3)

    for index, task in enumerate(tasks_to_display):
        check_button = Checkbutton(frame, cursor="hand2", variable=task.is_done, command=update_task_status)

        if task.is_done.get() == 1:
            check_button.select()

        font_color = "#000000"
        font_weight = 'normal'
        font_size = 11
        title_to_display = task.title

        if (task.is_done.get() == 0) and (task_highlighting.get() == 1):

            if calc_days_left(task) < 0:
                title_to_display += "\n(PAST DUE)"

            elif calc_days_left(task) == 0:
                title_to_display += "\n(Due today)"

            if calc_days_left(task) <= 0:
                font_weight = 'bold'
                font_color = "#ff0000"
                font_size = 13

            elif calc_days_left(task) <= 3:
                font_color = "#ff5d00"

        if sort_method.get() == 1:
            check_button.grid(row=current_row, column=task_table_start_column, rowspan=2, padx=(30, 30), pady=(10, 10))
        else:
            check_button.grid(row=current_row, column=task_table_start_column, padx=(30, 30), pady=(15, 15))

        no_label = Label(frame, text=task_no, font=('calibri', 11))

        if sort_method.get() == 1:
            no_label.grid(row=current_row, column=current_column+1, rowspan=2, padx=(30, 30), pady=(15, 15))
        else:
            no_label.grid(row=current_row, column=current_column+1, padx=(30, 30), pady=(15, 15))

        t_column_no = 1

        if sort_method.get() == 1:
            priority_button1 = Label(frame, image=up_arrow_image, cursor="hand2")
            priority_button1.bind("<Button-1>", lambda e, t_id=task.id: move_task(t_id, -1))

            priority_button2 = Label(frame, image=top_arrow_image, cursor="hand2")
            priority_button2.bind("<Button-1>", lambda e, t_id=task.id: move_task(t_id, 0))

            priority_button3 = Label(frame, image=down_arrow_image, cursor="hand2")
            priority_button3.bind("<Button-1>", lambda e, t_id=task.id: move_task(t_id, 1))

            priority_button4 = Label(frame, image=bottom_arrow_image, cursor="hand2")
            priority_button4.bind("<Button-1>", lambda e, t_id=task.id: move_task(t_id, 2))

            priority_button1.grid(padx=(30, 10), row=current_row, column=current_column+2,
                                  sticky="se", pady=(20, 10))  # up arrow
            priority_button2.grid(padx=(10, 30), row=current_row, column=current_column + 3,
                                  sticky="sw", pady=(20, 10))  # top arrow
            priority_button3.grid(row=current_row+1, column=current_column + 2, sticky="ne",
                                  pady=(10, 20), padx=(30, 10))  # down arrow
            priority_button4.grid(row=current_row+1, column=current_column + 3, sticky="nw",
                                  pady=(10, 20), padx=(10, 30))  # bottom arrow

            if index == 0:
                priority_button1.config(state=DISABLED)
                priority_button2.config(state=DISABLED)
                priority_button1.config(cursor="")
                priority_button2.config(cursor="")

            if index == len(tasks_to_display)-1:
                priority_button3.config(state=DISABLED)
                priority_button4.config(state=DISABLED)
                priority_button3.config(cursor="")
                priority_button4.config(cursor="")

            t_column_no = 3

        title_label = Label(frame, relief="flat", cursor="hand2", fg=font_color,
                            text=title_to_display, wraplength=150, font=('calibri', font_size, font_weight),
                            activeforeground=font_color)
        title_label.bind("<Button-1>", lambda e, t_id=task.id: change_task_details(t_id))

        if sort_method.get() == 1:
            title_label.grid(row=current_row, column=t_column_no+1, padx=(30, 30), rowspan=2, pady=(15, 15))
        else:
            title_label.grid(row=current_row, column=t_column_no + 1, padx=(50, 50), pady=(15, 15))

        due_label = Label(frame, relief="flat", cursor="hand2", fg=font_color, text=task.due_date,
                          font=('calibri', font_size, font_weight))
        due_label.bind("<Button-1>", lambda e, t_id=task.id: change_task_details(t_id))

        if sort_method.get() == 1:
            due_label.grid(row=current_row, column=t_column_no+2, padx=(30, 30), rowspan=2, pady=(15, 15))
        else:
            due_label.grid(row=current_row, column=t_column_no + 2, padx=(50, 50), pady=(15, 15))

        notes_label = Label(frame, relief="flat", cursor="hand2",
                            text=task.notes, wraplength=200, justify=CENTER, font=('calibri', 11))
        notes_label.bind("<Button-1>", lambda e, t_id=task.id: change_task_details(t_id))

        if sort_method.get() == 1:
            notes_label.grid(row=current_row, column=t_column_no+3, padx=(30, 30), rowspan=2, pady=(15, 15))
        else:
            notes_label.grid(row=current_row, column=t_column_no + 3, padx=(50, 50), pady=(15, 15))

        current_row += 2
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
        message = Label(window, text=text, bg="#ffffff", fg="#ff0000", font=('calibri', 16), wraplength=250)
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
        task_info_text = "You currently have no tasks. Enjoy a cup of coffee!"
    elif pending_count == 1:
        task_info_text = "You currently have 1 task remaining"
    else:
        task_info_text = f"You currently have {pending_count} tasks remaining"


def menu(action):
    # action set to 1 to makes menu visible, anything else makes it invisible/removes the menu
    if action == 1:
        menu_bar = Menu(window, background="#ffffff", activebackground='#ffffff')
        file = Menu(menu_bar, tearoff=0, background="#ffffff")
        program_help = Menu(menu_bar, tearoff=0, background="#ffffff")
        edit = Menu(menu_bar, tearoff=0, background="#ffffff")
        menu_bar.add_cascade(label="File", menu=file)
        menu_bar.add_cascade(label="Edit", menu=edit)
        menu_bar.add_cascade(label="Help", menu=program_help)
        file.add_command(label="Reset", command=reset_screen)
        file.add_command(label="Exit", command=window.destroy)
        edit.add_command(label="Sorting tasks", command=sort_settings_screen)
        edit.add_command(label="Appearance", command=appearance_settings_screen)
        program_help.add_command(label="About", command=about_screen)
        program_help.add_command(label="Updates", command=update_screen)
        window.config(menu=menu_bar)
        return

    remove_menu = Menu(window)
    window.config(menu=remove_menu)


def home_screen(startup=False):
    # main screen of the program, displays greet message, tasks pending info if any
    global user_name, time_greet_data, tasks_to_display, task_info_text
    global pending_task_label, to_update
    window.config(background="#ffffff")
    window.title("Tasks")

    init_screen()
    menu(1)

    header_label = Label(window, text="Tasks", font=(font_style, 40), bg="#ffffff", fg="#716747")
    greet_label_text = f"{time_greet_data} {user_name}!"
    greet_label = Label(window, font=(font_style, 16), text=greet_label_text, bg="#ffffff", fg="#31442b")
    add_task_button = Button(window, command=add_task_screen, relief="flat", cursor="hand2", bg="#ffffff",
                             activebackground="#ffffff",
                             text="  Add a task", font=('calibri', 14), image=add_new_image, compound=LEFT)
    remove_task_button = Button(window, text="  Remove completed tasks",
                                command=remove_tasks, relief="flat", cursor="hand2",
                                bg="#ffffff", activebackground="#ffffff", font=('calibri', 14),
                                image=delete_image, compound=LEFT)

    pending_task_info()
    pending_task_label = Label(window, text=task_info_text, font=(font_style, 11), bg="#ffffff")

    header_label.grid(padx=400, columnspan=10, pady=(0, 3))
    greet_label.grid(sticky="w", pady=(20, 20), padx=(30, 0))
    pending_task_label.grid(columnspan=10)

    list_tasks()

    if tasks_to_display:
        add_task_button.grid(pady=20, columnspan=2)
        remove_task_button.grid(row=4, columnspan=4, column=1)

    else:
        add_task_button.grid(pady=20, columnspan=10)

    if startup:
        if check_update_at_startup.get() == 1:
            add_task_button.after(1000, lambda: check_for_updates(True))


def error(code, sub_code):
    # code 0 - critical error, stops the program from execution
    # code 1 - file corrupt error, notify user, reset data files and relaunch program

    if code == 0:
        window.config(background="#ffffff")
        init_screen()
        Label(window, text="Critical Error", bg="#ffffff").grid()
        error_label_text = f"Error Code: {sub_code}\n\nWe've run into an error, " \
                           f"we had trouble while trying to access program files :(" \
                           f"\n\n\nThis would most likely occur if the program " \
                           f"has been installed in a system folder and is " \
                           f"run without administrator privileges"
        error_label = Label(window, text=error_label_text, wraplength=550)
        error_label.grid()

    if code == 1:
        window.config(background="#ffffff")
        init_screen()
        Label(window, text="Runtime Error", bg="#ffffff", fg="red", font=('calibri', 16, 'bold')).grid(columnspan=4)
        error_label_text = f"Error Code: {sub_code}\n\n\nWe've run into an error, something went " \
                           f"wrong with the program files :(" \
                           f"\n\nResetting program files might help, " \
                           f"but you will lose all data associated with this program"
        error_label = Label(window, text=error_label_text, bg="#ffffff", font=('calibri', 14))
        error_label.grid(pady=(50, 10), padx=5, columnspan=4)
        Button(window, text="Reset Data", cursor="hand2", relief="flat", command=reset_data, bg="#ffbcbc",
               font=('calibri', 14), activebackground="#ffbcbc").grid(pady=50, column=1)
        Button(window, text="Exit", cursor="hand2", relief="flat", command=window.destroy, bg="#bfffbc",
               font=('calibri', 14), activebackground="#bfffbc").grid(pady=50, row=2, column=2)

    if code == 3:
        pass
    # code 3 for runtime error while sorting tasks and such, most probably restart would fix


def extract_tasks():
    # throw critical error if file corrupt - to be modified to a format error
    # extract tasks and add task object to tasks_to_display list
    global tasks_data_file, no_tasks_pending, tasks_to_display

    with open(tasks_data_file, "r") as file:
        content = file.readlines()

    if not len(content) == no_tasks_pending:
        error(0, "FILE_CORRUPT")
        return

    try:
        for i in content:
            task_sliced = i.split("^^")
            new_task_id = int(task_sliced[0][1:])
            new_task_is_done = int(task_sliced[1])
            new_task_title = task_sliced[2]
            new_task_dd = task_sliced[3]
            task_notes_in_file = task_sliced[4][:len(task_sliced[4])]
            if task_notes_in_file.endswith("\n"):
                task_notes_in_file = task_notes_in_file[:len(task_notes_in_file) - 1]
            new_task_notes = ""
            for j in task_notes_in_file:
                if j == "^":
                    new_task_notes += "\n"
                    continue
                new_task_notes += j
            new_task_dd = datetime.strptime(new_task_dd, "%a, %d %b %Y")
            new_task = Task(new_task_title, new_task_dd, new_task_notes, new_task_id)

            task_status = IntVar()
            if new_task_is_done == 1:
                task_status.set(1)
            else:
                task_status.set(0)
            new_task.is_done = task_status

            tasks_to_display.append(new_task)
        return 1

    except ValueError:
        error(1, "FILE_CORRUPT")
        return -1


def extract_data():
    # return cases: 0 - File empty; 1 - Extracted data successfully and redirected to extract_tasks
    global main_data_file, user_name, master_task_count, tasks_data_file, no_tasks_pending
    global sort_method, move_done_to_end, task_highlighting, user_program_version
    global check_update_at_startup

    with open(main_data_file, "r") as open_file:
        user_data = open_file.readlines()

    if not user_data:
        return 0

    if user_data:

        with open(tasks_data_file, "r") as open_file:
            task_content = open_file.readlines()

        try:
            user_name = user_data[0][12:len(user_data[0])-1]

            master_task_count = int(user_data[1][20:])

            sort_method.set(int(user_data[2][14:]))

            temp_move_done_to_end = int(user_data[3][19:])

            move_done_to_end.set(temp_move_done_to_end)

            temp_task_highlighting = int(user_data[4][20:])
            task_highlighting.set(temp_task_highlighting)

            temp_check_update_at_startup = int(user_data[5][26:])
            check_update_at_startup.set(temp_check_update_at_startup)

            user_program_version = user_data[6][18: len(user_data[6])]
            if user_program_version.endswith("\n"):
                user_program_version = user_program_version[:len(user_program_version)-1]
            user_program_version = float(user_program_version)

        except (ValueError, IndexError):
            error(1, "FILE_CORRUPT")
            return -1

        if not task_content:
            no_tasks_pending = 0

        else:
            no_tasks_pending = len(task_content)

            if extract_tasks() == -1:
                error(1, "FILE_CORRUPT")
                return -1

    return 1


def auto_create_data_files_path():
    # return cases: 1 - created data file parent dir; -1 - OSError encountered
    global data_files_parent_path
    init_screen()

    try:
        mkdir(data_files_parent_path)
        return 1

    except (OSError, PermissionError):
        return -1


def initiate_data_files():
    # return cases: 1 - Created a new file; 0 - File already exists; -1 - Path does not exist
    global data_files_parent_path, main_data_file, tasks_data_file

    if path.isdir(data_files_parent_path):

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


def write_first_details():
    global user_name, master_task_count, user_program_version

    to_write = f"$user_name: {user_name}\n$master_task_count: {master_task_count}" \
               f"\n$sort_method: {sort_method.get()}\n$move_done_to_end: 1" \
               f"\n$task_highlighting: 1\n$check_update_at_startup: 1" \
               f"\n$program_version: {user_program_version}"

    with open(main_data_file, "w") as open_file:
        open_file.write(to_write)

    home_screen()


def first_launch_handler():
    global user_name, sort_method, user_name_var
    sort_method.set(0)  # engaging auto task sort
    init_screen()

    def place_submit_button():
        nonlocal submit_button
        submit_button.grid(row=4, column=0, columnspan=10, pady=50)

    def validate_name():
        global user_name
        nonlocal name_entry, submit_button
        to_check = name_entry.get()
        to_check = to_check.strip()

        if (len(to_check)) < 3 or (len(to_check) > 20):
            submit_button.grid_forget()
            short_m = Label(window, bg="#ffffff", font=(font_style, '14', 'bold'),
                            text="Enter a name that is 3-20 characters in length", fg="#ff0000")
            short_m.grid(row=4, column=0, columnspan=10, pady=20)
            submit_button.after(2000, place_submit_button)
            short_m.after(2000, short_m.grid_remove)
            return

        user_name = to_check
        user_name_var.set(user_name)
        sort_settings_screen(True)

    welcome_label = Label(window, text="Welcome to Tasks!",
                          font=(font_style, 48, 'bold'), fg="#464646", bg="#ffffff")
    welcome_label_2 = Label(window, pady=30, text="Task management, made easy",
                            font=(font_style, 28), fg="#d33200", bg="#ffffff")

    name_label = Label(window, text="Enter your name to start ", font=('century gothic', 18), bg="#ffffff")
    name_entry = Entry(window, textvariable=user_name_var, font=('calibri', 16), relief="flat",
                       bg="#ffe9e9")

    submit_button = Button(window, cursor="hand2", text="  Done", image=done_button_image,
                           activebackground="#ffffff", bg="#ffffff", command=validate_name, relief="flat",
                           font=('arial', 20), compound=LEFT)

    welcome_label.grid(columnspan=10, row=0, ipadx=20, pady=(70, 0), padx=200)
    welcome_label_2.grid(columnspan=8, column=1, row=1, ipadx=5)
    name_label.grid(row=2, columnspan=4, column=2, pady=(20, 0))
    name_entry.grid(row=2, columnspan=6, column=4, pady=(20, 0))
    place_submit_button()


def update_window():
    global user_program_version, latest_program_version
    update_top = Toplevel(window)
    update_top.config(background="#ffffff")
    update_top.geometry("300x200")
    update_top.title("Tasks - Update")
    update_top.resizable(False, False)

    info_label_text = "An Update is available, you are using an older version of this program" \
                      f"\nNew version: {latest_program_version}\nYour version: {user_program_version}"
    info_label = Label(update_top, text=info_label_text, bg="#ffffff")
    info_label.grid(padx=(100, 100), columnspan=5)

    update_top.attributes('-topmost', True)
    update_top.update()
    update_top.attributes('-topmost', False)


def update_screen():
    global check_update_at_startup
    init_screen()

    info_label_text = "Checking for updates..."
    info_label = Label(window, text=info_label_text, font=(font_style, 16), bg="#ffffff")
    retry_btn = Button(window, image=refresh_2_image, command=lambda: check_update(True),
                       relief="flat", bg="#ffffff", activebackground="#ffffff")

    def check_update(recall=False):
        nonlocal info_label, check_now_btn
        if recall:
            retry_btn.grid_forget()
        check_now_btn.grid_remove()
        info_label.config(text="Checking for updates...")
        info_label.grid(columnspan=10, pady=50)
        info_label.after(100, get_update_status)

    def get_update_status():
        nonlocal info_label
        status = check_for_updates()

        if status == 0:
            info_label.config(text="You're up to date")

            return

        if status == -1:
            info_label.config(text="We are having trouble connecting to the server\n"
                                   "\nCheck your connection and try again")
            retry_btn.grid(columnspan=10)
            return

        if status == 1:
            info_label.config(text=f"An update is available\nNew version: {latest_program_version}"
                                   f"\nYour version: {user_program_version}")
            download_button = Button(window, text="Update", bg="#ffffff", activebackground="#ffffff",
                                     command=lambda: webbrowser.open("https://srv-store5.gofile.io/"
                                                                     "download/nTgxFa/Tasks_setup.exe"), relief="flat",
                                     font=(font_style, 16), cursor="hand2")
            download_button.grid(columnspan=10)

    Button(window, command=home_screen, activebackground="#ffffff",
           image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff", relief="flat",
           cursor="hand2").grid(sticky="nw")

    header_label = Label(window, text="Update Tasks", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=350, pady=(0, 20))

    check_update_at_startup_cb = Checkbutton(window, text="Automatically check for updates during startup",
                                             variable=check_update_at_startup,
                                             font=(font_style, 16), command=update_main_data,
                                             bg="#ffffff", relief="flat", highlightthickness=0)
    check_update_at_startup_cb.grid(columnspan=10, pady=(30, 0))

    check_now_btn = Button(window, image=refresh_image, text="Check for updates now  ",
                           command=check_update, bg="#ffffff", compound=RIGHT,
                           activebackground="#ffffff", relief="flat", cursor="hand2",
                           font=(font_style, 16))
    check_now_btn.grid(columnspan=10, pady=(50, 0))


def check_for_updates(auto_check=False):
    global to_update, user_program_version, latest_program_version

    def get_latest_program_version():
        global latest_program_version
        try:
            source_code_url = 'https://raw.githubusercontent.com/PragadeshBS/Tasks/main/main.py'
            response = urllib.request.urlopen(source_code_url)
            source_code = response.read()
            source_code_str = source_code.decode("utf-8")
            source_code_lines = source_code_str.split("\n")
            for line in source_code_lines:
                if line.startswith("latest_program_version"):
                    latest_program_version = float(line[25:])
                    return 1
            return 0
        except urllib.error.URLError:
            return -1

    def popup_window():
        update_top = Toplevel(window)
        update_top.config(background="#ffffff")
        update_top.geometry("300x250")
        update_top.title("Tasks - Update")
        update_top.resizable(False, False)
        header = Label(update_top, text="An Update is Available", font=('arial', 14), bg="#ffffff",
                       fg="#d33200")
        header.grid(pady=20, padx=50, columnspan=5)
        info_label_text = f"New version: {latest_program_version}\nYour version: {user_program_version}"
        info_label = Label(update_top, text=info_label_text, bg="#ffffff")
        info_label.grid(columnspan=5)
        download_button = Button(update_top, text="Update now", bg="#ffffff", relief="flat",
                                 command=lambda: webbrowser.open("https://srv-store5.gofile.io/"
                                                                 "download/nTgxFa/Tasks_setup.exe"), cursor="hand2",
                                 activebackground="#ffffff")
        not_now_button = Button(update_top, text="Ignore", bg="#ffffff", command=update_top.destroy,
                                relief="flat", cursor="hand2", activebackground="#ffffff")
        download_button.grid(row=2, column=1, pady=(25, 25))
        not_now_button.grid(row=2, column=3, pady=(25, 25))
        tip_label_text = "Tip: You can turn off automatic updates from the help menu"
        tip_label = Label(update_top, text=tip_label_text, bg="#ffffff", wraplength=250)
        tip_label.grid(pady=20, columnspan=5)

    if get_latest_program_version() == 1:
        if user_program_version < latest_program_version:
            to_update = True
            if auto_check:
                popup_window()
            return 1
        return 0
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

    check_data = extract_data()

    if check_data == 0:
        first_launch_handler()
        return

    elif check_data == -1:
        error(1, "FILE_CORRUPT")
        return

    elif check_data == 1:
        home_screen(True)


def time_greet():
    global time_greet_data, current_time

    if current_time.hour < 12:
        time_greet_data = "Good morning"
    elif current_time.hour < 16:
        time_greet_data = "Good afternoon"
    else:
        time_greet_data = "Good evening"


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


if __name__ == '__main__':  # starter function
    update_index()
    main()

window.mainloop()
