import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from PIL import Image
from File import File
from Server import Server
from Network import Network
import threading

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("system") 
  
# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("green") 

num_clients_connected = 0
clients_connected = []


#create a window and set its geometry
window = ctk.CTk()
window.geometry("500x530")

window.minsize(60,50)
 
#window customizions
window.iconbitmap(default="Icon.ico")
window.title("Wireless File Transfer")

def update_users():
    global n
    global clients_connected
    clients_connected = n.get_connected_users().split()
    print(clients_connected)

def main_page():
    global page
    global n
    page = ctk.CTkToplevel(window)

    page.protocol("WM_DELETE_WINDOW", on_close_main)

    #Page customizations
    page.title(username.get())
    page.geometry("400x400")

    update_users()

def login():
    #This block of code starts the server if the slider "Run Server?" is toggled on
    if is_host_computer.get() == 1:
        global main_server
        main_server = Server(server.get())
        try:
            main_server.start_server()
            thread = threading.Thread(target = main_server.run)
            thread.start()
            is_host_computer.toggle()
            is_host_computer.configure(state="disabled")
        except OSError as e:
            if str(e) == "Server1":
                x = tkmb.showerror("Can't start Server", "Check server address. It should be the exact same as your local IP address.")
                return
            elif str(e) == "Server2":
                x = tkmb.showerror("Can't start Server", "Check server address.")
                return
            
    #Tries to open a connection to the server and open the UI
    try: 
        global n
        global num_clients_connected
        n = Network(username.get(), server.get())
        num_clients_connected += 1
        main_page()
        #TODO: This number is greater than 1 for testing perposes, fix that
        if (num_clients_connected > 1):
            n.disconnect()
            raise OSError("Multiple Clients")

    except OSError as e:
        if str(e) == "Server not found...":
            x = tkmb.showerror(str(e), "Check server address or check \"Run Server?\"")
            num_clients_connected -= 1
            return
        elif str(e) == "Could not connect to server...":
            x = tkmb.showerror(str(e), "User already exists!")
            n.disconnect()
            num_clients_connected -= 1
            return
        elif str(e) == "Multiple Clients":
            x = tkmb.showerror("Error", "Why would you want to send files to yourself?")
            n.disconnect()
            on_close_main()
            return
        
    except Exception as e:
        x = tkmb.showerror("Error", str(e))
        num_clients_connected -= 1
        return

def on_close_login():
    close = tkmb.askokcancel("Close", "Would you like to close the program?")
    if close:
        window.destroy()
        try:
            main_server.stop() 
        except:
            pass

def on_close_main():
    global page
    page.destroy()
    global n
    n.disconnect() 
    global num_clients_connected
    num_clients_connected -= 1 

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