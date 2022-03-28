from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from views import base, student_info
from PIL import ImageTk, Image
from controller import *
from helper import image_to_octet_string, validate_student_id, validate_date

class StudentListFrame(base.ParentFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=TOP, fill="both", expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        super().create_widgets()

        self.attributes_set = ("STT", "Họ và tên", "Mã SV", "Giới tính", "Ngày sinh", "Số tiết vắng")
        self.canvas1.create_text(350, 180, text="Tìm kiếm theo", font=("Arial", 18), fill="black")

        self.variable = StringVar(self.canvas1)
        self.variable.set("Thuộc tính")
        self.attribute_choosen = ttk.Combobox(self.canvas1, textvariable=self.variable, state="readonly", width=11, font=("Arial", 16))
        self.attribute_choosen["values"] = self.attributes_set
        self.attribute_choosen.current()
        self.attribute_choosen.place(x=470, y=165)

        self.value_entry = Entry(self.canvas1, width=20, font=("Arial", 18), highlightbackground="black", highlightthickness=1, borderwidth=0)
        self.value_entry.insert(0, "Nhập giá trị")
        self.value_entry.bind("<Button-1>", self.clear_entry)
        self.value_entry.bind("<Return>", self.search)
        self.value_entry.place(x=670, y=165)

        self.search_button_icon = ImageTk.PhotoImage(Image.open("images/search.png"))
        self.search_button = Button(self.canvas1, image=self.search_button_icon, highlightthickness=0, bd=0, borderwidth=0, command=self.search)
        self.search_button.place(x=990, y=160)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        self.table = ttk.Treeview(self.canvas1, height=15, show="headings", selectmode="browse")
        yscrollbar = ttk.Scrollbar(self.canvas1, orient=VERTICAL, command=self.table.yview)
        yscrollbar.place(x=1163, y=210, height=404)
        self.table["columns"] = self.attributes_set
        self.table.column("STT", minwidth=80, width=80, anchor="center", stretch=NO)
        self.table.column("Họ và tên", minwidth=280, width=280, anchor="center", stretch=NO)
        self.table.column("Mã SV", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Giới tính", minwidth=150, width=150, anchor="center", stretch=NO)
        self.table.column("Ngày sinh", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Số tiết vắng", minwidth=150, width=150, anchor="center", stretch=NO)
        for col in self.table['columns']:
            self.table.heading(col, text=f"{col}", anchor=CENTER)
        self.table.place(x=100, y=210)
        self.insert_data()
        self.table.bind("<Double-1>", self.show_student_info)

        self.add_button = Button(self.canvas1, text="Thêm", width=8, font=("Arial", 14), bg="yellow", fg="black", command=self.open_add_student_window)
        self.add_button.place(x=480, y=630)
        self.modify_button = Button(self.canvas1, text="Sửa", width=8, font=("Arial", 14), bg="yellow", fg="black", command=self.open_modify_student_window)
        self.modify_button.place(x=590, y=630)
        self.delete_button = Button(self.canvas1, text="Xóa", width=8, font=("Arial", 14), bg="yellow", fg="black", command=self.remove_student)
        self.delete_button.place(x=700, y=630)

    def clear_entry(self, event):
        if self.value_entry.get() == "Nhập giá trị":
            self.value_entry.delete(0, END)

    def search(self, event=None):
        attribute = self.attribute_choosen.current()
        value = self.value_entry.get()
        selections = []
        if attribute != -1 and not len(value) == 0:
            for child in self.table.get_children():
                if value.lower() in str(self.table.item(child)['values'][attribute]).lower():
                    selections.append(child)
            self.table.selection_set(selections)

    def insert_data(self):
        student_list = get_sorted_students_list()
        for i in range(len(student_list)):
            self.table.insert("", "end", values=[i+1, student_list[i][1], student_list[i][0], student_list[i][2], student_list[i][3], student_list[i][4]])

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        self.insert_data()

    def selected_student(self):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        return values

    def remove_student(self):
        student = self.selected_student()
        if student:
            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
                delete_student(student[2])
                helper.remove_image_student_from_ImagesStudent_dir(student[2])
                self.refresh_table()
        else:
            messagebox.showinfo("Thông báo", "Chưa chọn sinh viên nào")
        

    def create_new_window(self, title):
        self.new_window = Toplevel(self.master)
        self.new_window.title(title)
        self.new_window.geometry("400x300+500+200")
        self.new_window.resizable(False, False)
        self.new_window.config(bg="#D1D1D1")
        self.new_window.grab_set()
        self.new_window.focus_set()

        self.fullname_label = Label(self.new_window, text="Họ và tên", font=("Arial", 11), bg="#D1D1D1")
        self.fullname_label.place(x=10, y=140)
        self.fullname_entry = Entry(self.new_window, width=20, font=("Arial", 11), highlightbackground="black", highlightthickness=1, borderwidth=0)
        self.fullname_entry.place(x=110, y=140)

        self.id_label = Label(self.new_window, text="Mã sinh viên", font=("Arial", 11), bg="#D1D1D1")
        self.id_label.place(x=10, y=170)
        self.id_entry = Entry(self.new_window, width=20, font=("Arial", 11), highlightbackground="black", highlightthickness=1, borderwidth=0)
        self.id_entry.place(x=110, y=170)

        self.gender_label = Label(self.new_window, text="Giới tính", font=("Arial", 11), bg="#D1D1D1")
        self.gender_label.place(x=10, y=200)
        self.gender_combobox = ttk.Combobox(self.new_window, textvariable="Giới tính", state="readonly", width=18, font=("Arial", 11))
        self.gender_combobox["values"] = ("Nam", "Nữ")
        self.gender_combobox.current()
        self.gender_combobox.place(x=110, y=200)

        self.dob_label = Label(self.new_window, text="Ngày sinh", font=("Arial", 11), bg="#D1D1D1")
        self.dob_label.place(x=10, y=230)
        self.select_dob = DateEntry(self.new_window, width=18, font=("Arial", 11), borderwidth=0, date_pattern="dd/mm/yyyy")
        self.select_dob.delete(0, END)
        self.select_dob.place(x=110, y=230)

        self.absent_count_label = Label(self.new_window, text="Số tiết vắng", font=("Arial", 11), bg="#D1D1D1")
        self.absent_count_label.place(x=10, y=260)
        self.absent_count_entry = Entry(self.new_window, width=20, font=("Arial", 11), highlightbackground="black", highlightthickness=1, borderwidth=0)
        self.absent_count_entry.place(x=110, y=260)

        def pick_image():
            filename = filedialog.askopenfilename(filetypes=(("Image Files", "*.jpg"), ("Image Files", "*.png"), ("Image Files", "*.jpeg"), ("All Files", "*.*")))
            if len(filename) != 0:
                self.image_path_entry.delete(0, END)
                self.image_path_entry.insert(0, filename)

        self.pick_image_button = Button(self.new_window, text="Chọn ảnh", width=8, font=("Arial", 9), bg="#F32463", fg="white", command=pick_image)
        self.pick_image_button.place(x=10, y=110)
        self.image_path_entry = Entry(self.new_window, width=20, font=("Arial", 11), highlightbackground="black", highlightthickness=1, borderwidth=0)
        self.image_path_entry.place(x=110, y=110)

    def open_add_student_window(self):
        self.create_new_window("Thêm sinh viên")
        self.absent_count_entry.insert(0, "0")
        def _add_student():
            fullname = self.fullname_entry.get()
            id = self.id_entry.get()
            gender = self.gender_combobox.get()
            dob = self.select_dob.get()
            absent_count = self.absent_count_entry.get()
            image_path = self.image_path_entry.get()
            if fullname == "" or image_path == "" or id == "" or dob == "" or absent_count == "" or gender == "":
                messagebox.showinfo("Thông báo", "Hãy nhập đầy đủ thông tin")
            elif not validate_student_id(id):
                messagebox.showinfo("Thông báo", "Mã sinh viên không hợp lệ hoặc đã tồn tại")
            elif not validate_date(dob):
                messagebox.showinfo("Thông báo", "Ngày sinh không hợp lệ\nNgày sinh phải có dạng dd/mm/yyyy")
            elif not absent_count.isdigit():
                messagebox.showinfo("Thông báo", "Số tiết vắng phải là số. VD: 2")
            else:
                add_student(int(id), fullname, gender, dob, int(absent_count), image_path)
                update_absent_count(int(id))
                helper.copy_student_image_to_ImagesStudent_dir(id, image_path)
                self.new_window.destroy()
                self.refresh_table()

        add_button = Button(self.new_window, text="Thêm", height=3, width=8, font=("Arial", 11), bg="yellow", fg="black", command=_add_student)
        add_button.place(x=300, y=178)
    
    def open_modify_student_window(self):
        student = self.selected_student()
        if len(student) == 0:
            messagebox.showinfo("Thông báo", "Hãy chọn sinh viên cần sửa")
        else:
            student = get_student(student[2])[0]
            self.create_new_window("Sửa sinh viên")
            self.fullname_entry.insert(0, student[1])
            self.id_entry.insert(0, student[0])
            self.gender_combobox.set(student[2])
            self.select_dob.insert(0, student[3])
            self.absent_count_entry.insert(0, student[4])

            def _modify_student():
                old_id = student[0]
                fullname = self.fullname_entry.get()
                id = self.id_entry.get()
                gender = self.gender_combobox.get()
                dob = self.select_dob.get()
                absent_count = self.absent_count_entry.get()
                image_data = student[5]
                if self.image_path_entry.get() != "":
                    image_path = self.image_path_entry.get()
                    image_data = image_to_octet_string(image_path)
                else:
                    image_path = ""

                if fullname == "" or id == "" or dob == "" or absent_count == "":
                    messagebox.showinfo("Thông báo", "Hãy nhập đầy đủ thông tin")
                elif int(id) != int(old_id) and not validate_student_id(id):
                    messagebox.showinfo("Thông báo", "Mã sinh viên không hợp lệ hoặc đã tồn tại")
                elif not validate_date(dob):
                    messagebox.showinfo("Thông báo", "Ngày sinh không hợp lệ\nNgày sinh phải có dạng dd/mm/yyyy")
                elif not absent_count.isdigit():
                    messagebox.showinfo("Thông báo", "Số tiết vắng phải là số. VD: 2")
                else:
                    update_student(int(old_id), int(id), fullname, gender, dob, int(absent_count), image_data)
                    update_attendance(int(old_id), int(id))
                    helper.update_student_image_in_ImagesStudent_dir(old_id, id, image_path)
                    self.new_window.destroy()
                    self.refresh_table()

            modify_button = Button(self.new_window, text="Sửa", height=3, width=8, font=("Arial", 11), bg="yellow", fg="black", command=_modify_student)
            modify_button.place(x=300, y=178)

    def show_student_info(self, event):
        info = self.selected_student()
        selected_student_id = info[2]
        self.destroy()
        student_info.StudentInfoFrame(self.master, selected_student_id).tkraise()