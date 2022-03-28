from tkinter import *
from tkinter import messagebox
from views import login, menu
from PIL import ImageTk, Image
from controller import *

class ParentFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

    def create_widgets(self):
        self.canvas1 = Canvas(self, bg="#D1D1D1")
        self.canvas1.pack(side=TOP, fill="both", expand=True)

        self.background_image = ImageTk.PhotoImage(Image.open("images/background.png"))
        self.canvas1.create_image(60, 40, image=self.background_image, anchor=NW)

        self.back_icon = ImageTk.PhotoImage(Image.open("images/back.png"))
        self.back_button = Button(self.canvas1, image=self.back_icon, highlightthickness=0, bd=0, borderwidth=0, command=self.back)
        self.back_button.place(x=80, y=60)

        self.canvas1.create_text(630, 100, text="Hệ thống quản lý sinh viên", font=("Arial", 40), fill="#FF5858")

        self.logout_icon = ImageTk.PhotoImage(Image.open("images/logout.png"))
        self.logout_button = Button(self.canvas1, image=self.logout_icon, highlightthickness=0, bd= 0, borderwidth=0, command=self.logout)
        self.logout_button.place(x=1140, y=60)
    
    def back(self):
        previous_frame = None
        if type(self) is menu.MenuFrame:
            self.logout()
        else:
            previous_frame = menu.MenuFrame(self.master)
        if not previous_frame is None:
            self.destroy()
            previous_frame.tkraise()

    def logout(self):
        msgbox = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        if msgbox:
            login_frame = login.LoginFrame(self.master)
            self.destroy()
            login_frame.tkraise()
        else:
            return