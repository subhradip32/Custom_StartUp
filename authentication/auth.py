import customtkinter
import pickle as pk
import os
import time

class Authentication:
    def __init__(self, auth_window, main_window, path="./auth.data"):
        self.filepath = path
        self.auth_window = auth_window  
        self.main_window = main_window  # Store reference to main window

        if not os.path.exists(path):  
            with open(path, "wb") as file:
                pk.dump({}, file)

    def check_user(self, username, password, remember_me, lbl) -> bool:
        try:
            with open(self.filepath, "rb") as file:
                data = pk.load(file)

            if not isinstance(data, dict):
                lbl.configure(text="Authentication data corrupted!", text_color="red")
                return False

            if username in data:
                stored_password, _, last_logged_time = data[username]  
                if stored_password == password:
                    lbl.configure(text=f"Logged in as {username}", text_color="green")
                    data[username] = (password, remember_me, time.time())  
                    with open(self.filepath, "wb") as file:
                        pk.dump(data, file)
                    
                    self.main_window.show_main(username = username)  # Update main window
                    self.auth_window.destroy()  
                    return True
                else:
                    lbl.configure(text="Invalid username or password", text_color="red")
                    return False
            else:
                # Register a new user
                data[username] = (password, remember_me, time.time())
                with open(self.filepath, "wb") as file:
                    pk.dump(data, file)
                lbl.configure(text=f"New account created for {username}", text_color="yellow")
                self.main_window.show_main()  # Update main window
                self.auth_window.destroy()  
                return True

        except (EOFError, pk.UnpicklingError):  
            lbl.configure(text="Error reading auth file", text_color="red")
            return False

    def verify_login(self, userent, pass_ent, check_remember, display_lbl):
        username = userent.get()
        password = pass_ent.get()
        remember_me = 1 if check_remember.get() == "on" else 0  

        if not username or not password:
            display_lbl.configure(text="Please enter username & password", text_color="red")
            return
        
        self.check_user(username, password, remember_me, display_lbl)


class AuthWindow(customtkinter.CTkToplevel):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window  # Store reference to main window
        self.geometry("400x300")
        self.title("Authentication")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = customtkinter.CTkLabel(self, text="Login", font=("Arial", 22, "bold"))
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))

        self.username_ent = customtkinter.CTkEntry(self, placeholder_text="Enter Username", width=250)
        self.username_ent.grid(row=1, column=0, pady=10, padx=20)

        self.password_ent = customtkinter.CTkEntry(self, placeholder_text="Enter Password", show="*", width=250)
        self.password_ent.grid(row=2, column=0, pady=10, padx=20)

        self.check_var = customtkinter.StringVar(value="off")  
        self.check_remember = customtkinter.CTkCheckBox(
            self, text="Remember Me", variable=self.check_var, onvalue="on", offvalue="off"
        )
        self.check_remember.grid(row=3, column=0, pady=5)

        self.verification_lbl = customtkinter.CTkLabel(self, text="", font=("Arial", 14))
        self.verification_lbl.grid(row=5, column=0, pady=(10, 10))

        auth = Authentication(self, main_window)  
        self.login_btn = customtkinter.CTkButton(
            self, text="Login", fg_color="#007BFF", hover_color="#0056b3", width=150,
            command=lambda: auth.verify_login(
                self.username_ent, self.password_ent, self.check_var, self.verification_lbl
            )
        )
        self.login_btn.grid(row=4, column=0, pady=20)
