from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from views import base
from controller import *
from PIL import ImageTk, Image

class LastestAttendance(base.ParentFrame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        super().create_widgets()
        self.lastest_date = get_dates_list()[-1]
        self.attributes_set = ["STT", "Họ và tên", "Mã SV", "Giới tính", "Ngày sinh", "Số tiết vắng", self.lastest_date]

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

        self.yscrollbar = ttk.Scrollbar(self.canvas1, orient=VERTICAL, command=self.table.yview)
        self.yscrollbar.place(x=1163, y=210, height=404)

        self.table["columns"] = self.attributes_set
        self.set_columns()
        self.table.place(x=100, y=210)
        self.insert_data()

        self.late_attendance_button = Button(self.canvas1, text="Điểm danh bù", width=12, font=("Arial", 14), bg="yellow", fg="black", command=self._attendance_late)
        self.late_attendance_button.place(relx=0.4, rely=0.9, anchor=CENTER)

        self.remove_attendance_button = Button(self.canvas1, text="Xóa điểm danh", width=12, font=("Arial", 14), bg="yellow", fg="black", command=self._remove_attendance)
        self.remove_attendance_button.place(relx=0.6, rely=0.9, anchor=CENTER)

    def set_columns(self):
        self.table.column("STT", minwidth=40, width=40, anchor="center", stretch=NO)
        self.table.column("Họ và tên", minwidth=250, width=250, anchor="center", stretch=NO)
        self.table.column("Mã SV", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Giới tính", minwidth=150, width=150, anchor="center", stretch=NO)
        self.table.column("Ngày sinh", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Số tiết vắng", minwidth=150, width=150, anchor="center", stretch=NO)
        self.table.column(self.lastest_date, minwidth=70, width=70, anchor="center", stretch=NO)
        for col in self.table['columns']:
            self.table.heading(col, text=f"{col}", anchor=CENTER)

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
        else:
            return

    def insert_data(self):
        student_list = get_sorted_students_list()
        for i in range(len(student_list)):
            lastest_attendance_std = get_attendance(student_list[i][0])[-1]
            self.table.insert("", "end", values=[i+1, student_list[i][1], student_list[i][0], student_list[i][2], student_list[i][3], student_list[i][4]] + [lastest_attendance_std])

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        self.insert_data()

    def _attendance_late(self):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        try:
            id = values[2]
            if values[6] == 'vắng':
                attendance_late(id, self.lastest_date)
                self.refresh_table()
            else:
                messagebox.showinfo("Thông báo", "Sinh viên đã được điểm danh trước đó")
        except:
            messagebox.showinfo("Thông báo", "Bạn chưa chọn sinh viên nào")

    def _remove_attendance(self):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        try:
            id = values[2]
            if values[6] == 'x':
                remove_attendance(id, self.lastest_date)
                self.refresh_table()
            else:
                messagebox.showinfo("Thông báo", "Sinh viên chưa được điểm danh trước đó")
        except:
            messagebox.showinfo("Thông báo", "Bạn chưa chọn sinh viên nào")
        