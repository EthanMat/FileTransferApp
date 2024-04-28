import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from PIL import Image
from File import File
from Server import Server
from Network import Network
import threading

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("dark") 
  
# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("green") 

global main_server
global n

#create a window and set its geometry
window = ctk.CTk()
window.geometry("500x530")

window.minsize(60,50)
 
#window customizions
window.iconbitmap("Icon.ico")
window.title("Wireless File Transfer")

def login():
    if is_host_computer.get() == 1:
        global main_server
        main_server = Server(server.get())
        main_server.start_server()
        x = threading.Thread(target = main_server.run)
        x.start()
        is_host_computer.toggle()
    try: 
        global n
        n = Network(username.get(), server.get())
        print(n.send("Hello"))
        print(n.send("Working"))
        print(main_server.get_connected_users()) #type: ignore
        #n.disconnect()

    except OSError as e:
        x = False
        if e == "Server not found...":
            x = tkmb.askretrycancel(str(e), "Check server address or check \"Run Server?\"")
        elif e == "Could not connect to server...":
            x = tkmb.askretrycancel(str(e), "User already exists!")

        if x:
            pass

def on_close():
    close = tkmb.askokcancel("Close", "Would you like to close the program?")
    if close:
        window.destroy()
        n.disconnect() # type: ignore
        try:
            main_server.stop() # type: ignore
        except:
            pass

image = ctk.CTkImage(light_image=Image.open("logo.png"),
                    dark_image=Image.open("logo.png"),
                    size=(128, 128))

logo = ctk.CTkLabel(window, image = image, text = "")
logo.pack(pady=55)

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

is_host_computer = ctk.CTkSwitch(login_frame, text = "Run Server?")
is_host_computer.pack(pady = 5)

window.protocol("WM_DELETE_WINDOW", on_close)

#run main loop
window.mainloop()