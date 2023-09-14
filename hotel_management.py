import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

#Dark mode
is_dark_mode = False
main_window = None
data_to_edit = None

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    if is_dark_mode:
        main_window.configure(bg="black")
        for button in buttons:
            button.configure(bg="black", fg="white", highlightbackground="white", highlightcolor="white", borderwidth=0, highlightthickness=0)
    else:
        main_window.configure(bg="white")
        for button in buttons:
            button.configure(bg="white", fg="black", highlightbackground="black", highlightcolor="black", borderwidth=0, highlightthickness=0)
#Login
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "Admin" and password == "jarvis":
        root.withdraw()
        global main_window
        main_window = tk.Tk()
        main_window.title("Menu Page")
        main_window.geometry("400x200")

        #Creating individual buttons
        button1 = tk.Button(main_window, text="New Booking", command=lambda: button_click(1), bg="white", borderwidth=0, highlightthickness=0)
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        button2 = tk.Button(main_window, text="Past bookings", command=display_past_bookings, bg="white", borderwidth=0, highlightthickness=0)
        button2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        button3 = tk.Button(main_window, text="Room edit", command=room_edit_window, bg="white", borderwidth=0, highlightthickness=0)
        button3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        button4 = tk.Button(main_window, text="Delete", command=remove_record_window, bg="white", borderwidth=0, highlightthickness=0)
        button4.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        button5 = tk.Button(main_window, text="Accounts", command=lambda: button_click(5), bg="white", borderwidth=0, highlightthickness=0)
        button5.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        button6 = tk.Button(main_window, text="Settings", command=lambda: button_click(6), bg="white", borderwidth=0, highlightthickness=0)
        button6.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        global buttons
        buttons = [button1, button2, button3, button4, button5, button6]

        for i in range(3):
            main_window.columnconfigure(i, weight=1)
            main_window.rowconfigure(i, weight=1)

        #dark mode/light mode toggle button
        toggle_button = tk.Button(main_window, text="🌙", command=toggle_dark_mode)
        toggle_button.grid(row=2, column=2, padx=10, pady=10, sticky="se")

        main_window.mainloop()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def open_form_window():
    form_window = tk.Tk()
    form_window.title("Form Page")

    #Creating form questions
    questions = ["Name of Member:", "Email id:", "Date of Birth:", "Day of Entry:", "Day of Exit:", "Number of Guests:",    ]
    entry_fields = []

    for i, question in enumerate(questions):
        label = tk.Label(form_window, text=question)
        label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
        entry = tk.Entry(form_window)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="e")
        entry_fields.append(entry)

    #Room Types
    room_types = ["Single", "Double", "Suite", "Family"]
    room_type_label = tk.Label(form_window, text="Room Type:")
    room_type_label.grid(row=len(questions), column=0, padx=10, pady=10, sticky="w")
    room_type_var = tk.StringVar(value=room_types[0])
    room_type_dropdown = ttk.Combobox(form_window, textvariable=room_type_var, values=room_types)
    room_type_dropdown.grid(row=len(questions), column=1, padx=10, pady=10, sticky="e")

    def save_form_data():
        data = [entry.get() for entry in entry_fields]
        selected_room_type = room_type_var.get()

        if not selected_room_type:
            messagebox.showerror("Missing Room Type", "Please select a Room Type and the number.")
            return

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="jarvis", database="hotel")

            cursor = db.cursor()

            sql = "INSERT INTO hotel (name_of_member, email, date_of_birth, day_of_entry, day_of_exit, number_of_guests, room_types) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, tuple(data + [selected_room_type]))
            db.commit()
            messagebox.showinfo("Success", "Form data saved successfully!")
            form_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error: {err}")

    submit_button = tk.Button(form_window, text="Submit", command=save_form_data)
    submit_button.grid(row=len(questions) + 1, columnspan=2, padx=10, pady=10)

    form_window.mainloop()

def button_click(button_number):
    if button_number == 1:
        open_form_window()
    else:
        print(f"Clicked: Button {button_number}")


def display_past_bookings():
    
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="jarvis", database="hotel")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hotel")
        past_bookings_data = cursor.fetchall()
        past_bookings_window = tk.Toplevel(main_window)
        past_bookings_window.title("Past Bookings")
        
        past_bookings_table = ttk.Treeview(past_bookings_window, columns=("id", "Name of Member", "Email id", "Dtae of Birth", "Date of Entry", "Date of Exit", "Number of Guests", "Room Type"))
        past_bookings_table.heading("#1", text="id")
        past_bookings_table.heading("#2", text="Name of member")
        past_bookings_table.heading("#3", text="Email id")
        past_bookings_table.heading("#4", text="Date of birth")
        past_bookings_table.heading("#5", text="Date of entry")
        past_bookings_table.heading("#6", text="Date of exit")
        past_bookings_table.heading("#7", text="No of guest")
        past_bookings_table.heading("#8", text="Room Type")

        # Column width
        column_widths = (50, 120, 120, 100, 100, 100, 100, 100)

        for i, width in enumerate(column_widths):
            past_bookings_table.column(f"#{i+1}", width=width)
        for booking in past_bookings_data:
            past_bookings_table.insert("", "end", values=booking)

        past_bookings_table.pack()

    except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", f"Error: {err}")

def room_edit_window():
    room_edit_window = tk.Toplevel(main_window)
    room_edit_window.title("Room Edit")

    id_label = tk.Label(room_edit_window, text="Enter ID to Edit:")
    id_label.pack()

    id_entry = tk.Entry(room_edit_window)
    id_entry.pack()

    def fetch_data_to_edit():
        id_to_edit = id_entry.get()

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="jarvis", database="hotel")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM hotel WHERE id = %s", (id_to_edit,))
            global data_to_edit
            data_to_edit = cursor.fetchone()

            if data_to_edit:
                edit_room_data()
            else:
                messagebox.showerror("Data Not Found", f"No data found for ID {id_to_edit}")

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error: {err}")

    def edit_room_data():
        edit_window = tk.Toplevel(room_edit_window)
        edit_window.title("Edit Room Data")

        questions = ["Name of Member:", "Email id:", "Date of Birth:", "Day of Entry:", "Day of Exit:", "Number of Guests:"]
        entry_fields = []

        for i, question in enumerate(questions):
            label = tk.Label(edit_window, text=question)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="e")
            entry_fields.append(entry)
            entry.insert(0, data_to_edit[i + 1])

        room_types = ["Single", "Double", "Suite", "Family"]
        room_type_label = tk.Label(edit_window, text="Room Type:")
        room_type_label.grid(row=len(questions), column=0, padx=10, pady=10, sticky="w")
        room_type_var = tk.StringVar(value=data_to_edit[7]) 
        room_type_dropdown = ttk.Combobox(edit_window, textvariable=room_type_var, values=room_types)
        room_type_dropdown.grid(row=len(questions), column=1, padx=10, pady=10, sticky="e")

        def update_data():
            updated_data = [entry.get() for entry in entry_fields]
            updated_room_type = room_type_var.get()

            try:
                db = mysql.connector.connect(host="localhost", user="root", password="jarvis", database="hotel")


                cursor = db.cursor()

                cursor.execute(
                    "UPDATE hotel SET name_of_member=%s, email=%s, date_of_birth=%s, day_of_entry=%s, day_of_exit=%s, number_of_guests=%s, room_type=%s WHERE id = %s",
                    tuple(updated_data + [updated_room_type] + [data_to_edit[0]]))
                db.commit()
                messagebox.showinfo("Success", "Room data updated successfully!")
                edit_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("MySQL Error", f"Error: {err}")

        submit_button = tk.Button(edit_window, text="Update", command=update_data)
        submit_button.grid(row=len(questions) + 1, columnspan=2, padx=10, pady=10)

    fetch_button = tk.Button(room_edit_window, text="Fetch Data", command=fetch_data_to_edit)
    fetch_button.pack()


def remove_record_window():
    remove_window = tk.Toplevel(main_window)
    remove_window.title("Remove Record")

    id_label = tk.Label(remove_window, text="Enter ID to Remove:")
    id_label.pack()

    id_entry = tk.Entry(remove_window)
    id_entry.pack()

    def remove_record():
        id_to_remove = id_entry.get()
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="jarvis", database="hotel")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM hotel WHERE id = %s", (id_to_remove,))
            record_to_remove = cursor.fetchone()

            if record_to_remove:
                cursor.execute("DELETE FROM hotel WHERE id = %s", (id_to_remove,))
                db.commit()
                messagebox.showinfo("Success", f"Record with ID {id_to_remove} removed successfully!")
                remove_window.destroy()
            else:
                messagebox.showerror("Data Not Found", f"No data found for ID {id_to_remove}")

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error: {err}")

    remove_button = tk.Button(remove_window, text="Remove", command=remove_record)
    remove_button.pack()

root = tk.Tk()
root.title("Login Page")
root.geometry("574x432")
background_image = Image.open(r"C:\Users\Hp\Downloads\LAIfhup.png")
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

username_label = tk.Label(root, text="Username:")
username_label.place(x=70, y=230)

username_entry = tk.Entry(root, borderwidth=0)
username_entry.place(x=70, y=230)

#password label and entry field
password_label = tk.Label(root, text="Password:")
password_label.place(x=70, y=305)

password_entry = tk.Entry(root, show="*", borderwidth=0, relief="flat")
password_entry.place(x=70, y=305)

#login button
login_button = tk.Button(root, text="Login", command=login)
login_button.place(x=70, y=350)
root.mainloop()
