import tkinter as tk
from tkinter import ttk
import File

#create a window and set its geometry
window = tk.Tk()
window.geometry("800x500")
test = File.File.file_to_binary_string("File.py")
try:
    print(test)
    File.File.binary_string_to_file(test, "C:\\Users\\ethma\\Documents\\Ethan_work\\home\\Ethan_codes\\python\\FileTransferApp\\test.py")
except MemoryError as e:
    print("This file is too large to Process!")

#run main loop
window.mainloop()