import customtkinter
from authentication import auth 

# basic setup
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x700")
        customtkinter.set_appearance_mode("System")  
        customtkinter.set_default_color_theme("blue")
        self.title("Custom Startup")

        self.button_1 = customtkinter.CTkButton(self, text="Open Toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.AuthWindow = None
    
    def open_toplevel(self):
        if self.AuthWindow is None or not self.AuthWindow.winfo_exists():
            self.AuthWindow = auth.AuthWindow(self)  # Create window if it's None or destroyed
            self.AuthWindow.grab_set()  # Prevent interaction with root until Toplevel is closed
        else:
            self.AuthWindow.focus()  # If window exists, bring it to focus

app = App()
app.mainloop()
