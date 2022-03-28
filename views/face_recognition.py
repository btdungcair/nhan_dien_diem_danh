from tkinter import *
from tkinter import filedialog, messagebox
from views import base
from PIL import ImageTk, Image
from controller import *
import recognition
import os
class FaceRecognitionFrame(base.ParentFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        super().create_widgets()
        self.import_image_button = Button(self, text="Import ảnh", font=("Arial", 18), bg="#F32463", fg="white", command=self.import_image)
        self.import_image_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def import_image(self):
        self.imgs_res = []
        self.id_list = []
        self.image_index = len(self.imgs_res)
        self.image_path_list = filedialog.askopenfilenames(title="Chọn ảnh", filetypes=(("Image Files", "*.jpg"), ("Image Files", "*.png"), ("Image Files", "*.jpeg"), ("All Files", "*.*")))
        if len(self.image_path_list) > 0:
            self._face_recognition()
            self.create_control_button()
            self.show_image()

    def create_control_button(self):
        self.import_image_button.destroy()

        self.canvas1.create_rectangle(239, 149, 1040, 600, fill="white", outline="black")

        self.previous_image_button_icon = ImageTk.PhotoImage(Image.open("images/previous_image_button.png"))
        previous_image_button = Button(self, image=self.previous_image_button_icon, highlightthickness=0, bd=0, borderwidth=0, command=self.show_previous_image)
        previous_image_button.place(relx=0.27, rely=0.85)

        self.next_image_button_icon = ImageTk.PhotoImage(Image.open("images/next_image_button.png"))
        next_image_button = Button(self, image=self.next_image_button_icon, highlightthickness=0, bd=0, borderwidth=0, command=self.show_next_image)
        next_image_button.place(relx=0.7, rely=0.85)

        self.verify_button = Button(self, text="Xác nhận kết quả", font=("Arial", 16), bg="#F32463", fg="white", command=self.verify)
        self.verify_button.place(relx=0.425, rely=0.855)
        
        if type(self) is FaceRecognitionFrame:
            self.master.bind("<Left>", self.show_previous_image)
            self.master.bind("<Right>", self.show_next_image)

    def _face_recognition(self):
        res1 = recognition.faceRecognition(self.image_path_list)
        self.id_list = res1[0]
        self.imgs_res = res1[1]
        return True

    def show_image(self):
        _img = Image.open(self.imgs_res[self.image_index])
        x, y = 640, 375
        #800 x 450
        while True:
            width, height = _img.size
            if width <= 800 and height <= 450:
                break
            old_ratio = width/height
            if width > 800:
                width = 800
                height = int(width/old_ratio)
                _img = _img.resize((width, height), Image.ANTIALIAS)
            elif height > 450:
                height = 450
                width = int(height*old_ratio)
                _img = _img.resize((width, height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(_img) 
        self.canvas1.create_image(x, y, image=self.img, anchor=CENTER)

    def show_previous_image(self, event=None):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()
    
    def show_next_image(self, event=None):
        if self.image_index < len(self.image_path_list) - 1:
            self.image_index += 1
            self.show_image()

    def verify(self):
        attendance(self.id_list)
        messagebox.showinfo("Thông báo", "Đã lưu thông tin")