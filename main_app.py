import tkinter as tk
import mysql.connector
import csv
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

WHITE = "#F9F7F7"
BLUE = '#3F72AF'
LIGHT_BLUE = "#DBE2EF"
GREEN = "#9bdeac"
LIGHT_GREEN = "#B4FF9F"
RED = "#e7305b"
SKY_BLUE = "#40DFEF"


class DataBase(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self, bg=GREEN)
        container.place(x=0, y=0, width=1360, height=730)
        self.frames = {}
        for F in (RegPage, MainPage, HazInventory, HazPullout, ComChecklist, ChemicalInventory):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, width=1360, height=730)

        self.show_frame("RegPage")

    def show_frame(self, page_name):
        """show the frame that was raised"""
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE)
        self.controller = controller
        self.title_frame = Frame(self, bg=LIGHT_BLUE)
        self.title_frame.place(x=0, y=0, width=1400, height=60)
        self.title_label = Label(self.title_frame, text="ECS DATABASE MANAGEMENT SYSTEM",
                                font=("helvetica", 18, "bold"), bg="#DBE2EF", fg="#112D4E", highlightthickness=0)
        self.title_label.place(x=350, y=10)
        self.app_version_label = Label(self.title_frame, text=" v. 1.000.1",
                                font=("helvetica", 10, "bold"), bg="#DBE2EF", fg="#112D4E", highlightthickness=0)
        self.app_version_label.place(x=960, y=20)

        self.check_btn = tk.Button(self, text="Legal", width=15, bg=BLUE, borderwidth=0,
                                   command=lambda: DataBase.show_frame(self.controller, "ComChecklist"))
        self.check_btn.place(x=100, y=450)

        # legal button
        self.legal_canvas = tk.Canvas(self, width=210, height=210, bg="white")
        self.legal_canvas.place(x=60, y=220)
        self.legal_img = (Image.open("legal.png"))
        self.legal_resized_img = self.legal_img.resize((210, 210), Image.LANCZOS)
        self.legal_new_img = ImageTk.PhotoImage(self.legal_resized_img)
        self.legal_canvas.create_image(2, 2, anchor=NW, image=self.legal_new_img)

        # hazardous button
        inventory_btn = tk.Button(self, text="Hazardous", width=15, bg=BLUE, borderwidth=0,
                                  command=lambda: DataBase.show_frame(self.controller, "HazInventory"))
        inventory_btn.place(x=350, y=450)
        self.haz_canvas = tk.Canvas(self, width=210, height=210, bg="white")
        self.haz_canvas.place(x=313, y=220)
        self.haz_img = (Image.open("hazardous.png"))
        self.haz_resized_img = self.haz_img.resize((210, 210), Image.LANCZOS)
        self.haz_new_img = ImageTk.PhotoImage(self.haz_resized_img)
        self.haz_canvas.create_image(2, 2, anchor=NW, image=self.haz_new_img)

        # pullout button
        pullout_btn = tk.Button(self, text="Pullout", width=15, bg=BLUE, borderwidth=0,
                                command=lambda: DataBase.show_frame(self.controller, "HazPullout"))
        pullout_btn.place(x=600, y=450)
        self.pullout_canvas = tk.Canvas(self, width=210, height=210, bg="white")
        self.pullout_canvas.place(x=560, y=220)
        self.pullout_img = (Image.open("hazardous.png"))
        self.pullout_resized_img = self.pullout_img.resize((210, 210), Image.LANCZOS)
        self.pullout_new_img = ImageTk.PhotoImage(self.pullout_resized_img)
        self.pullout_canvas.create_image(2, 2, anchor=NW, image=self.pullout_new_img)

        chemical_btn = tk.Button(self, text="Inventory", width=15, bg=BLUE, borderwidth=0,
                                 command=lambda: DataBase.show_frame(self.controller, "ChemicalInventory"))
        chemical_btn.place(x=850, y=450)
        self.chemical_canvas = tk.Canvas(self, width=210, height=210, bg="white")
        self.chemical_canvas.place(x=810, y=220)
        self.chemical_img = (Image.open("inventory.png"))
        self.chemical_resized_img = self.chemical_img.resize((210, 210), Image.LANCZOS)
        self.chemical_new_img = ImageTk.PhotoImage(self.chemical_resized_img)
        self.chemical_canvas.create_image(2, 2, anchor=NW, image=self.chemical_new_img)

        registration_btn = tk.Button(self, text="LOGIN", width=15, bg=BLUE, borderwidth=0,
                                     command=lambda: DataBase.show_frame(self.controller, "RegPage"))
        registration_btn.place(x=1100, y=450)


class RegPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F9F7F7")
        self.controller = controller
        self.login = None

        self.title_frame = Frame(self, bg="#DBE2EF", highlightthickness=0)
        self.title_frame.place(x=0, y=0, width=1400, height=60)
        self.title_label = Label(self.title_frame, text="ECS DATABASE MANAGEMENT SYSTEM",
                                font=("helvetica", 18, "bold"), bg="#DBE2EF", fg="#112D4E", highlightthickness=0)
        self.title_label.place(x=350, y=10)
        self.app_version_label = Label(self.title_frame, text=" v. 1.000.1",
                                font=("helvetica", 10, "bold"), bg="#DBE2EF", fg="#112D4E", highlightthickness=0)
        self.app_version_label.place(x=960, y=20)

        self.login_btn = Button(self, text="LOGIN", font=("helvetica", 10), borderwidth=0,
                                bg="#83BD75", command=self.login_window)
        self.login_btn.place(x=1250, y=80)
        reg_btn = Button(self, text="Register", font=("helvetica", 10), borderwidth=0,
                         bg="#83BD75", command=self.reg_window)
        reg_btn.place(x=1150, y=80)

    def login_window(self):
        self.login = Toplevel(self, bg=WHITE)
        self.login.geometry("500x120")
        name_label = Label(self.login, text="Username", font=("helvetica", 8), bg="#E8E8A6")
        name_label.place(x=20, y=22)
        self.login_username_entry = Entry(self.login, width=30)
        self.login_username_entry.place(x=120, y=20, height=30)
        pass_label = Label(self.login, text="Password", font=("helvetica", 8), bg="#E8E8A6")
        pass_label.place(x=20, y=72)
        self.login_password_entry = Entry(self.login, width=30)
        self.login_password_entry.place(x=120, y=70, height=30)
        self.reg_sub_btn = Button(self.login, text="Submit", height=2, font=("helvetica", 8),
                         bg="#83BD75", command=self.login_confirm)
        self.reg_sub_btn.place(x=420, y=30)

    def login_confirm(self):
        # connect to mysql
        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="Piquero17",
                                       database="my_database")
        # initialize the database
        cur = mydb.cursor()
        cur.execute(" SELECT `Username`, `Password` FROM registration")
        reg_data = cur.fetchall()
        # fetch data from entry
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        for row in reg_data:
            if username == row[0] and password == row[1]:
                DataBase.show_frame(self.controller, "MainPage")
                self.login.destroy()

    def reg_window(self):
        self.reg_frame = LabelFrame(self, text="Register Here", font=("helvetica", 8))
        self.reg_frame.place(x=400, y=200, width=480, height=400)
        reg_fname_lbl = Label(self.reg_frame, text="First Name", font=("helvetica", 8))
        reg_fname_lbl.place(x=10, y=50)
        self.reg_fname_entry = Entry(self.reg_frame, width=30)
        self.reg_fname_entry.place(x=120, y=50)
        reg_lname_lbl = Label(self.reg_frame, text="Last Name", font=("helvetica", 8))
        reg_lname_lbl.place(x=10, y=100)
        self.reg_lname_entry = Entry(self.reg_frame, width=30)
        self.reg_lname_entry.place(x=120, y=100)
        reg_username_lbl = Label(self.reg_frame, text="Username", font=("helvetica", 8))
        reg_username_lbl.place(x=10, y=150)
        self.reg_username_entry = Entry(self.reg_frame, width=30)
        self.reg_username_entry.place(x=120, y=150)
        reg_password_lbl = Label(self.reg_frame, text="Enter Password", font=("helvetica", 8))
        reg_password_lbl.place(x=10, y= 200)
        self.reg_password_entry = Entry(self.reg_frame, width=20)
        self.reg_password_entry.place(x=120, y=200)
        reg_confirm_btn = Button(self.reg_frame, text="Confirm", width=10, command=self.reg_confirm)
        reg_confirm_btn.place(x=20, y=300)
        reg_cancel_btn = Button(self.reg_frame, text="Cancel", width=10, command=self.reg_cancel)
        reg_cancel_btn.place(x=20, y=300)

    def reg_confirm(self):
        # save the registry inputs
        firstname = self.reg_fname_entry.get()
        lastname = self.reg_lname_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        # connect to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        # initialize the database
        cur = mydb.cursor()
        db_reg = " INSERT INTO registration(`First Name`, `Last Name`, `Username`, `Password`) " \
                 "values( %s, %s, %s, %s)"
        val = (firstname, lastname, username, password)
        cur.execute(db_reg, val)
        mydb.commit()
        mydb.close()
        # delete the frame for reg.
        self.reg_frame.destroy()

    def reg_cancel(self):
        pass


class HazInventory(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BLUE)
        self.controller = controller
        # frame for main buttons
        self.btn_main = tk.LabelFrame(self, text="Hazardous", bg=LIGHT_BLUE)
        self.btn_main.place(x=0, y=0, width=160, height=730)

        back_btn = tk.Button(self.btn_main, text="Back", width=15, bg=BLUE, borderwidth=0,
                             command=lambda: DataBase.show_frame(controller, "MainPage"))
        back_btn.place(x=10, y=50)
        new_entry_btn = Button(self.btn_main, text='New Entry', bg=BLUE, width=15, borderwidth=0,
                               command=self.top_inventory)
        new_entry_btn.place(x=10, y=100)
        export_excel_button = Button(self.btn_main, text="Export", bg=BLUE, width=15, borderwidth=0,
                                     command=self.convert_excel)
        export_excel_button.place(x=10, y=150)

        # frame for checklist
        self.haztree_frame = Frame(self, bg=LIGHT_BLUE)
        self.haztree_frame.place(x=160, y=50, width=1300, height=630)
        self.haz_btn_frame = Frame(self, bg=LIGHT_BLUE)
        self.haz_btn_frame.place(x=160, y=0, width=1300, height=50)

        filter_btn = Button(self.haz_btn_frame, text="Filter", command=self.filter)
        filter_btn.place(x=1125, y=10)
        self.filter_entry = Entry(self.haz_btn_frame, width=20)
        self.filter_entry.place(x=950, y=10, height=30)

        # connect python to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        # initialize the database
        cur = mydb.cursor()

        # create treeview
        columns = ("id", "Date", "Waste Type", "Volume Input", "Volume Output", "Volume Balance", "Type of Container",
                   "Section", "Monitored By")
        # create scrollbar inside treeview
        haz_canvas = tk.Canvas(self.haztree_frame)
        haz_canvas.place(x=0, y=0, width=1200, height=630)
        self.listbox = ttk.Treeview(haz_canvas, columns=columns, show="headings")
        haz_scrollbar = Scrollbar(haz_canvas, orient=HORIZONTAL, command=self.listbox.xview)
        for col in columns:
            self.listbox.heading(col, text=col)
            self.listbox.pack(fill="both", expand=True)
            self.listbox.column(col, stretch=True, anchor=CENTER, width=100)
            self.listbox.config(xscrollcommand=haz_scrollbar.set)
        haz_scrollbar.configure = Scrollbar(haz_canvas, orient=HORIZONTAL, command=self.listbox.xview)
        haz_scrollbar.place(x=0, y=608, width=1200)

        # connect python to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        # initialize the database
        cur = mydb.cursor()
        cur.execute(
            'SELECT `id`, `Date`, `Waste Type`, `Volume Input`, `Volume Output`, `Volume Balance`, `Type of Container`'
            ', `Section`, `Monitored By` FROM hazardous')
        # fetch data at the mysql
        self.listbox.delete(*self.listbox.get_children())
        mysql_data = cur.fetchall()
        for row in mysql_data:
            self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        self.treeview_right_click()

        mydb.commit()
        mydb.close()

    # filter data from treeview
    def filter(self):
        # get the data at entry
        query = self.filter_entry.get()
        # delete treeview data
        for rec in self.listbox.get_children():
            self.listbox.delete(rec)

        try:
            # connect python to mysql
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
            # initialize the database(
            cur = mydb.cursor()
            data_sql = "SELECT * FROM hazardous WHERE (`Waste Type` LIKE '%s') OR (`Section` = '%s') " \
                       "OR (`Monitored By` = '%s'); "
            cur.execute(data_sql % (query, query, query))
            # fetch the selected column
            data = cur.fetchall()
            # insert data to treeview
            for d in data:
                self.listbox.insert("", END, values=d)
        except Exceptions as e:
            messagebox.showerror(title="Error!", message=f"{e}")
        # delete typed filter
        self.filter_entry.delete(0, END)

# create new window for hazardous waste inputs
    def top_inventory(self):
        self.new = Toplevel(self)
        self.new.geometry("700x550")
        self.new.title("Add Information!")

        self.menu = StringVar()
        self.mon = StringVar()
        self.waste = StringVar()

        self.menu.set("Select")
        self.mon.set("Select")
        self.waste.set("Select")

        sec_label = Label(self.new, text="Section")
        sec_label.place(x=30, y=50)
        self.sec_menu = OptionMenu(self.new, self.menu, "CCD", "CWP", "SWP", "PWS", "POC", "CCI")
        self.sec_menu.place(x=160, y=50)
        self.sec_menu.config(width=15)

        waste_label = Label(self.new, text="Waste Type")
        waste_label.place(x=30, y=100)
        self.waste_menu = OptionMenu(self.new, self.waste, "A101", "B299", "C399", "D402", "D407", "F604", "G703",
                                     "G704", "I101", "I104", "J201", "K301")
        self.waste_menu.place(x=160, y=100)
        self.waste_menu.config(width=15)

        mon_label = Label(self.new, text="Monitored By")
        mon_label.place(x=30, y=150)
        self.mon_menu = OptionMenu(self.new, self.mon, "Miguelito Baguio", "Branley Basubas")
        self.mon_menu.place(x=160, y=150)
        self.mon_menu.config(width=15)

        cont_label = Label(self.new, text="Type of Container")
        cont_label.place(x=30, y=200)
        self.cont_entry = Entry(self.new, width=20)
        self.cont_entry.place(x=160, y=200)

        date_label = Label(self.new, text="Date")
        date_label.place(x=30, y=250)
        self.cal = DateEntry(self.new, width=17, selectmode="day", year=2022, month=4, day=7)
        self.cal.place(x=160, y=250)

        in_label = Label(self.new, text="Volume Input")
        in_label.place(x=30, y=300)
        self.in_entry = Entry(self.new, width=20)
        self.in_entry.place(x=160, y=300)

        out_label = Label(self.new, text="Volume Out")
        out_label.place(x=30, y=350)
        self.out_entry = Entry(self.new, width=20)
        self.out_entry.place(x=160, y=350)

        self.confirm_btn = Button(self.new, text="Confirm", width=10, command=self.add_inv)
        self.confirm_btn.place(x=30, y=450)
        self.cancel_btn = Button(self.new, text="Cancel", width=10, command=self.cancel)
        self.cancel_btn.place(x=150, y=450)

    # add entry at mysql
    def add_inv(self):
        section = self.menu.get()
        waste = self.waste.get()
        container_entry = self.cont_entry.get()
        monitored = self.mon.get()
        calendar = self.cal.get()

        try:
            self.input_entry = float(self.in_entry.get())
            self.output_entry = float(self.out_entry.get())
        except ValueError:
            messagebox.showerror(message="Input value in number!")

        try:
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
            cur = mydb.cursor()
            # insert data at mysql workbench
            sql_db = "INSERT INTO hazardous(`Date`,`Waste Type`,`Volume Input`, `Volume Output`, `Type of Container`," \
                     "`Section`,`Monitored By`) values(%s,%s,%s, %s, %s, %s, %s)"
            val = (calendar, waste, self.input_entry, self.output_entry, container_entry, section, monitored)
            cur.execute(sql_db, val)
            # update treeview table
            cur.execute(
                'SELECT `Date`,`Waste Type`, `Volume Input`, `Volume Output`, `Volume Balance`, `Type of Container`'
                ', `Section`, `Monitored By` FROM hazardous')
            # fetch data at the mysql
            self.listbox.delete(*self.listbox.get_children())
            mysql_data = cur.fetchall()
            for row in mysql_data:
                self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            mydb.commit()
            mydb.close()

        except Exception as e:
            print(e)

    def treeview_right_click(self):
        """ popup menu after double- click on treeview widget table"""
        self.menu_click = Menu(self, tearoff=False)
        self.menu_click.add_command(label="Edit", command=self.edit_haz_treeview)
        self.menu_click.add_command(label="Delete", command=self.delete_haz_treeview)
        self.menu_click.add_command(label="Filter", command=self.filter_haz_treeview)
        self.menu_click.add_separator()
        self.menu_click.add_command(label="Exit", command=self.exit_menu)
        
        self.listbox.bind("<Button-3>", self.menu_event)

    def edit_haz_treeview(self):
        """Function Method for updating/editing entries at treeview widget"""
        self.edit_window = Toplevel(self)
        self.edit_window.geometry("400x450")
        self.edit_window.title("Information!")

        # grab entry values from treeview
        for child in self.listbox.get_children():
            if child == self.entry_index:
                self.value = self.listbox.item(child)["values"]

        dc_id_label = Label(self.edit_window, text="ID")
        dc_id_label.place(x=30, y=80)
        self.dc_id_entry = Entry(self.edit_window, width=15)
        self.dc_id_entry.place(x=160, y=80)
        dc_date_label = Label(self.edit_window, text="date")
        dc_date_label.place(x=30, y=120)
        self.dc_date_entry = Entry(self.edit_window, width=15)
        self.dc_date_entry.place(x=160, y=120)
        dc_waste_label = Label(self.edit_window, text="Waste Type")
        dc_waste_label.place(x=30, y=160)
        self.dc_waste_entry = Entry(self.edit_window, width=15)
        self.dc_waste_entry.place(x=160, y=160)
        dc_input_label = Label(self.edit_window, text="Input")
        dc_input_label.place(x=30, y=200)
        self.dc_input_entry = Entry(self.edit_window, width=15)
        self.dc_input_entry.place(x=160, y=200)
        dc_output_label = Label(self.edit_window, text="Output")
        dc_output_label.place(x=30, y=240)
        self.dc_output_entry = Entry(self.edit_window, width=15)
        self.dc_output_entry.place(x=160, y=240)
        dc_container_label = Label(self.edit_window, text="Container")
        dc_container_label.place(x=30, y=280)
        self.dc_container_entry = Entry(self.edit_window, width=15)
        self.dc_container_entry.place(x=160, y=280)
        dc_section_label = Label(self.edit_window, text="Section")
        dc_section_label.place(x=30, y=320)
        self.dc_section_entry = Entry(self.edit_window, width=15)
        self.dc_section_entry.place(x=160, y=320)
        dc_monitor_label = Label(self.edit_window, text="Monitored by")
        dc_monitor_label.place(x=30, y=360)
        self.dc_monitor_entry = Entry(self.edit_window, width=15)
        self.dc_monitor_entry.place(x=160, y=360)

        self.dc_id_entry.insert(0, self.value[0])
        self.dc_date_entry.insert(0, self.value[1])  # default column 2 value
        self.dc_waste_entry.insert(0, self.value[2])
        self.dc_input_entry.insert(0, self.value[3])
        self.dc_output_entry.insert(0, self.value[4])
        self.dc_container_entry.insert(0, self.value[6])
        self.dc_section_entry.insert(0, self.value[7])
        self.dc_monitor_entry.insert(0, self.value[8])

        update_treeview_btn = Button(self.edit_window, text="Update", width=8, borderwidth=1,
                                     command=self.update_hazardous_treeview)
        update_treeview_btn.place(x=30, y=20)

    def menu_event(self, e):
        """Menu widget will popup after mouse right click"""
        self.entry_index = self.listbox.focus()
        item = self.listbox.selection()
        if "" == self.entry_index: return
        # popup menu
        self.menu_click.tk_popup(e.x_root, e.y_root)

    def update_hazardous_treeview(self):
        """ Methods for updating treeview entries by clicking update button"""
        date_entry = self.dc_date_entry.get()
        waste_entry = self.dc_waste_entry.get()
        input_entry = self.dc_input_entry.get()
        output_entry = self.dc_output_entry.get()
        container_entry = self.dc_container_entry.get()
        section_entry = self.dc_section_entry.get()
        monitor_entry = self.dc_monitor_entry.get()
        id_entry = self.dc_id_entry.get()

        try:
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
            cur = mydb.cursor()
            query_update = """UPDATE hazardous SET 
                                `Date` = %s, 
                                `Waste Type` = %s, 
                                `Volume Input` = %s, 
                                `Volume Output` = %s, 
                                `Type of Container` = %s, 
                                `Section` = %s, 
                                `Monitored By` = %s WHERE `id` = %s ;  """

            value = (date_entry, waste_entry, input_entry, output_entry, container_entry, section_entry,
                     monitor_entry, id_entry)
            cur.execute(query_update, value)
            mydb.commit()
            mydb.close()
        except Exception as e:
            print(e)

            # update treeview table
        try:
            mydb = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password="Piquero17",
                                           database="my_database")
            cur = mydb.cursor()
            cur.execute('SELECT `id`, `Date`,`Waste Type`, `Volume Input`, `Volume Output`, `Volume Balance`,'
                        '`Type of Container`, `Section`, `Monitored By` FROM hazardous')
            # fetch data at the mysql
            self.listbox.delete(*self.listbox.get_children())
            mysql_data = cur.fetchall()
            for row in mysql_data:
                self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4],
                                                     row[5], row[6], row[7], row[8]))
            mydb.commit()
            mydb.close()
        except Exception as e:
            print(e)

        self.edit_window.destroy()

    def delete_haz_treeview(self):
        pass

    def exit_menu(self):
        pass

    def filter_haz_treeview(self):
        pass

    def cancel(self):
        self.new.destroy()

    def convert_excel(self, mysql_data):
        with open('inventory.csv', 'a', newline='') as f:
            w = csv.writer(f, dialect="excel")
            for record in mysql_data:
                w.writerow(record)


class HazPullout(tk.Frame):
    """ Module for hazardous waste pullouts """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BLUE)
        self.controller = controller
        self.btn_main = tk.LabelFrame(self, text="Pullout", bg=LIGHT_BLUE)
        self.btn_main.place(x=0, y=0, width=160, height=730)
        # create btn
        back_btn = Button(self.btn_main, text="Back", width=15, bg=BLUE, borderwidth=0,
                          command=lambda: DataBase.show_frame(controller, "MainPage"))
        back_btn.place(x=10, y=50)
        pull_add_item= Button(self.btn_main, text='New Entry', bg=BLUE, width=15, borderwidth=0,
                              command=self.top_pullout)
        pull_add_item.place(x=10, y=100)
        excel_button = Button(self.btn_main, text="Export", bg=BLUE, width=15, borderwidth=0,
                              command=self.convert_excel)
        excel_button.place(x=10, y=150)

        self.pullout_tree_frame = Frame(self, bg=LIGHT_BLUE)
        self.pullout_btn_frame = Frame(self, bg=LIGHT_BLUE)
        self.pullout_tree_frame.place(x=160, y=50, width=1300, height=630)
        self.pullout_btn_frame.place(x=160, y=0, width=1300, height=50)

        # scroll bar for treeview

        self.filter_entry = Entry(self.pullout_btn_frame, width=20)
        self.filter_entry.place(x=950, y=10, height=30)
        pull_filter_btn = Button(self.pullout_btn_frame, text="Filter", bg=BLUE, width=5,
                                 command=self.pullout_filter)
        pull_filter_btn.place(x=1125, y=10)

        # create treeview
        columns = ("Date of Collection", "Name of Transporter", "Name of Treater", "Name of Hazardous Waste",
                   "Type of Hazardous Waste", "Weight Solid (kg)", "Volume Liquid (L)", "Date COT Received")
        self.listbox = ttk.Treeview(self.pullout_tree_frame, columns=columns, show="headings")
        for col in columns:
            self.listbox.heading(col, text=col)
            self.listbox.pack(fill="both", expand=True)
            self.listbox.column(col, stretch=True, anchor=CENTER, width=205)

        # connect python to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        cur = mydb.cursor()
        # update treeview table
        cur.execute("SELECT `Date of Collection`,`Name of Transporter`, `Name of Treater`, `Name of Hazardous Waste`,"
                    "`Type of Hazardous Waste`,`Weight Solid (kg)`,`Volume Liquid (L)`,`Date COT Received` FROM pullout")
        # fetch data at the mysql
        self.listbox.delete(*self.listbox.get_children())
        sql_data = cur.fetchall()
        for row in sql_data:
            self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        mydb.commit()
        mydb.close()
        # create module for where to input data

    def top_pullout(self):
        """Toplevel window method for pullout data"""
        self.add_pullout = Toplevel(self)
        self.add_pullout.geometry("370x400")
        self.add_pullout.title("Add Pullout")
        # create buttons, labels and entries
        self.transporter_label = Label(self.add_pullout, text="Transpoter")
        self.treater_label = Label(self.add_pullout, text="Treater")
        self.weight_label = Label(self.add_pullout, text="Weight/Volume")
        self.wastetype_label = Label(self.add_pullout, text="HazWaste Name")
        self.date_label = Label(self.add_pullout, text="Pullout Date")
        self.transporter_label.grid(row=0, column=0)
        self.treater_label.grid(row=1, column=0)
        self.weight_label.grid(row=2, column=0)
        self.wastetype_label.grid(row=3, column=0)
        self.date_label.grid(row=4, column=0)

        self.transporter_entry = Entry(self.add_pullout, width=25)
        self.treater_entry = Entry(self.add_pullout, width=25)
        self.weight_entry = Entry(self.add_pullout, width=25)
        self.wastetype_entry = Entry(self.add_pullout, width=25)
        self.date_entry = DateEntry(self.add_pullout, width=20, selectmode="day", year=2022, month=4, day=7)
        self.transporter_entry.grid(row=0, column=1)
        self.treater_entry.grid(row=1, column=1)
        self.weight_entry.grid(row=2, column=1)
        self.wastetype_entry.grid(row=3, column=1)
        self.date_entry.grid(row=4, column=1)

        self.pullout_confirm_btn = Button(self.add_pullout, text="Confirm", width=8, command=self.add_to_waste_pullout)
        self.pullout_cancel_btn = Button(self.add_pullout, text="Cancel", width=8)
        self.pullout_confirm_btn.place(x=80, y=150)
        self.pullout_cancel_btn.place(x=200, y=150)

    def add_to_waste_pullout(self):
        """Method for fetching the entries input by the user into the mysql pullout database"""
        # get the data from toplevel widgets
        input_transporter = self.transporter_entry.get()
        input_treater = self.treater_entry.get()
        input_weight = self.weight_entry.get()
        input_waste_type = self.wastetype_entry.get()
        input_calendar = self.date_entry.get()
        # connect python to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        cur = mydb.cursor()
        # insert data at mysql workbench
        sql = "INSERT INTO pullout(`Date of Collection`, `Name of Transporter`,`Name of Treater`," \
              "`Name of Hazardous Waste`,`Volume Liquid (L)`) values(%s,%s, %s, %s, %s)"
        pullout_val = (input_calendar, input_transporter, input_treater, input_waste_type, input_weight)
        cur.execute(sql, pullout_val)
        # update treeview table
        cur.execute("SELECT `Date of Collection`,`Name of Transporter`, `Name of Treater`, `Name of Hazardous Waste`,"
                    "`Type of Hazardous Waste`,`Weight Solid (kg)`,`Volume Liquid (L)`,"
                    "`Date COT Received` FROM pullout")
        # fetch data at the mysql
        self.listbox.delete(*self.listbox.get_children())
        sql_data = cur.fetchall()
        for row in sql_data:
            self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        mydb.commit()
        mydb.close()

    def pullout_filter(self):
        """ Method for filtering the entries at waste pullout module"""
        # get the data at entry
        query = self.filter_entry.get()
        # delete treeview data
        for rec in self.listbox.get_children():
            self.listbox.delete(rec)
        # connect python to mysql
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        # initialize the database
        cur = mydb.cursor()
        data_sql = "SELECT * FROM hazardous WHERE (`Date of Collection` LIKE '%s') OR (`Name of Transporter` LIKE'%s')"\
                   "OR (`Name of Treater` LIKE '%s') OR (`Name of Hazardous Waste` LIKE '%s)" \
                   "OR (`Date COT Received` LIKE'%s'); "
        cur.execute(data_sql % (query, query, query, query, query))

    def convert_excel(self):
        pass


class ComChecklist(tk.Frame):
    """ Module for compliance checklist"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BLUE)
        self.controller = controller
        # buttons at main button frame
        self.btn_main = Frame(self, bg=LIGHT_BLUE)
        self.btn_main.place(x=0, y=100, width=160, height=630)
        # create btn
        back_btn = Button(self.btn_main, text="Back", width=15, bg=BLUE, borderwidth=0,
                          command=lambda: DataBase.show_frame(controller, "MainPage"))
        back_btn.place(x=10, y=10)
        self.legal_checklist = Button(self.btn_main, text="Legal Permits", width=15, bg=BLUE, borderwidth=0,
                                 command=self.legal_checklist_widgets)
        self.legal_checklist.place(x=10, y=50)
        self.supplier_checklist = Button(self.btn_main, text="Supplier", width=15, bg=BLUE, borderwidth=0,
                                command=self.supplier_checklist_widgets)
        self.supplier_checklist.place(x=10, y=90)

        try:
            mydb = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password="Piquero17",
                                           database="my_database")
            cur = mydb.cursor()
        except Exception as e:
            print(e)

    def legal_checklist_widgets(self):
        # delete previous widgets

        # frame for checklist
        self.tree_frame = Frame(self)
        self.tree_frame.place(x=160, y=70, width=1300, height=680)
        self.check_btn_frame = Frame(self, bg=LIGHT_BLUE)
        self.check_btn_frame.place(x=160, y=0, width=1300, height=70)

        # create a combobox for checklist
        year_label = Label(self.check_btn_frame, text="Year", bg=LIGHT_BLUE)
        year_label.place(x=0, y=10)
        n = tk.StringVar()
        self.selected_year = ttk.Combobox(self.check_btn_frame, width=50, textvariable=n)
        # add combobox drop down list
        self.selected_year["values"] = ("2022", "2023", "2024", "2025")
        self.selected_year.place(x=150, y=10)
        self.selected_year.current(0)
        self.selected_year.bind("<<ComboboxSelected>>", self.click_checklist_combobox_dropdown)

    def supplier_checklist_widgets(self):
        # delete previous widgets
        self.check_btn_frame.destroy(), self.selected_year.destroy()
        # create combobox for supplier
        self.supplier_btn_frame = Frame(self, bg=LIGHT_BLUE)
        self.supplier_btn_frame.place(x=160, y=0, width=1300, height=70)
        supplier_label = Label(self.supplier_btn_frame, text="Supplier Permit", bg=LIGHT_BLUE)
        supplier_label.place(x=0, y=10)
        sup_name = tk.StringVar()
        self.supplier_cat = ttk.Combobox(self.supplier_btn_frame, width=50, textvariable=sup_name)
        self.supplier_cat["values"] = ("DENR", "PDEA", "PNP", "OTHERS")
        self.supplier_cat.place(x=150, y=10)
        self.supplier_cat.current(0)
        self.supplier_cat.bind("<<ComboboxSelected>>", self.click_supplier_combobox_dropdown)

    def click_checklist_combobox_dropdown(self, event):
        """Method functions for checklist combobox. Popup treeview widget once user selected. """
        if self.selected_year.get() == "2022":
            # delete previous shown widgets

            # create treeview
            columns = ("id", "Process Items", "RRDS Reference", "Certificates/License/Reports", "Monitoring Method",
                       "Required Documents", "Frequency", "Acquired Date", "Expired Date", "Required Submission Date",
                       "Actual Date Applied", "Responsible Person", "Remarks")

            self.check_tree_canvas = tk.Canvas(self.tree_frame)
            self.check_tree_canvas.place(x=0, y=0, width=1200, height=630)
            self.listbox = ttk.Treeview(self.check_tree_canvas, columns=columns, show="headings")
            treeview_scrollbar = Scrollbar(self.check_tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)
            for col in columns:
                self.listbox.heading(col, text=col)
                self.listbox.pack(fill='both', expand=True)
                self.listbox.column(col, stretch=True, anchor=CENTER, width=150)
                self.listbox.config(xscrollcommand=treeview_scrollbar.set)
            # create scrollbar for treeview widget
            treeview_scrollbar = Scrollbar(self.check_tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)
            treeview_scrollbar.place(x=0, y=608, width=1200)

            try:
                mydb = mysql.connector.connect(host="localhost",
                                               user="root",
                                               password="Piquero17",
                                               database="my_database")
                cur = mydb.cursor()

                cur.execute("SELECT `id`,`Process Items`,`RRDS Reference`,`Certificates/License/Reports`,"
                            "`Monitoring Method`,`Required Documents`, `Frequency`, `Acquired Date`,`Expired Date`,"
                            "`Required Submission Date`,`Actual Date Applied`,`Responsible Person`,"
                            "`Remarks` FROM checklist")
                # fetch data at the mysql
                self.listbox.delete(*self.listbox.get_children())
                sql_data = cur.fetchall()
                for row in sql_data:
                    self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                         row[8], row[9], row[10], row[11], row[12]))
                mydb.commit()
                mydb.close()
            except Exception as e:
                messagebox.showerror(message=f"{e}")
            # show menu widget upon right
            self.treeview_checklist_right_click()

    def return_back_btn_frame(self):
        """Function for deleting btn frame widgets."""
        self.supplier_frame.destroy()
        self.check_btn_frame_widgets()

    def click_supplier_combobox_dropdown(self, event):
        """Method for supplier category combobox dropdown. A treeview widget will popup once item is selected"""
        if self.supplier_cat.get() == "DENR":
            # delete previous shown widgets
            self.check_tree_canvas.destroy()
            # show initial widgets
            self.click_supplier_combobox_dropdown_initial_widgets()
            # create treeview widgets
            columns = ("Supplier Name", "Address", "Contract", "ECC", "TSD", "TRC", "PTO", "DP", "Others", "Remarks")
            self.supplier_tree_canvas = tk.Canvas(self)
            self.denr_tree_canvas.place(x=160, y=10, width=1200, height=340)
            self.listbox = ttk.Treeview(self.supplier_tree_canvas, columns=columns, show="headings")
            treeview_scrollbar = Scrollbar(self.supplier_tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)

            self.listbox.column("# 1", stretch=NO, anchor=CENTER, width=250)
            self.listbox.column("# 2", stretch=NO, anchor=CENTER, width=250)
            self.listbox.column("# 3", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 4", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 5", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 6", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 7", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 8", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 9", stretch=NO, anchor=CENTER, width=120)
            self.listbox.column("# 10", stretch=NO, anchor=CENTER, width=250)

            for col in columns:
                self.listbox.heading(col, text=col)
                self.listbox.pack(fill='both', expand=True)
                self.listbox.config(xscrollcommand=treeview_scrollbar.set)
            # create scrollbar for treeview widget
            treeview_scrollbar = Scrollbar(tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)
            treeview_scrollbar.place(x=3, y=377, width=1194)

        elif self.supplier_cat.get() == "PDEA":
            # delete previous shown widget
            self.check_tree_canvas.destroy()
            self.click_supplier_combobox_dropdown_initial_widgets()
            # create treeview widget
            columns = ("Supplier Name", "Address", "Certificate", "Validity", "Remarks")
            self.supplier_tree_canvas = tk.Canvas(self)
            self.pdea_tree_canvas.place(x=160, y=50, width=1200, height=630)
            self.listbox = ttk.Treeview(self.supplier_tree_canvas, columns=columns, show="headings")

            self.listbox.column("# 1", stretch=NO, anchor=CENTER, width=280)
            self.listbox.column("# 2", stretch=NO, anchor=CENTER, width=280)
            self.listbox.column("# 3", stretch=NO, anchor=CENTER, width=150)
            self.listbox.column("# 4", stretch=NO, anchor=CENTER, width=150)
            self.listbox.column("# 5", stretch=NO, anchor=CENTER, width=280)
            for col in columns:
                self.listbox.heading(col, text=col)
                self.listbox.pack(fill='both', expand=True)

    def click_supplier_combobox_dropdown_initial_widgets(self):
        # delete frames from main btn
        self.check_btn_frame.destroy()

        # create supplier frame and buttons
        self.supplier_frame = Frame(self, bg=LIGHT_BLUE)
        self.supplier_frame.place(x=0, y=0, width=158, height=730)
        supplier_back_btn = Button(self.supplier_frame, text="Back", width=15, bg=BLUE, borderwidth=0,
                                   command=self.return_back_btn_frame)
        supplier_back_btn.place(x=10, y=50)
        supplier_add_btn = Button(self.supplier_frame, text="New Entry", width=15, bg=BLUE, borderwidth=0,
                                  command=self.supplier_add_window)
        supplier_add_btn.place(x=10, y=100)

    def supplier_add_window(self):
        supplier_add_frame = LabelFrame(self, text="New Entry")
        supplier_add_frame.place(x=160, y=350, width=1200, height=420)
        supplier_name_label = Label(supplier_add_frame, text="Supplier Name")
        supplier_name_label.place(x=50, y=60)
        supplier_name_entry = Entry(supplier_add_frame, width=25)
        supplier_name_entry.place(x=200, y=60)
        supplier_address_label = Label(supplier_add_frame, text="Address")
        supplier_address_label.place(x=50, y=100)
        supplier_address_entry = Entry(supplier_add_frame, width=25)
        supplier_address_entry.place(x=200, y=100)
        supplier_contract_label = Label(supplier_add_frame, text="Contract")
        supplier_contract_label.place(x=50, y=140)
        supplier_contract_entry = Entry(supplier_add_frame, width=25)
        supplier_contract_entry.place(x=200, y=140)
        supplier_remarks_label = Label(supplier_add_frame, text="Remarks")
        supplier_remarks_label.place(x=50, y=180)
        supplier_remarks_entry = Entry(supplier_add_frame, width=25)
        supplier_remarks_entry.place(x=200, y=180)
        dp_label = Label(supplier_add_frame, text="DP")
        dp_label.place(x=50, y=220)
        dp_entry = Entry(supplier_add_frame, width=20)
        dp_entry.place(x=200, y=220)
        supplier_remarks_entry = Entry(supplier_add_frame, width=25)
        supplier_remarks_entry.place(x=200, y=220)

        ecc_label = Label(supplier_add_frame, text="ECC")
        ecc_label.place(x=450, y=60)
        ecc_entry = Entry(supplier_add_frame, width=20)
        ecc_entry.place(x=550, y=60)
        tsd_label = Label(supplier_add_frame, text="TSD")
        tsd_label.place(x=450, y=100)
        tsd_entry = Entry(supplier_add_frame, width=20)
        tsd_entry.place(x=550, y=100)
        trc_label = Label(supplier_add_frame, text="TRC")
        trc_label.place(x=450, y=140)
        trc_entry = Entry(supplier_add_frame,width=20)
        trc_entry.place(x=550, y=140)
        pto_label = Label(supplier_add_frame, text="PTO")
        pto_label.place(x=450, y=180)
        pto_entry = Entry(supplier_add_frame, width=20)
        pto_entry.place(x=550, y=180)
        others_label = Label(supplier_add_frame,text="Others")
        others_label.place(x=450, y=220)
        others_entry = Entry(supplier_add_frame, width=20)
        others_entry.place(x=550, y=220)

        acquired_date_label = Label(supplier_add_frame, text="Acquired Date")
        acquired_date_label.place(x=750, y=10)
        expiry_date_label = Label(supplier_add_frame, text="Expiry Date")
        expiry_date_label.place(x=850, y=10)




        # add ID column at mysql db with auto increment primary key
        # try:
        #    mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
        #    cur = mydb.cursor()
        #    cur.execute("ALTER TABLE checklist ADD id INT PRIMARY KEY AUTO_INCREMENT;")
        #    mydb.commit()
        #    mydb.close()
        # except Exception as e:
        #    print(e)

    def toplevel_add_to_checklist(self):
        """Toplevel method for Compliance Checklist where user input their entries"""
        self.toplevel_checklist = tk.Toplevel(self)
        self.toplevel_checklist.title("Add Information!")
        self.toplevel_checklist.geometry("700x400")
        self.toplevel_checklist.resizable(False, False)
        toplevel_frame = Frame(self.toplevel_checklist)
        toplevel_frame.pack()
        # create canvas for scroll bar
        canvas = Canvas(toplevel_frame, width=700, height=800, scrollregion=(0, 0, 700, 800))
        # create scroll bar
        y_scroll_bar = Scrollbar(toplevel_frame, orient=VERTICAL)
        y_scroll_bar.pack(side=RIGHT, fill=Y)
        y_scroll_bar.config(command=canvas.yview)
        # configure the canvas
        canvas.config(yscrollcommand=y_scroll_bar.set)
        canvas.pack(fill=BOTH, expand=True)

        process_label = Label(canvas, text="Process Item")
        canvas.create_window(100, 50, window=process_label)
        rrds_label = Label(canvas, text="RRDS Reference")
        canvas.create_window(100, 110, window=rrds_label)
        cert_label = Label(canvas, text="Certificate")
        canvas.create_window(100, 170, window=cert_label)
        method_label = Label(canvas, text="Mon. Method")
        canvas.create_window(100, 230, window=method_label)
        document_label = Label(canvas, text="Req. Document")
        canvas.create_window(100, 290, window=document_label)
        aq_date_label = Label(canvas, text="Acquired Date")
        canvas.create_window(100, 350, window=aq_date_label)
        ex_date_label = Label(canvas, text="Expired Date")
        canvas.create_window(400, 350, window=ex_date_label)
        req_date_label = Label(canvas, text="Submission Date")
        canvas.create_window(100, 410, window=req_date_label)
        actual_date_label = Label(canvas, text="Date Applied")
        canvas.create_window(400, 410, window=actual_date_label)
        frequency_label = Label(canvas, text="Frequency")
        canvas.create_window(100, 470, window=frequency_label)
        res_person_label = Label(canvas, text=" Responsible Person")
        canvas.create_window(100, 530, window=res_person_label)
        remarks_label = Label(canvas, text="Remarks")
        canvas.create_window(100, 590, window=remarks_label)

        self.process_txt = Text(canvas, width=40)
        canvas.create_window(400, 50, window=self.process_txt, height=45)
        self.rrds_txt = Text(canvas, width=40)
        canvas.create_window(400, 110, window=self.rrds_txt, height=45)
        self.cert_txt = Text(canvas, width=40)
        canvas.create_window(400, 170, window=self.cert_txt, height=45)
        self.method_txt = Text(canvas, width=40)
        canvas.create_window(400, 230, window=self.method_txt, height=45)
        self.document_txt = Text(canvas, width=40)
        canvas.create_window(400, 290, window=self.document_txt, height=45)

        self.aq_date_entry = DateEntry(canvas, width=12)
        self.aq_date_entry.delete(0, END)
        canvas.create_window(260, 350, window=self.aq_date_entry)
        self.ex_date_entry = DateEntry(canvas, width=12)
        self.ex_date_entry.delete(0, END)
        canvas.create_window(520, 350, window=self.ex_date_entry)
        self.req_date_entry = DateEntry(canvas, width=12)
        self.req_date_entry.delete(0, END)
        canvas.create_window(260, 410, window=self.req_date_entry)
        self.act_date_entry = DateEntry(canvas, width=12)
        self.act_date_entry.delete(0, END)
        canvas.create_window(520, 410, window=self.act_date_entry)
        self.frequency_txt = Text(canvas, width=40)
        canvas.create_window(400, 470, window=self.frequency_txt, height=25)
        self.res_person_txt = Text(canvas, width=40)
        canvas.create_window(400, 530, window=self.res_person_txt, height=25)
        self.remarks_txt = Text(canvas, width=40)
        canvas.create_window(400, 590, window=self.remarks_txt, height=45)
        # buttons
        confirm_btn = Button(canvas, text="Confirm", width=10, command=self.save_to_checklist_database)
        canvas.create_window(80, 750, window=confirm_btn)
        cancel_btn = Button(canvas, text="Cancel", width=10, command=self.cancel_to_checklist_database)
        canvas.create_window(180, 750, window=cancel_btn)

    def save_to_checklist_database(self):
        """ Method for saving entries into mysql database"""
        # fetch the data from entries
        process = self.process_txt.get("1.0", END)
        rrds = self.rrds_txt.get("1.0", END)
        certificate = self.cert_txt.get("1.0", END)
        method = self.method_txt.get("1.0", END)
        document = self.document_txt.get("1.0", END)
        res_person = self.res_person_txt.get("1.0", END)
        remarks = self.remarks_txt.get("1.0", END)
        frequency = self.frequency_txt.get("1.0", END)
        acquired_date = self.aq_date_entry.get()
        expired_date = self.ex_date_entry.get()
        required_date = self.req_date_entry.get()
        actual_date = self.act_date_entry.get()

        try:
            mydb = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password="Piquero17",
                                           database="my_database")
            cur = mydb.cursor()
            sql_data_checklist = "INSERT INTO checklist(`Process Items`,`RRDS Reference`," \
                                 "`Certificates/License/Reports`,`Monitoring Method`, `Required Documents`, " \
                                 "`Frequency`, `Acquired Date`,`Expired Date`,`Required Submission Date`, " \
                                 "`Actual Date Applied`,`Responsible Person`,`Remarks`) " \
                                 "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            checklist_val = (process, rrds, certificate, method, document, frequency, res_person, remarks,
                             acquired_date, expired_date, required_date, actual_date)
            cur.execute(sql_data_checklist, checklist_val)
            mydb.commit()
            mydb.close()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"{e}")

        # fetch data from mysql every entry
        try:
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
            cur = mydb.cursor()
            cur.execute(" SELECT `id`,`Process Items`,`RRDS Reference`,`Certificates/License/Reports`,"
                        "`Monitoring Method`, `Required Documents`, `Frequency`, `Acquired Date`,`Expired Date`,"
                        "`Required Submission Date`, `Actual Date Applied`,`Responsible Person`,`Remarks`"
                        "FROM checklist")
            self.listbox.delete(*self.listbox.get_children())
            sql_data = cur.fetchall()
            for row in sql_data:
                self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                     row[8], row[9], row[10], row[11], row[12]))

        except Exception as e:
            messagebox.showerror(title="Error", message=f"{e}")

        # close the toplevel after click confirm button
        self.toplevel_checklist.destroy()

    def cancel_to_checklist_database(self):
        """Method function to cancel entry"""
        self.toplevel_checklist.destroy()

    def treeview_checklist_right_click(self):
        """ Method function where menu widget will popup after right-click on the selected row at treeview
            widget table"""
        self.menu_checklist_click = Menu(self, tearoff=False)
        self.menu_checklist_click.add_command(label="Edit", command=self.edit_checklist_treeview)
        self.menu_checklist_click.add_command(label="Delete", command=self.delete_checklist_treeview)
        self.menu_checklist_click.add_command(label="Filter", command=self.filter_checklist_treeview)
        self.menu_checklist_click.add_separator()
        self.menu_checklist_click.add_command(label="Exit", command=self.exit_checklist_menu)

        self.listbox.bind("<Button-3>", self.menu_checklist_event)

    def menu_checklist_event(self, e):
        """Method functions events after clicking right click"""
        self.entry_index = self.listbox.focus()
        self.listbox.selection()
        if "" == self.entry_index: return
        # popup menu
        self.menu_checklist_click.tk_popup(e.x_root, e.y_root)

    def edit_checklist_treeview(self):
        self.toplevel_checklist = Toplevel(self)
        self.toplevel_checklist.title("Edit Information!")
        self.toplevel_checklist.geometry("700x550")
        toplevel_frame = Frame(self.toplevel_checklist)
        toplevel_frame.pack()
        # create canvas for scroll bar
        canvas = Canvas(toplevel_frame, width=700, height=800, scrollregion=(0, 0, 700, 800))
        # create scroll bar
        y_scroll_bar = Scrollbar(toplevel_frame, orient=VERTICAL)
        y_scroll_bar.pack(side=RIGHT, fill=Y)
        y_scroll_bar.config(command=canvas.yview)
        # configure the canvas
        canvas.config(yscrollcommand=y_scroll_bar.set)
        canvas.pack(fill=BOTH, expand=True)

        id_label = Label(canvas, text="ID")
        canvas.create_window(100, 50, window=id_label)
        process_label = Label(canvas, text="Process Item")
        canvas.create_window(100, 100, window=process_label)
        rrds_label = Label(canvas, text="RRDS Reference")
        canvas.create_window(100, 170, window=rrds_label)
        cert_label = Label(canvas, text="Certificate")
        canvas.create_window(100, 230, window=cert_label)
        method_label = Label(canvas, text="Mon. Method")
        canvas.create_window(100, 290, window=method_label)
        document_label = Label(canvas, text="Req. Document")
        canvas.create_window(100, 350, window=document_label)
        aq_date_label = Label(canvas, text="Acquired Date")
        canvas.create_window(100, 410, window=aq_date_label)
        ex_date_label = Label(canvas, text="Expired Date")
        canvas.create_window(400, 410, window=ex_date_label)
        req_date_label = Label(canvas, text="Submission Date")
        canvas.create_window(100, 470, window=req_date_label)
        actual_date_label = Label(canvas, text="Date Applied")
        canvas.create_window(400, 470, window=actual_date_label)
        frequency_label = Label(canvas, text="Frequency")
        canvas.create_window(100, 530, window=frequency_label)
        res_person_label = Label(canvas, text=" Responsible Person")
        canvas.create_window(100, 590, window=res_person_label)
        remarks_label = Label(canvas, text="Remarks")
        canvas.create_window(100, 650, window=remarks_label)

        self.id_text = Text(canvas, width=10, font="Calibre,7")
        canvas.create_window(260, 50, window=self.id_text, height=25)
        self.process_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 110, window=self.process_txt, height=45)
        self.rrds_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 170, window=self.rrds_txt, height=45)
        self.cert_txt = Text(canvas, width=40,font="Calibre,7")
        canvas.create_window(400, 230, window=self.cert_txt, height=45)
        self.method_txt = Text(canvas, width=40,font="Calibre,7")
        canvas.create_window(400, 290, window=self.method_txt, height=45)
        self.document_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 350, window=self.document_txt, height=45)

        self.aq_date_entry = DateEntry(canvas, width=12, font="Calibre,7")
        self.aq_date_entry.delete(0, END)
        canvas.create_window(260, 410, window=self.aq_date_entry)
        self.ex_date_entry = DateEntry(canvas, width=12, font="Calibre,7")
        self.ex_date_entry.delete(0, END)
        canvas.create_window(520, 410, window=self.ex_date_entry)
        self.req_date_entry = DateEntry(canvas, width=12, font="Calibre,7")
        self.req_date_entry.delete(0, END)
        canvas.create_window(260, 470, window=self.req_date_entry)
        self.act_date_entry = DateEntry(canvas, width=12,font="Calibre,7")
        self.act_date_entry.delete(0, END)
        canvas.create_window(520, 470, window=self.act_date_entry)
        self.frequency_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 530, window=self.frequency_txt, height=25)
        self.res_person_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 590, window=self.res_person_txt, height=25)
        self.remarks_txt = Text(canvas, width=40, font="Calibre,7")
        canvas.create_window(400, 650, window=self.remarks_txt, height=45)
        # buttons
        update_checklist_btn = Button(canvas, text="Update", width=10, command=self.update_edited_to_checklist_database)
        canvas.create_window(150, 750, window=update_checklist_btn)
        # insert data to the toplevel menu entries
        # grab entry values from treeview
        for child in self.listbox.get_children():
            if child == self.entry_index:
                self.value = self.listbox.item(child)["values"]

        self.id_text.insert("1.0", self.value[0])
        self.process_txt.insert("1.0", self.value[1])
        self.rrds_txt.insert("1.0", self.value[2])
        self.cert_txt.insert("1.0", self.value[3])
        self.method_txt.insert("1.0", self.value[4])
        self.document_txt.insert("1.0", self.value[5])
        self.frequency_txt.insert("1.0", self.value[6])
        self.aq_date_entry.insert(0, self.value[7])
        self.ex_date_entry.insert(0, self.value[8])
        self.req_date_entry.insert(0, self.value[9])
        self.act_date_entry.insert(0, self.value[10])
        self.res_person_txt.insert("1.0", self.value[11])
        self.remarks_txt.insert("1.0", self.value[12])

    def update_edited_to_checklist_database(self):
        # fetch the data from entries
        process = self.process_txt.get("1.0", END)
        rrds = self.rrds_txt.get("1.0", END)
        certificate = self.cert_txt.get("1.0", END)
        method = self.method_txt.get("1.0", END)
        document = self.document_txt.get("1.0", END)
        frequency = self.frequency_txt.get("1.0", END)
        acquired_date = self.aq_date_entry.get()
        expired_date = self.ex_date_entry.get()
        required_date = self.req_date_entry.get()
        actual_date = self.act_date_entry.get()
        res_person = self.res_person_txt.get("1.0", END)
        remarks = self.remarks_txt.get("1.0", END)
        id = self.id_text.get("1.0", END)

        try:
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piquero17", database="my_database")
            cur = mydb.cursor()
            query_update = """UPDATE checklist SET
                                        `Process Items` = %s,
                                        `RRDS Reference` = %s,
                                        `Certificates/License/Reports`= %s,
                                        `Monitoring Method`= %s,
                                        `Required Documents`= %s,
                                        `Frequency`= %s,
                                        `Acquired Date` = %s,
                                        `Expired Date` = %s,
                                        `Required Submission Date` = %s, 
                                        `Actual Date Applied` = %s,
                                        `Responsible Person` =%s,
                                        `Remarks` = %s WHERE  `id` = %s ;  """
            value = (process, rrds, certificate, method, document, res_person, remarks, frequency, acquired_date,
                     expired_date, required_date, actual_date, id)
            cur.execute(query_update, value)
            mydb.commit()
            mydb.close()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"{e}")

        # update treeview table by fetching data from mysql database
        try:
            mydb = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password="Piquero17",
                                           database="my_database")
            cur = mydb.cursor()
            cur.execute('SELECT `id`, `Process Items`,  `RRDS Reference`, `Certificates/License/Reports`,'
                        '`Monitoring Method`, `Required Documents`, `Frequency`,`Acquired Date`,`Expired Date`,'
                        ' `Required Submission Date`,`Actual Date Applied`,`Responsible Person`,`Remarks`'
                        ' FROM checklist')
            # fetch data at the mysql
            self.listbox.delete(*self.listbox.get_children())
            mysql_data = cur.fetchall()
            for row in mysql_data:
                self.listbox.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                     row[8], row[9], row[10], row[11], row[12]))
            mydb.commit()
            mydb.close()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"{e}")

        # delete toplevel window
        self.toplevel_checklist.destroy()

    def delete_checklist_treeview(self):
        pass

    def filter_checklist_treeview(self):
        pass

    def exit_checklist_menu(self):
        pass


class ChemicalInventory(tk.Frame):
    """ Module for chemical inventories"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BLUE)
        self.controller = controller
        # buttons at main button frame
        self.btn_main = tk.LabelFrame(self, text="Inventory", bg=LIGHT_BLUE)
        self.btn_main.place(x=0, y=0, width=160, height=730)
        # create btn
        exit_btn = Button(self.btn_main, text="Back", width=15, bg=BLUE, borderwidth=0,
                          command=lambda: DataBase.show_frame(controller, "MainPage"))
        exit_btn.place(x=10, y=55)

        # frame for checklist
        tree_frame = Frame(self)
        tree_frame.place(x=160, y=50, width=1300, height=630)

        # create treeview
        columns = ("id", "Process Items", "RRDS Reference", "Certificates/License/Reports", "Monitoring Method",
                   "Required Documents", "Frequency", "Acquired Date", "Expired Date", "Required Submission Date",
                   "Actual Date Applied", "Responsible Person", "Remarks")

        tree_canvas = tk.Canvas(tree_frame)
        tree_canvas.place(x=0, y=0, width=1200, height=630)
        self.listbox = ttk.Treeview(tree_canvas, columns=columns, show="headings")
        treeview_scrollbar = Scrollbar(tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)
        for col in columns:
            self.listbox.heading(col, text=col)
            self.listbox.pack(fill='both', expand=True)
            self.listbox.column(col, stretch=True, anchor=CENTER, width=150)
            self.listbox.config(xscrollcommand=treeview_scrollbar.set)
        # create scrollbar for treeview widget
        treeview_scrollbar = Scrollbar(tree_canvas, orient=HORIZONTAL, command=self.listbox.xview)
        treeview_scrollbar.place(x=0, y=608, width=1200)


if __name__ == "__main__":
    app = DataBase()
    app.state("zoomed")
    app.mainloop()




