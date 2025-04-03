import customtkinter
from authentication import auth
import pickle as pk
import os

# Global values
AUTH_FILEPATH = "./auth.data"
BASH_FILEPATH = "./genrated/"
TEMP_FILENAME = "temp_data.data"

def is_user_already_loggedin():
    """Checks if the user has previously logged in and selected 'Remember Me'."""
    if os.path.exists(AUTH_FILEPATH):  
        with open(AUTH_FILEPATH, "rb") as file:
            try:
                data = pk.load(file)
                if not data:
                    return None, False  
            except (EOFError, pk.UnpicklingError):
                return None, False  
            
        last_logged_user = max(data, key=lambda user: data[user][2]) 
        
        if data[last_logged_user][1] == 1:  
            return last_logged_user, True
        else:
            return last_logged_user, False 

    return None, False  


class Utility: 
    '''This utility function handles all the fucntions all together to handling the files.'''
    def __init__(self, code_box, username):
        self.code_area = code_box
        self.username = username  
        self.filepath = os.path.join(BASH_FILEPATH, f"{username}_last_session.pkl")

        self.load_previous_data()

    def add_echo(self): 
        if self.code_area:
            self.code_area.insert("end", "echo \"Write a message you want to display\"\n")

    def store_data_on_window_close(self):
        if self.code_area and self.code_area.winfo_exists():  # Check if widget exists
            data = self.code_area.get("1.0", "end-1c")
            os.makedirs(BASH_FILEPATH, exist_ok=True)
            with open(self.filepath, "wb") as file:
                pk.dump(data, file)

    def load_previous_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "rb") as file:
                    data = pk.load(file)
                    if self.code_area:
                        self.code_area.insert("1.0", data)
            except (EOFError, pk.UnpicklingError):
                pass


                
        

# Basic GUI setup
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x700")
        customtkinter.set_appearance_mode("System")  
        customtkinter.set_default_color_theme("blue")
        self.title("Custom Startup")

        self.AuthWindow = None
        self.current_user, self.logged_in = is_user_already_loggedin()
        self.main_frame1 = None 
        self.main_frame2 = None
        self.script_textbox = None  
        self.util = None  # Initialize as None first

        self.label = customtkinter.CTkLabel(self, text="", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        if self.logged_in:
            self.show_main()
        else:
            self.show_login_button()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.util:
            self.util.store_data_on_window_close()
        else: 
            pass
        self.destroy()

    def show_login_button(self):
        """Display the login button when no user is logged in."""
        self.label.configure(text="Welcome! Please log in.")
        self.button_1 = customtkinter.CTkButton(self, text="Login", command=self.open_toplevel)
        self.button_1.pack(pady=20)
    
    def logout_user(self):
        self.util.store_data_on_window_close()

        self.AuthWindow = None
        self.current_user, self.logged_in = "", False 
        if hasattr(self, "button_2"):  
            self.button_2.pack_forget()

        self.label = customtkinter.CTkLabel(self, text="Welcome! Please log in.", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        if self.main_frame1:
            self.main_frame1.destroy()
        if self.main_frame2:
            self.main_frame2.destroy()

        self.main_frame1 = None 
        self.main_frame2 = None
        self.show_login_button()
        


    def update_ui(self, username):
        """Update the main window after a successful login."""
        self.label.destroy()

        # self.util.username = self.current_user

        if hasattr(self, "button_1"):  
            self.button_1.pack_forget()
        
        self.button_2 = customtkinter.CTkButton(self, text="Logout", command=self.logout_user, 
                                                fg_color="red", hover_color="#8B0000")
        self.button_2.pack(pady=20)

    def open_toplevel(self):
        """Open the authentication window."""
        if self.AuthWindow is None or not self.AuthWindow.winfo_exists():
            self.AuthWindow = auth.AuthWindow(self)  
            self.AuthWindow.grab_set()
        else:
            self.AuthWindow.focus()

    def show_main(self, username):
        """Showing the main UI"""
        self.current_user = username
        self.update_ui(self.current_user)

        # Create UI structure
        self.main_frame1 = customtkinter.CTkFrame(self, fg_color="grey")
        self.main_frame1.pack(side="left", expand=True, fill="both")

        self.main_frame2 = customtkinter.CTkFrame(self)
        self.main_frame2.pack(side="left", fill="both")

        # Create text box
        self.script_textbox = customtkinter.CTkTextbox(master=self.main_frame1, font=("arial", 14), fg_color="black")
        self.script_textbox.pack(side="top", padx=10, pady=10, expand=True, fill="both")

        # Initialize utility class after text box is created
        self.util = Utility(self.script_textbox, self.current_user)  

        # Buttons
        self.save_btn = customtkinter.CTkButton(self.main_frame2, fg_color="green", hover_color="dark green", text="Save")
        self.save_btn.pack(side="top", padx=10, pady=10)

        self.cmd_echo_btn = customtkinter.CTkButton(self.main_frame2, text="Echo", command=self.util.add_echo)
        self.cmd_echo_btn.pack(side="top", padx=10, pady=10)
    
    

app = App()
app.mainloop()
