from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class ScrollableFrame(ttk.Frame):
  def __init__(self, container, *args, **kwargs):
    super().__init__(container, *args, **kwargs)
    canvas = Canvas(self)
    scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
    self.scrollable_frame = ttk.Frame(canvas)
    self.scrollable_frame.bind(
      "<Configure>",
      lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
      )
    )
    canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(column=0, row=0, sticky="we")
    scrollbar.grid(column=1, row=0, sticky="ns")

class MainScreen:
  def __init__(self, root, dbc):
    self.root = root
    self.dbc = dbc

    self.root.title("Password Manager")
    self.frame = ttk.Frame(self.root)
    self.frame.grid()

    ttk.Label(self.frame, text="Welcome, user").grid(column=0,row=0)
    ttk.Label(self.frame, text="Your stored passwords:").grid(column=0,row=1)
    
    self.table = ScrollableFrame(self.frame)
    self.table.grid(column=0, row=2, columnspan=2)
    
    self.input_name = StringVar()
    self.input_userid = StringVar()
    self.input_password = StringVar()
    ttk.Label(self.frame, text="Add an entry:").grid(column=0,row=3)

    ttk.Label(self.frame, text="Name:").grid(column=0,row=4)
    ttk.Entry(self.frame, textvariable=self.input_name).grid(column=1,row=4)

    ttk.Label(self.frame, text="Userid:").grid(column=0,row=5)
    ttk.Entry(self.frame, textvariable=self.input_userid).grid(column=1,row=5)

    ttk.Label(self.frame, text="Password:").grid(column=0,row=6)
    ttk.Entry(self.frame, textvariable=self.input_password).grid(column=1,row=6)

    ttk.Button(self.frame, text="Add", command=self.add_entry).grid(column=1,row=7)

  def reload(self):
    for child in self.table.scrollable_frame.winfo_children():
      child.destroy()
    ttk.Label(self.table.scrollable_frame, text="name").grid(column=0, row=0)
    ttk.Label(self.table.scrollable_frame, text="userid").grid(column=1, row=0)
    ttk.Label(self.table.scrollable_frame, text="password").grid(column=2, row=0)
    ttk.Label(self.table.scrollable_frame, text="action").grid(column=3, row=0)

    cnt = 1
    entries = self.dbc.get_entries()
    for e in entries:
      print(e)
      ttk.Label(self.table.scrollable_frame, text=e[1]).grid(column=0, row=cnt)
      ttk.Label(self.table.scrollable_frame, text=e[2]).grid(column=1, row=cnt)
      ttk.Label(self.table.scrollable_frame, text=e[3]).grid(column=2, row=cnt)
      ttk.Button(self.table.scrollable_frame, text="Delete",command=lambda x=e[0]:self.delete_entry(x)).grid(column=3, row=cnt)
      cnt += 1
        
  def delete_entry(self, entry_id):
    self.dbc.remove_entry(entry_id)
    self.reload()

  def add_entry(self):
    self.dbc.add_entry(self.input_name.get(), self.input_userid.get(), self.input_password.get())
    self.reload()
