import customtkinter



# basic setup
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x700")
        customtkinter.set_appearance_mode("System")  
        customtkinter.set_default_color_theme("blue")
        self.button_1 = customtkinter.CTkButton(self, text="open toplevel")
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None


app = App()
app.mainloop()