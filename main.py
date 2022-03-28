from tkinter import Tk
from views.login import LoginFrame

window = Tk()
window.title("Quản lý điểm danh - HUS")
window.geometry("1280x720")
window.resizable(0, 0)
startFrame = LoginFrame(window)

# username: admin   | anhquanhus0902    | user1
# password: admin   | 123456            | haha

if __name__ == "__main__":
    window.mainloop()
