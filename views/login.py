from tkinter import *
from tkinter import messagebox
from views.menu import MenuFrame
from PIL import ImageTk, Image
from controller import *

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=TOP, fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.canvas1 = Canvas(self, bg="#D1D1D1")
        self.canvas1.pack(side=TOP, fill="both", expand=True)

        self.canvas1.create_rectangle(100, 60, 1180, 640, fill="#FFFFFF", outline="#B2B1B1")

        # self.canvas1.create_rectangle(100, 90, 280, 310, fill="#573434", outline="#573434")#180x220
        self.hus_logo = ImageTk.PhotoImage(Image.open("images/huslogo.jpg"))
        self.canvas1.create_image(400, 350, image=self.hus_logo)#190 200

        self.canvas1.create_text(670, 200, text="Đăng nhập", font=("Arial", 20, "bold"), fill="#1160FB")

        self.canvas1.create_text(570, 300, text="Tài khoản", font=("Arial", 14))
        self.username_entry = Entry(self.canvas1, width=25, font=("Arial", 14), background="#C4C4C4")
        self.username_entry.bind("<Return>", self.login)
        self.username_entry.place(x=530, y=320)

        self.canvas1.create_text(568, 380, text="Mật khẩu", font=("Arial", 14))
        self.password_entry = Entry(self.canvas1, width=25, font=("Arial", 14), background="#C4C4C4", show="*")
        self.password_entry.bind("<Return>", self.login)
        self.password_entry.place(x=530, y=400)

        self.login_button = Button(self.canvas1, text="Đăng nhập", height=1, width=15, font=("Arial", 15), background="#F32463", foreground="white", command=self.login)
        self.login_button.place(x=580, y=450)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if check_login(username, password):
            self.destroy()
            MenuFrame(self.master).tkraise()
        else:
            messagebox.showerror("Thông báo", "Đăng nhập thất bại\nTài khoản hoặc mật khẩu không đúng.")