import customtkinter
from customtkinter import filedialog
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
    
    def clear_text(self):
        if self.code_area: 
            self.code_area.delete("1.0",customtkinter.END)
            self.text_status(self.status_lbl)

    def open_file(self):
        if self.code_area: 
            self.code_area.delete("1.0",customtkinter.END)
            bat_file = filedialog.askopenfilename(
                filetypes=[("Bash Files", "*.bat")] 
            )
            if bat_file:
                with open(bat_file, "r") as file:
                    data = file.read()
                self.code_area.insert("end", data)
            self.text_status(self.status_lbl)

    def save_as(self):
        if self.code_area:
            bat_path = filedialog.asksaveasfilename(defaultextension=".bat",
                                                    filetypes=[("Batch Files", "*.bat")])
            if bat_path:
                with open(bat_path, "w") as file:
                    file.write(self.code_area.get("1.0", "end"))
    
    def text_status(self, status_label : customtkinter.CTkLabel):
        """
        Generates a summary with line count, word count, and character count.
        Parameters:
            data (str): The input text.
        Returns:
            str: Summary string for status bar.
        """
        self.status_lbl = status_label
        data = self.code_area.get("1.0", customtkinter.END)
        lines = data.strip().split('\n')
        line_count = len(lines) if data.strip() else 0
        word_count = len(data.split())
        char_count = len(data)
    
        staus_line =  f"Lines: {line_count}  |  Words: {word_count}  |  Chars: {char_count-1}"
        status_label.configure(text = staus_line)
        

    def add_echo(self): 
        if self.code_area:
            self.code_area.insert("end", "echo \"Write a message you want to display\"\n")
            self.text_status(self.status_lbl)

    


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
        

        if self.logged_in:
            self.show_main(self.current_user)
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
        
        self.button_2 = customtkinter.CTkButton(self.last_frame, text="Logout", command=self.logout_user, 
                                                fg_color="red", hover_color="#8B0000")
        self.button_2.pack(side = "left")

    def open_toplevel(self):
        """Open the authentication window."""
        if self.AuthWindow is None or not self.AuthWindow.winfo_exists():
            self.AuthWindow = auth.AuthWindow(self)  
            self.AuthWindow.grab_set()
        else:
            self.AuthWindow.focus()

    def show_main(self, username):
        """Showing the main UI"""
        # Container for the two side-by-side frames
        self.current_user = username

        self.main_container = customtkinter.CTkFrame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # Left frame
        self.main_frame1 = customtkinter.CTkFrame(self.main_container, fg_color="grey")
        self.main_frame1.pack(side="left", expand=True, fill="both")

        # Right frame
        self.main_frame2 = customtkinter.CTkFrame(self.main_container)
        self.main_frame2.pack(side="left", fill="both")

        # Your textbox inside main_frame1
        self.script_textbox = customtkinter.CTkTextbox(master=self.main_frame1, font=("arial", 14), fg_color="black")
        self.script_textbox.pack(side="top", padx=10, pady=10, expand=True, fill="both")

        # Init utility
        self.util = Utility(self.script_textbox, self.current_user)
        

        # Buttons inside main_frame2
        self.save_btn = customtkinter.CTkButton(self.main_frame2, fg_color="green", hover_color="dark green",
                                                command=self.util.save_as, text="Save As")
        self.save_btn.pack(side="top", padx=5, pady=5)

        self.open_btn = customtkinter.CTkButton(self.main_frame2, fg_color="green", hover_color="dark green", 
                                                command=self.util.open_file,text="Open")
        self.open_btn.pack(side="top", padx=5, pady=5)

        self.cmd_echo_btn = customtkinter.CTkButton(self.main_frame2, text="Echo", command=self.util.add_echo)
        self.cmd_echo_btn.pack(side="top", padx=10, pady=15)

        self.clear_btn = customtkinter.CTkButton(self.main_frame2, fg_color="red", hover_color="dark red", 
                                                command=self.util.clear_text,text="Clear")
        self.clear_btn.pack(side="bottom", padx=10, pady=10)

        # Label at bottom of the whole UI
        self.last_frame = customtkinter.CTkFrame(self)
        self.last_frame.pack(side = "bottom", fill = "both", padx = 10, pady = 10)
        
        self.work_display = customtkinter.CTkLabel(self.last_frame, text="")
        self.work_display.pack(side="right")
        self.util.text_status(self.work_display)
        # self.script_textbox.bind("<KeyRelease>", self.util.text_status(self.work_display)) 
        self.script_textbox.bind("<KeyRelease>", lambda event: self.util.text_status(self.work_display))



        self.update_ui(self.current_user)
            

app = App()
app.mainloop()
