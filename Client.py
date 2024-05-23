import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from tkinter import filedialog
from PIL import Image
from File import File
from Server import Server
from Network import Network
import threading
import time

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("dark") 
  
# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("green") 

num_clients_connected = 0
clients_connected = [] 
names = []

#create a window and set its geometry
window = ctk.CTk()
window.geometry("500x530")

window.minsize(60,50)
 
#window customizions
window.iconbitmap(default="Icon.ico")
window.title("Wireless File Transfer")

def listen_for_files():
    while True:
        try:
            data = n.listen()
            if data.find("0") > -1:
                File.binary_string_to_file(data, "C:\\Users\\ethma\\Downloads\\TEST.PNG")
                print(data)
                return
            time.sleep(7)
        except:
            continue    

def send_file():
    try:
        for file in names:
            print(n.send(dropdown_menu.get() + " " + File.file_to_binary_string(file)))
            #print(File.file_to_binary_string(file))

    except NameError as e:
        x = tkmb.showerror("Error", "No files selected...")

def split_string(string):
    length = len(string)
    return_string = ""
    for i in range(length):
        if i >= length / 2:
            return_string += string[i]
    return return_string

def open_file_dialog():
    global names
    file_path = filedialog.askopenfiles(title="Select a File(s)", filetypes=[("All files", "*.*")])
    if file_path:
        for item in scrolling_frame.winfo_children():
            destroy(item)
        for file in file_path:
            names.append(file.name)
        for n in names:
            x = ctk.CTkLabel(scrolling_frame, text = "..." + split_string(n))
            x.pack()
        process = threading.Thread(target = process_file, args = (file_path,))
        process.start()
        for file in file_path:
            print(file.name)

def process_file(file_path):
    file_data = []
    progress_bar = ctk.CTkProgressBar(window, orientation = "horizontal", determinate_speed = (1/len(file_path)) * 10)
    progress_bar.set(0)
    progress_bar.pack()
    for file in file_path:
        file_data.append(File.file_to_binary_string(file.name))
        progress_bar.step()
    progress_bar.set(1)
    time.sleep(0.5)
    destroy(progress_bar)
    #print(file_data)


def update_users(string):
    global n
    global clients_connected
    global dropdown_menu
    try:
        clients_connected = n.get_connected_users().split()
        clients_connected.remove(username.get())
        dropdown_menu.configure(values = clients_connected)
    except: 
        pass
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

    top_frame = ctk.CTkFrame(page, width = 3000, height = 200, bg_color = "transparent")
    top_frame.pack_configure(pady=55,padx=65,fill='none',expand=False)

    global dropdown_menu
    dropdown_menu = ctk.CTkOptionMenu(top_frame, values = clients_connected, variable = selected_value, command = update_users)
    dropdown_menu.grid(row = 0, column = 0, padx = 10)

    # refresh = ctk.CTkButton(top_frame, text = "Refresh", width = 50, height = 50)
    # refresh.grid(row = 0, column = 1)

    select_file_button = ctk.CTkButton(page, text = "Select File", command = open_file_dialog)
    select_file_button.pack()

    global selected_file_label
    selected_file_label = ctk.CTkLabel(page, text = "Selected file(s): ")
    selected_file_label.pack(pady = 15)

    global scrolling_frame
    scrolling_frame = ctk.CTkScrollableFrame(page, width = 400)
    scrolling_frame.pack()

    send_file_button = ctk.CTkButton(page, text = "Send File(s)", command = send_file)
    send_file_button.pack(pady = 20)

    listener = threading.Thread(target = listen_for_files)
    listener.start()

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
            n.disconnect()
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