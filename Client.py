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
clients_connected = 0

#create a window and set its geometry
window = ctk.CTk()
window.geometry("500x530")

window.minsize(60,50)
 
#window customizions
window.iconbitmap(default="Icon.ico")
window.title("Wireless File Transfer")

def main_page(n):
    page = ctk.CTkToplevel(window)
    page.grab_set()

    page.protocol("WM_DELETE_WINDOW", lambda args = (page, n): on_close_main(args))

    #Page customizations
    page.title(username.get())
    page.geometry("400x400")
    page.attributes("-topmost", True)
    page.attributes("-topmost", False)

def login():
    if is_host_computer.get() == 1:
        global main_server
        main_server = Server(server.get())
        try:
            main_server.start_server()
            x = threading.Thread(target = main_server.run)
            x.start()
            is_host_computer.toggle()
            is_host_computer.configure(state="disabled")
        except OSError as e:
            if str(e) == "Server1":
                x = tkmb.showerror("Can't start Server", "Check server address. It should be the exact same as your local IP address.")
                return
            elif str(e) == "Server2":
                x = tkmb.showerror("Can't start Server", "Check server address.")
                return
    try: 
        n = Network(username.get(), server.get())
        global clients_connected
        clients_connected += 1
        #TODO: This number is greater than 1 for testing perposes, fix that
        if (clients_connected > 5):
            n.disconnect()
            raise OSError("Multiple Clients")
        print(main_server.get_connected_users())
        main = threading.Thread(target = main_page, args = (n,))
        main.start()
        #n.disconnect()

    except OSError as e:
        if str(e) == "Server not found...":
            x = tkmb.showerror(str(e), "Check server address or check \"Run Server?\"")
            clients_connected -= 1
            return
        elif str(e) == "Could not connect to server...":
            x = tkmb.showerror(str(e), "User already exists!")
            n.disconnect()
            clients_connected -= 1
            return
        elif str(e) == "Multiple Clients":
            x = tkmb.showerror("Error", "Why would you want to send files to yourself?")
            n.disconnect()
            clients_connected -= 1
            return
        
    except Exception as e:
        x = tkmb.showerror("Error", str(e))
        clients_connected -= 1
        return

def on_close_login():
    close = tkmb.askokcancel("Close", "Would you like to close the program?")
    if close:
        window.destroy()
        try:
            main_server.stop() 
        except:
            pass

def on_close_main(page):
    page[0].destroy()
    page[1].disconnect() 
    global clients_connected
    clients_connected -= 1 

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

window.protocol("WM_DELETE_WINDOW", on_close_login)

#run main loop
window.mainloop()