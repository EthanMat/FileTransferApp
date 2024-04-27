import tkinter as tk
import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from tkinter import ttk, font
from PIL import Image
from File import File
import Network

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("dark") 
  
# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("green") 

#create a window and set its geometry
window = ctk.CTk()
window.geometry("500x530")

window.minsize(60,50)
 
#window customizions
window.iconbitmap("Icon.ico")
window.title("Wireless File Transfer")

def login():
    print(username.get())
    print(server.get())

image = ctk.CTkImage(light_image=Image.open("logo.png"),
                    dark_image=Image.open("logo.png"),
                    size=(128, 128))

logo = ctk.CTkLabel(window, image = image, text = "")
logo.pack(pady=70)

welcome_label = ctk.CTkLabel(window, text="Welcome", font = ("Trebuchet MS", 42, "bold"))
welcome_label.pack(padx = 10)

login_frame = ctk.CTkFrame(window)
login_frame.pack(pady=20,padx=150,fill='both',expand=True)

username = ctk.CTkEntry(login_frame, placeholder_text = "Username")
username.pack(pady = 20)

server = ctk.CTkEntry(master = login_frame, placeholder_text = "Server IP Address")
server.pack()

login_button = ctk.CTkButton(login_frame, text = "Log In", command = login)
login_button.pack(pady = 20)

#run main loop
window.mainloop()