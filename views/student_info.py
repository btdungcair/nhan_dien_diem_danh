from tkinter import *
from views.base import ParentFrame
from views import student_list
from PIL import ImageTk, Image
from controller import *
from helper import octet_string_to_image

class StudentInfoFrame(ParentFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.student_id = student_id
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        super().create_widgets()

        self.student = get_student(self.student_id)[0]

        self.canvas1.create_rectangle(299, 149, 675, 650, fill='#00bfff', outline='red')

        image = octet_string_to_image(self.student[5])
        image = image.resize((375, 500), Image.ANTIALIAS)
        self.student_image = ImageTk.PhotoImage(image)
        self.canvas1.create_image(487, 400, image=self.student_image)

        self.fullname_label = Label(self.canvas1, text=self.student[1], font=('Arial', 22), fg="white", bg="#F32463")
        self.fullname_label.place(x=800, y=200)

        self.id_label = Label(self.canvas1, text="Mã sinh viên: "+str(self.student[0]), font=('Arial', 18), fg="black")
        self.id_label.place(x=795, y=300)

        self.gender_label = Label(self.canvas1, text="Giới tính: "+self.student[2], font=('Arial', 18), fg="black")
        self.gender_label.place(x=795, y=380)

        self.dob_label = Label(self.canvas1, text="Ngày sinh: "+self.student[3], font=('Arial', 18), fg="black")
        self.dob_label.place(x=795, y=460)

        self.absent_count_label = Label(self.canvas1, text="Số buổi vắng: "+str(self.student[4]), font=('Arial', 18), fg="black")
        self.absent_count_label.place(x=795, y=540)

    def back(self):
        self.destroy()
        student_list.StudentListFrame(self.master).tkraise()