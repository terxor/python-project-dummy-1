from tkinter import *
from tkinter import ttk

from .init_screen import InitScreen
from .auth_screen import AuthScreen

class AppGUI:
  def __init__(self,dbc):
    self.dbc = dbc
    self.root = Tk()

  def go(self):
    if self.dbc.is_initialized():
      AuthScreen(self.root, self.dbc)
    else:
      InitScreen(self.root, self.dbc)
    self.root.mainloop()
