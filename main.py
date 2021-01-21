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
latest_program_version = 2.2
user_program_version = 2.2
can_start = False
to_update = False
window = Tk()
window.title("Tasks")
window.geometry("1000x600")
window.configure(background="#ffffff")
window.resizable(False, False)
update_loop = True
time_greet_data = "Good morning"
current_time = datetime.now()
tasks_to_display = []
task_info_text = ""
pending_task_label = Label(window)
font_style = "century gothic"
about_top = top = None
sort_method = IntVar()  # 0 - auto; 1 - manual
move_done_to_end = IntVar()
move_done_to_end.set(1)
task_highlighting = IntVar()
task_highlighting.set(1)
check_update_at_startup = IntVar()
check_update_at_startup.set(1)
current_screen = 1  # 1-home; 2- add task; 3 - edit task; 4 - reset; 5- sort settings; 6 - appearance settings
# 7 - username change; 8 - update screen

# paths
data_files_parent_path = getcwd()
main_data_file_name = "data.txt"
tasks_data_file_name = "tasks.txt"
main_data_file = path.join(data_files_parent_path, main_data_file_name)
tasks_data_file = path.join(data_files_parent_path, tasks_data_file_name)


def error(code, sub_code):

    if code == 1:
        window.config(background="#ffffff")
        init_screen()
        window.title("Tasks - Critical Error")
        Label(window, text="Runtime Error", bg="#ffffff", fg="red",
              font=('calibri', 28, 'bold')).grid(columnspan=10, padx=(200, 0))
        error_label_text = f"Error Code: {sub_code}\n\n\nWe've run into an error, the program " \
                           f"files are corrupt" \
                           f"\n\nResetting the program files might help, " \
                           f"but you will lose all data associated with this program"
        error_label = Label(window, text=error_label_text, bg="#ffffff", font=('calibri', 14))
        error_label.grid(pady=(50, 10), columnspan=10, padx=(140, 0))
        Button(window, text="Reset Data", cursor="hand2", relief="flat", command=reset_data, bg="#ffbcbc",
               font=('calibri', 14), activebackground="#ffbcbc").grid(pady=50, column=5)
        Button(window, text="Exit", cursor="hand2", relief="flat", command=window.destroy, bg="#bfffbc",
               font=('calibri', 14), activebackground="#bfffbc").grid(pady=50, row=2, column=6)

    if code == 3:
        # code 3 for runtime error while sorting tasks and such, most probably restart would fix
        window.config(background="#ffffff")
        window.title("Tasks - Runtime Error")
        Label(window, text="Runtime Error", bg="#ffffff", fg="red",
              font=('calibri', 28, 'bold')).grid(columnspan=10, padx=(300, 0))
        error_label_text = f"Error Code: {sub_code}\n\n\nWe've run into an error, something went really wrong :( " \
                           f"\n\nRestarting the program might help"
        error_label = Label(window, text=error_label_text, bg="#ffffff", font=('calibri', 14))
        error_label.grid(pady=(50, 10), columnspan=10, padx=(200, 0))
        Button(window, text="Exit", cursor="hand2", relief="flat", command=window.destroy, bg="#bfffbc",
               font=('calibri', 14), activebackground="#bfffbc").grid(pady=50, row=2, columnspan=4, column=5)

    if code == 4:
        # Permission denied to write file
        window.title("Tasks - Critical Error")
        Label(window, text="Critical Error", bg="#ffffff",
              fg="red", font=('calibri', 28, 'bold')).grid(columnspan=10, padx=(150, 0))
        error_label_text = f"Error Code: {sub_code}\n\n\nWe've run into an error, something went " \
                           f"wrong while we were looking for program files :(" \
                           f"\n\nThis might be most probably caused " \
                           f"if the program is installed in a restricted \nfolder and " \
                           f"run without administrator privileges" \
                           f"\n\n\n\nReinstalling the program might fix this issue"
        error_label = Label(window, text=error_label_text, bg="#ffffff", font=('calibri', 14))
        error_label.grid(pady=(50, 10), columnspan=10, padx=(140, 0))
        Button(window, text="Exit", cursor="hand2", relief="flat", command=window.destroy, bg="#fff8f8",
               font=('calibri', 14), activebackground="#fff8f8").grid(pady=50, row=2, columnspan=10,
                                                                      padx=(150, 0))
        return

    if code == 5:
        # initial file check failed
        window.title("Tasks - Critical Error")
        Label(window, text="Critical Error", bg="#ffffff",
              fg="red", font=('calibri', 28, 'bold')).grid(columnspan=10, padx=(100, 0))
        error_label_text = f"Error Code: {sub_code}\n\n\nWe've run into an error, something went " \
                           f"wrong while we were looking for program files :(" \
                           f"\n\nThis might be most probably caused " \
                           f"if the program files were deleted or moved to another directory " \
                           f"\n\n\n\nReinstalling the program might fix this issue"
        error_label = Label(window, text=error_label_text, bg="#ffffff", font=('calibri', 14))
        error_label.grid(pady=(50, 10), columnspan=10, padx=(100, 0))
        Button(window, text="Exit", cursor="hand2", relief="flat", command=window.destroy, bg="#fff8f8",
               font=('calibri', 14), activebackground="#fff8f8").grid(pady=50, row=2, columnspan=10,
                                                                      padx=(100, 0))

# paths


try:

    icon_file_name = "logo.png"
    icon_file = path.join(data_files_parent_path, icon_file_name)

    image_icon_files = ['logo.png', 'addnew.png', 'backarrow.png', 'bottomarrow.png',
                         'create.png', 'delete.png', 'done.png', 'downarrow.png',
                         'editdone.png', 'exit.png', 'logo.png', 'refresh.png', 'refresh2.png',
                         'reset.png', 'smalldone.png', 'start.png', 'toparrow.png', 'uparrow.png']

    for file in image_icon_files:
        if not path.isfile(path.join(data_files_parent_path, file)):
            raise TclError

    # images/icons
    logo = PhotoImage(file=icon_file)
    window.iconphoto(True, logo)
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
    can_start = True

except TclError:
    error(5, "FILE_NOT_FOUND")


# data variables
user_name_var = StringVar()
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
    global current_screen
    current_screen = 6
    init_screen()
    window.title("Tasks - Appearance Settings")

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
    task_highlighting_cb.grid(columnspan=10, pady=(100, 0))


def change_name_screen():
    global user_name, user_name_var, current_screen
    current_screen = 7
    init_screen()
    window.title("Tasks - Change User Name")

    def place_submit_button():
        nonlocal submit_button
        global current_screen
        if current_screen == 7:
            submit_button.grid(row=3, columnspan=10, pady=100)

    def validate_new_name():
        global user_name
        nonlocal new_name_entry, submit_button
        to_check = new_name_entry.get()
        to_check = to_check.strip()

        if (len(to_check)) < 3 or (len(to_check) > 20):
            submit_button.grid_forget()
            short_m = Label(window, bg="#ffffff", font=(font_style, '14', 'bold'),
                            text="Enter a name that is 3-20 characters in length", fg="#ff0000")
            short_m.grid(row=4, column=0, columnspan=10, pady=100)
            submit_button.after(2000, place_submit_button)
            short_m.after(2000, short_m.grid_remove)
            return

        user_name = to_check
        user_name_var.set(user_name)
        update_main_data()
        home_screen()
        message = Label(window, text="User name was changed", bg="#ffffff",
                        fg="#00af82", font=('calibri', 16), wraplength=250)
        message.grid(row=1, column=1, columnspan=6)
        message.after(2000, message.grid_remove)

    back_button = Button(window, command=home_screen, activebackground="#ffffff", activeforeground="#565656",
                         image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff",
                         fg="#d33200", relief="flat", cursor="hand2")

    back_button.grid(sticky="nw")

    header_label = Label(window, text="Change User Name", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=300, pady=(0, 20))

    new_name_label_text = f"Hello {user_name}. Enter a new name: "
    new_name_label = Label(window, text=new_name_label_text, font=('century gothic', 18), bg="#ffffff")
    new_name_entry = Entry(window, textvariable=user_name_var, font=('calibri', 16),
                           relief="flat", bg="#ffe9e9")

    submit_button = Button(window, cursor="hand2", text="  Done", image=done_button_image,
                           activebackground="#ffffff", bg="#ffffff", command=validate_new_name, relief="flat",
                           font=('arial', 20), compound=LEFT)

    new_name_label.grid(row=2, columnspan=6, pady=(100, 0))
    new_name_entry.grid(row=2, columnspan=4, column=5, pady=(100, 0))
    place_submit_button()


def sort_settings_screen(first_run=False):
    global sort_method, current_screen
    current_screen = 5
    init_screen()
    window.title("Tasks - Sort Settings")

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
        if first_run:
            rad_btn.grid(columnspan=5, column=1, pady=(15, 15), sticky="w")
        else:
            rad_btn.grid(columnspan=10, column=3, pady=(15, 15), sticky="w")

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
        move_to_end_cb.grid(columnspan=10, column=1, pady=(30, 0))


def about_screen():
    global about_top, user_program_version

    if (not about_top) or (about_top.winfo_exists() == 0):
        about_top = Toplevel(window)
        about_top.config(background="#ffffff")
        # about_top.iconbitmap(icon_file)
        about_top.geometry("500x370")
        about_top.title("Tasks - About")
        about_top.resizable(False, False)
        Label(about_top, text=f"Tasks {user_program_version}",
              font=('arial', 14), bg="#ffffff").grid(pady=20, padx=(150, 0))
        Label(about_top, text="Pragadesh BS\n\nTasks is a freeware licensed under the GNU "
                              "General Public License\n", bg="#ffffff", justify=LEFT).grid(sticky="nw")

        main_frame = tkinter.ttk.Frame(about_top, width=480, height=150)
        main_frame.grid(columnspan=6)
        sf = ScrolledFrame(main_frame, width=470, height=160)
        sf.grid()
        sf.bind_arrow_keys(main_frame)
        sf.bind_scroll_wheel(main_frame)
        frame = sf.display_widget(Frame)

        Label(frame, text="GNU General Public License v3.0", font=('arial', 12)).grid(padx=20)
        license_text = """
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  'This License' refers to version 3 of the GNU General Public License.

  'Copyright' also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  'The Program' refers to any copyrightable work licensed under this
License.  Each licensee is addressed as 'you'.  'Licensees' and
'recipients' may be individuals or organizations.

  To 'modify' a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a 'modified version' of the
earlier work or a work 'based on' the earlier work.

  A 'covered work' means either the unmodified Program or a work based
on the Program.

  To 'propagate' a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To 'convey' a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays 'Appropriate Legal Notices'
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The 'source code' for a work means the preferred form of the work
for making modifications to it.  'Object code' means any non-source
form of a work.

  A 'Standard Interface' means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The 'System Libraries' of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
'Major Component', in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The 'Corresponding Source' for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    'keep intact all notices'.

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
'aggregate' if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A 'User Product' is either (1) a 'consumer product', which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, 'normally used' refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  'Installation Information' for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  'Additional permissions' are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered 'further
restrictions' within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An 'entity transaction' is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A 'contributor' is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's 'contributor version'.

  A contributor's 'essential patent claims' are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, 'control' includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a 'patent license' is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To 'grant' such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  'Knowingly relying' means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is 'discriminatory' if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License 'or any later version' applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM 'AS IS' WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the 'copyright' line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an 'about box'.

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a 'copyright disclaimer' for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>."""
        Label(frame, text=license_text).grid()
        Button(about_top, image=small_done_image, command=about_top.destroy, activebackground="#ffffff",
               bg="#ffffff", relief="flat", cursor="hand2").grid(padx=(170, 0), pady=20)


def add_task_screen():
    global current_screen
    current_screen = 2
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
        global current_screen
        if current_screen == 2:
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
    global current_screen
    current_screen = 4
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
    global current_screen
    current_screen = 3
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
        global current_screen
        if current_screen == 3:
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
        edit.add_command(label="User Name", command=change_name_screen)
        program_help.add_command(label="About", command=about_screen)
        program_help.add_command(label="Updates", command=update_screen)
        window.config(menu=menu_bar)
        return

    remove_menu = Menu(window)
    window.config(menu=remove_menu)


def home_screen(startup=False):
    # main screen of the program, displays greet message, tasks pending info if any
    global user_name, time_greet_data, tasks_to_display, task_info_text
    global pending_task_label, to_update, current_screen
    current_screen = 1
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


def extract_tasks():
    # throw critical error if file corrupt - to be modified to a format error
    # extract tasks and add task object to tasks_to_display list
    global tasks_data_file, no_tasks_pending, tasks_to_display

    with open(tasks_data_file, "r") as file:
        content = file.readlines()

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
            if user_program_version == 2.1:
                user_program_version = 2.2
                update_main_data()

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
            try:
                with open(main_data_file, "a"):
                    pass
                with open(tasks_data_file, "a"):
                    pass
            except PermissionError:
                return -1
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


def update_screen():
    global check_update_at_startup, current_screen
    current_screen = 8
    init_screen()
    window.title("Tasks - Updates")

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
                                     command=lambda: webbrowser.open("https://gofile.io/d/nTgxFa"), relief="flat",
                                     font=(font_style, 16), cursor="hand2")
            download_button.grid(columnspan=10)

    Button(window, command=home_screen, activebackground="#ffffff",
           image=back_button_image, font=("sans serif", 16, 'bold'), bg="#ffffff", relief="flat",
           cursor="hand2").grid(sticky="nw")

    header_label = Label(window, text="Update Tasks", bg="#ffffff", fg="#d33200",
                         font=(font_style, 28))
    header_label.grid(row=0, columnspan=10, padx=350, pady=(0, 20))

    check_update_at_startup_cb = Checkbutton(window, text="Automatically check for updates during startup",
                                             variable=check_update_at_startup, cursor="hand2",
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
                                 command=lambda: webbrowser.open("https://gofile.io/d/nTgxFa"), cursor="hand2",
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
            error(4, "PERMISSION_DENIED_FOR_FILE_INIT")
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
    if can_start:
        update_index()
        main()

window.mainloop()
