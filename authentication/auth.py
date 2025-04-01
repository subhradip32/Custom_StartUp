import customtkinter 
import pickle as pk 
import os 

class authentication:
    def __init__(self, path = "./auth.txt"):
        if not os.path.exists(path=path):
            print("ok")



class AuthWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Authentication")
        self.resizable(False, False)

        # Set grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Title label
        self.title_lbl = customtkinter.CTkLabel(self, text="Login", font=("Arial", 22, "bold"))
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))

        # Username field
        self.username_ent = customtkinter.CTkEntry(self, placeholder_text="Enter Username", width=250)
        self.username_ent.grid(row=1, column=0, pady=10, padx=20)

        # Password field
        self.password_ent = customtkinter.CTkEntry(self, placeholder_text="Enter Password", show="*", width=250)
        self.password_ent.grid(row=2, column=0, pady=10, padx=20)

        # Remember Me Checkbox
        self.check_var = customtkinter.StringVar(value="on")
        self.check_remember = customtkinter.CTkCheckBox(
            self, text="Remember Me", variable=self.check_var, onvalue="on", offvalue="off"
        )
        self.check_remember.grid(row=3, column=0, pady=5)

        # Login button
        self.login_btn = customtkinter.CTkButton(
            self, text="Login", fg_color="#007BFF", hover_color="#0056b3", width=150
        )
        self.login_btn.grid(row=4, column=0, pady=20)

