from tkinter import *
from tkinter import ttk, filedialog, messagebox
from views import base
from PIL import ImageTk, Image
from controller import *
from helper import export_csv_file, export_xlsx_file

class StatisticalFrame(base.ParentFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=TOP, fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        super().create_widgets()

        self.date_list = get_dates_list()
        atts = ["STT", "Họ và tên", "Mã SV", "Giới tính", "Ngày sinh", "Số tiết vắng"]
        self.start_index_to_display = 0
        self.config_size_list = list()
        self.attributes_set = atts + self.date_list
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

        self.table = ttk.Treeview(self.canvas1, height=12, show="headings", selectmode="browse")

        self.yscrollbar = ttk.Scrollbar(self.canvas1, orient=VERTICAL, command=self.table.yview)
        self.yscrollbar.place(x=1163, y=210, height=330)
        self.xscrollbar = ttk.Scrollbar(self.canvas1, orient=HORIZONTAL, command=self.table.xview)
        self.xscrollbar.place(x=100, y=538, width=1077)
        self.table.configure(yscroll=self.yscrollbar.set, xscroll=self.xscrollbar.set)

        self.table["columns"] = self.attributes_set
        if len(self.date_list) > 0:
            self.set_columns()
        else:
            self.set_columns_without_dates()
        
        self.table.place(x=100, y=210)
        self.insert_data()

        if type(self) is StatisticalFrame:
            self.master.bind("<Left>", self.set_display_columns_previous)
            self.master.bind("<Right>", self.set_display_columns_next)

        self.canvas1.create_rectangle(100, 538, 1175, 620, fill="#D1D1D1", outline="#D1D1D1")
        self.canvas1.create_text(630, 585, text="Tổng kết điểm danh sinh viên", font=("Arial", 20), fill="black")
        self.export_button = Button(self.canvas1, text="Xuất file", width=8, font=("Arial", 14), bg="yellow", fg="black", command=self.export_file)
        self.export_button.place(x=590, y=630)

    def set_columns(self):
        self.table.column("STT", minwidth=40, width=40, anchor="center", stretch=NO)
        self.table.column("Họ và tên", minwidth=250, width=250, anchor="center", stretch=NO)
        self.table.column("Mã SV", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Giới tính", minwidth=150, width=150, anchor="center", stretch=NO)
        self.table.column("Ngày sinh", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Số tiết vắng", minwidth=150, width=150, anchor="center", stretch=NO)
        for date in self.date_list:
            self.table.column(date, minwidth=70, width=70, anchor="center", stretch=NO)
        for col in self.table['columns']:
            self.table.heading(col, text=f"{col}", anchor=CENTER)
        self.set_display_columns()

    def set_columns_without_dates(self):
        self.table.column("STT", minwidth=80, width=80, anchor="center", stretch=NO)
        self.table.column("Họ và tên", minwidth=280, width=280, anchor="center", stretch=NO)
        self.table.column("Mã SV", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Giới tính", minwidth=150, width=150, anchor="center", stretch=NO)
        self.table.column("Ngày sinh", minwidth=200, width=200, anchor="center", stretch=NO)
        self.table.column("Số tiết vắng", minwidth=150, width=150, anchor="center", stretch=NO)
        for col in self.table['columns']:
            self.table.heading(col, text=f"{col}", anchor=CENTER)

    def set_display_columns(self):
        self.table['displaycolumns'] = self.attributes_set[self.start_index_to_display:self.start_index_to_display+7]
        self.table.update()

    def set_display_columns_next(self, event=None):
        if self.start_index_to_display + 7 < len(self.attributes_set):
            self.modify_columns_size_if_next()
            self.start_index_to_display += 1
            self.set_display_columns()

    def set_display_columns_previous(self, event=None):
        if self.start_index_to_display > 0:
            self.modify_columns_size_if_previous()
            self.start_index_to_display -= 1
            self.set_display_columns()

    def modify_columns_size_if_next(self):
        self.config_size_list.append([self.table.column(col, option='width') for col in self.table['columns']])
        max_size_column = 0
        max_col_name = ""
        first_column_size = self.table.column(self.table['displaycolumns'][0], width=None)
        size_of_column_need_to_display = self.table.column(self.table['columns'][self.start_index_to_display+7], width=None)
        size_need_to_change = size_of_column_need_to_display - first_column_size 

        for col in self.table['displaycolumns']:
            size_column = self.table.column(col, option="width")
            if size_column > max_size_column:
                max_size_column = size_column
                max_col_name = col

        new_sum_size = 0
        for i in range(self.start_index_to_display+1, self.start_index_to_display+8):
            new_sum_size += self.table.column(self.table['columns'][i], width=None)
        
        if new_sum_size == 1060:
            return
        
        if size_need_to_change > 0:
            self.table.column(max_col_name, width=max_size_column - size_need_to_change)
        elif size_need_to_change < 0:
            size_need_to_change = -size_need_to_change
            width_increase_for_each_column = size_need_to_change//7
            residual_width = size_need_to_change%7
            for i in range(self.start_index_to_display+1, self.start_index_to_display+8):
                if i == self.start_index_to_display+4:
                    self.table.column(self.table['columns'][i], width=self.table.column(self.table['columns'][i], width=None) + width_increase_for_each_column + residual_width)
                else:
                    self.table.column(self.table['columns'][i], width=self.table.column(self.table['columns'][i], width=None) + width_increase_for_each_column)

    def modify_columns_size_if_previous(self):
        previous_config_size = self.config_size_list.pop()
        for i in range(len(previous_config_size)):
            self.table.column(self.table['columns'][i], width=previous_config_size[i])

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
            attendance_std_list = get_attendance(student_list[i][0])
            self.table.insert("", "end", values=[i+1, student_list[i][1], student_list[i][0], student_list[i][2], student_list[i][3], student_list[i][4]] + attendance_std_list)

    def get_data(self):
        data = {}
        for col in self.table['columns']:
            data[col] = []
        for child in self.table.get_children():
            for col in self.table['columns']:
                data[col].append(self.table.item(child)['values'][self.table['columns'].index(col)])
        return data

    def export_file(self):
        data = self.get_data()
        file_name = filedialog.asksaveasfilename(initialdir="/", title="Save as", filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")), defaultextension=".xlsx")
        if file_name:
            if file_name.endswith('.xlsx'):
                export_xlsx_file(file_name, data, self.attributes_set)
                efs = 1
            elif file_name.endswith('.csv'):
                export_csv_file(file_name, data, self.attributes_set)
                efs = 1         
            else:
                messagebox.showerror("Lỗi", "Định dạng file không hỗ trợ")
                efs = 0
            if efs == 1:
                messagebox.showinfo("Thông báo", "Xuất file thành công")
        else:
            return       