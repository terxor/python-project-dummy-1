from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from .main_screen import MainScreen

class AuthScreen:
  def __init__(self, root, dbc):
    self.root = root
    self.dbc = dbc

    self.root.title("Authenticate")
    self.frame = ttk.Frame(self.root)
    self.frame.grid()

    self.password = StringVar()

    labelText = "Authenticate to access the password manager"
    ttk.Label(self.frame, text=labelText).grid(column=0,row=0)

    ttk.Label(self.frame, text="Master password").grid(column=0,row=1)
    ttk.Entry(self.frame, textvariable=self.password).grid(column=1, row=1)

    ttk.Button(self.frame, text="Proceed", command=self.go).grid(column=1, row=2)

  def go(self):
    if self.dbc.is_correct_password(self.password.get()):
      self.frame.destroy()
      main_screen = MainScreen(self.root, self.dbc)
      main_screen.reload()
    else:
      messagebox.showinfo(message="Incorrect Password")
      self.password.set("")

