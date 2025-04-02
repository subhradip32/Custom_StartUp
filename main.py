import customtkinter
from authentication import auth
import pickle as pk
import os

# Global values
AUTH_FILEPATH = "./auth.data"

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

        self.label = customtkinter.CTkLabel(self, text="", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        if self.logged_in:
            self.update_ui(self.current_user)
        else:
            self.show_login_button()

    def show_login_button(self):
        """Display the login button when no user is logged in."""
        self.label.configure(text="Welcome! Please log in.")
        self.button_1 = customtkinter.CTkButton(self, text="Login", command=self.open_toplevel)
        self.button_1.pack(pady=20)
    
    def logout_user(self):
        self.AuthWindow = None
        self.current_user, self.logged_in = "", False 
        if hasattr(self, "button_2"):  # Hide login button if present
            self.button_2.pack_forget()


        self.show_login_button()
        pass

    def update_ui(self, username):
        """Update the main window after a successful login."""
        self.label.configure(text=f"Welcome Back, {username}!")
        if hasattr(self, "button_1"):  # Hide login button if present
            self.button_1.pack_forget()
        
        # Adding the logout button and feature
        self.button_2 = customtkinter.CTkButton(self, text="Logout", command=self.logout_user, 
                                                fg_color ="red", hover_color = "#8B0000")
        self.button_2.pack(pady=20)

    def open_toplevel(self):
        """Open the authentication window."""
        if self.AuthWindow is None or not self.AuthWindow.winfo_exists():
            self.AuthWindow = auth.AuthWindow(self)  # Pass self to AuthWindow
            self.AuthWindow.grab_set()
        else:
            self.AuthWindow.focus()

app = App()
app.mainloop()
