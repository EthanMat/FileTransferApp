import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from tkinter import filedialog
from PIL import Image
from File import File
from Server import Server
from Network import Network
import threading

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("dark") 
  
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

def open_file_dialog():
    file_path = filedialog.askopenfiles(title="Select a File(s)", filetypes=[("All files", "*.*")])
    if file_path:
        selected_file_label.configure(text=f"Selected File(s): {file_path}")
        process_file(file_path)
        for file in file_path:
            print(file.name)

def process_file(file_path):
    pass

def update_users():
    global n
    global clients_connected
    global dropdown_menu
    clients_connected = n.get_connected_users().split()
    try:
        clients_connected.remove(username.get())
    except: 
        pass
    dropdown_menu.configure(values = clients_connected)
    print(clients_connected)

def main_page(page):
    global n

    page.protocol("WM_DELETE_WINDOW", on_close_main)

    #Page customizations
    page.title(username.get())
    page.geometry("500x500")

    clients_connected.append("Select a user")
    selected_value = ctk.StringVar()
    selected_value.set(clients_connected[0])

    global dropdown_menu
    dropdown_menu = ctk.CTkOptionMenu(page, values = clients_connected, variable = selected_value)
    update_users()
    dropdown_menu.pack()

    refresh = ctk.CTkButton(page, text = "Refresh", command = update_users)
    refresh.pack()

    global selected_file_label
    selected_file_label = ctk.CTkLabel(page, text = "Selected file: ")
    selected_file_label.pack()

    select_file = ctk.CTkButton(page, text = "Select File", command = open_file_dialog)
    select_file.pack()

def login():
    #This block of code starts the server if the slider "Run Server?" is toggled on
    if is_host_computer.get() == 1:
        global main_server
        main_server = Server(server.get())
        try:
            main_server.start_server()
            thread = threading.Thread(target = main_server.run)
            thread.start()
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
        on_close_login()
        n = Network(username.get(), server.get())
        num_clients_connected += 1
        main_page(window)
        #TODO: This number is greater than 1 for testing perposes, fix that
        if (num_clients_connected > 1):
            n.disconnect()
            raise OSError("Multiple Clients")

    except OSError as e:
        if str(e) == "Server not found...":
            x = tkmb.showerror(str(e), "Check server address or check \"Run Server?\"")
            num_clients_connected -= 1
            login_page()
            return
        elif str(e) == "Could not connect to server...":
            x = tkmb.showerror(str(e), "User already exists!")
            n.disconnect()
            num_clients_connected -= 1
            login_page()
            return
        elif str(e) == "Multiple Clients":
            x = tkmb.showerror("Error", "Why would you want to send files to yourself?")
            n.disconnect()
            login_page()
            return
        
    except Exception as e:
        x = tkmb.showerror("Error", str(e))
        num_clients_connected -= 1
        login_page()
        return

def on_close_main():
    close = tkmb.askokcancel("Close", "Would you like to close the program?")
    if close:
        window.destroy()
        try:
            main_server.stop() 
        except:
            pass

def on_close_login():
    username.set(username_entry.get())
    server.set(server_entry.get())
    destroy(logo, welcome_label, login_frame)

def destroy(*args):
    for arg in args:
        arg.destroy()

def login_page():
    image = ctk.CTkImage(light_image=Image.open("logo.png"),
                        dark_image=Image.open("logo.png"),
                        size=(128, 128))

    global logo
    logo = ctk.CTkLabel(window, image = image, text = "")
    logo.pack(pady=55)

    global welcome_label
    welcome_label = ctk.CTkLabel(window, text="Welcome", font = ("Trebuchet MS", 42, "bold"))
    welcome_label.pack(padx = 10)

    global login_frame
    login_frame = ctk.CTkFrame(window)
    login_frame.pack(pady=20,padx=150,fill='both',expand=True)

    global username
    username = ctk.StringVar()

    global username_entry
    username_entry = ctk.CTkEntry(login_frame, placeholder_text = "Username")
    username_entry.pack(pady = 20)

    global server
    server = ctk.StringVar()

    global server_entry
    server_entry = ctk.CTkEntry(master = login_frame, placeholder_text = "Server IP Address")
    server_entry.pack()

    login_button = ctk.CTkButton(login_frame, text = "Log In", command = login)
    login_button.pack(pady = 20)

    global is_host_computer
    is_host_computer = ctk.BooleanVar()
    is_host_computer.set(False)

    is_host_computer_switch = ctk.CTkSwitch(login_frame, text = "Run Server?", variable = is_host_computer)
    is_host_computer_switch.pack(pady = 5)

    window.protocol("WM_DELETE_WINDOW", on_close_main)

login_page()
#run main loop
window.mainloop()