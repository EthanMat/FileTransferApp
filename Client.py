import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import File

#create a window and set its geometry
window = tk.Tk()
window.geometry("800x500")

window.minsize(300,100)
 
#window customizions
window.iconbitmap("Icon.ico")
window.title("Wireless File Transfer")

image = Image.open('logo.png').resize((128, 128))
image = ImageTk.PhotoImage(image)

logo = tk.Label(window, image=image) # type: ignore
logo.pack()

welcome_label = ttk.Label(window, text="Welcome", font=font.BOLD)
welcome_label.pack()

username = ttk.Entry(window)
username.pack()

#run main loop
window.mainloop()