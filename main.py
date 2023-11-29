import tkinter
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter
import shutil
import os
import glob

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MSSS")
        self.geometry(f"{1100}x{580}")

        self.audio_files = {}
        self.chip_buttons = {}
        self.sound_labels = {}


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Smart Sound", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Help", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        # create textbox
        # Existing image setup
        self.shirts_image = Image.open("shirts.png")
        self.shirts_image_tk = ImageTk.PhotoImage(self.shirts_image)
        self.image_label = tkinter.Label(self, image=self.shirts_image_tk)
        self.image_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Additional image setup
        '''
        self.logo_image = Image.open("logo.png")
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tkinter.Label(self, image=self.logo_image_tk)
        self.logo_label.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        '''


        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Current file settings", label_text_color= "blue")
        self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        # Specify the folder path to explore
        folder_path = "C:/Users/jbara/Desktop/clips"

        # List all subdirectories (chip 1 to chip 13)
        subdirectories = [f"chip {i}" for i in range(1, 14)]

        for subdir_name in subdirectories:
            subdir_path = os.path.join(folder_path, subdir_name)
            if os.path.isdir(subdir_path):
                
                # Create a label to display the folder name using customtkinter.CTkLabel
                label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Contents of {subdir_name}")
                label.pack()

                # List files in the subdirectory
                for file_name in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, file_name)
                    if os.path.isfile(file_path):
                        # Display the file name using customtkinter.CTkLabel
                        file_label = customtkinter.CTkLabel(self.scrollable_frame, text=file_name)
                        file_label.pack()
        
##################################################################################################

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("RFID STATUS")
        # Create and add the upload button to the "Part Selected" tab
        self.upload_button = customtkinter.CTkButton(self.tabview.tab("RFID STATUS"), text="Status", command=self.sidebar_button_event)
        self.upload_button.pack(padx=20, pady=20) 
        
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        for i in range(1, 14):
            button = customtkinter.CTkButton(master=button_frame, text=f"Chip {i}",
                                             command=lambda i=i: self.select_audio_file(i))
            button.grid(row=i, column=0, pady=(5, 0), padx=20, sticky="nw")
            self.chip_buttons[i] = button

        self.upload_all_button = customtkinter.CTkButton(master=button_frame, text="Upload All",
                                                         command=self.upload_all_files)
        self.upload_all_button.grid(row=14, column=0, pady=(20, 0), padx=20, sticky="nw")

    def select_audio_file(self, chip_number):
        filetypes = [('Audio Files', '*.wav *.mp3 *.ogg *.flac')]
        filename = filedialog.askopenfilename(title="Select a file", initialdir="/",
                                                filetypes=filetypes)
        if filename:
            self.audio_files[chip_number] = filename
            self.chip_buttons[chip_number].configure(text=f"Chip {chip_number} ✓")

    def upload_all_files(self):
        base_folder = os.path.expanduser("C:/Users/jbara/Desktop/clips")

        for chip, filepath in self.audio_files.items():
            dest_folder = os.path.join(base_folder, f"chip {chip}")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            else:
                # Clear the contents of the folder
                for file in os.listdir(dest_folder):
                    os.remove(os.path.join(dest_folder, file))

            # Move the new file to the folder
            shutil.move(filepath, dest_folder)
            print(f"Moved {filepath} to {dest_folder}")

            # Reset the button text
            self.chip_buttons[chip].configure(text=f"Chip {chip}")

        # Clear the audio_files dictionary
        self.update_current_file_settings()
        self.audio_files.clear()

    
    def load_preset(self):
        preset_folder = filedialog.askdirectory(title="Select Preset Folder")
        if not preset_folder:
            return  # User cancelled the selection

        # Check if the preset folder contains chip subfolders
        for i in range(1, 14):
            chip_folder = os.path.join(preset_folder, f"chip {i}")
            if not os.path.exists(chip_folder):
                print(f"Missing folder: {chip_folder}")
                return  # Preset folder is not valid
        self.update_current_file_settings()

        # Copy contents to the clips folder
        clips_folder = os.path.expanduser("~/Desktop/clips")
        for i in range(1, 14):
            chip_folder = os.path.join(preset_folder, f"chip {i}")
            dest_folder = os.path.join(clips_folder, f"chip {i}")

            if os.path.exists(dest_folder):
                shutil.rmtree(dest_folder)  # Remove existing contents

            shutil.copytree(chip_folder, dest_folder)  # Copy new contents
            print(f"Copied from {chip_folder} to {dest_folder}")

    def update_current_file_settings(self):
        # Clear existing content in scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Specify the folder path to explore
        folder_path = "C:/Users/jbara/Desktop/clips"

        # List all subdirectories (chip 1 to chip 13)
        subdirectories = [f"chip {i}" for i in range(1, 14)]

        for subdir_name in subdirectories:
            subdir_path = os.path.join(folder_path, subdir_name)
            if os.path.isdir(subdir_path):
                # Create a label to display the folder name
                label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Contents of {subdir_name}")
                label.pack()

                # List files in the subdirectory
                for file_name in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, file_name)
                    if os.path.isfile(file_path):
                        # Display the file name
                        file_label = customtkinter.CTkLabel(self.scrollable_frame, text=file_name)
                        file_label.pack()
    def sidebar_button_event(self):
        print("sidebar_button click")

if __name__ == "__main__":
    app = App()
    app.mainloop()