import os
import shutil
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

class ImageMover:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Mover")

        # Initialize directories
        self.source_directory = r"C:\Users\Russ\Documents\AI_Image\Renders\Newfolder_14"
        print("Selected source directory:", self.source_directory)
        print("Does the directory exist?", os.path.exists(self.source_directory))
        files_and_directories = os.listdir(self.source_directory)
        #for item in files_and_directories:
        #    print(item)



        self.destination_directory1 = None
        self.destination_directory2 = None

        # Image handling
        self.images = []
        self.current_image_path = None
        self.current_image_index = -1


        # GUI setup
        '''


        self.image_label = Label(master)
        self.image_label.pack(pady=20)

        Button(master, text="Select Source Directory", command=self.select_source_directory).pack()
        Button(master, text="Select Destination Directory 1", command=lambda: self.select_destination_directory(1)).pack()
        Button(master, text="Select Destination Directory 2", command=lambda: self.select_destination_directory(2)).pack()
        Button(master, text="Next Image", command=self.load_next_image).pack()
        Button(master, text="Move to Destination 1", command=lambda: self.move_image(1)).pack(side='left', padx=50, pady=20)
        Button(master, text="Move to Destination 2", command=lambda: self.move_image(2)).pack(side='right', padx=50, pady=20)
        '''

        self.label = Label(master, text="Select source and destination directories")
        self.label.grid(row=7, column=0, columnspan=2, sticky='ew')  # Adjust grid parameters as needed

        # Configure grid columns
        self.master.grid_columnconfigure(0, weight=1)  # Image column
        self.master.grid_columnconfigure(1, weight=0)  # Buttons column

        # Setup for image label
        self.image_label = Label(master)
        self.image_label.grid(row=0, column=0, sticky="nsew", rowspan=6)  # Ensure rowspan covers the height of all button rows

        # Setup buttons
        Button(master, text="Select Source Directory", command=self.select_source_directory).grid(row=0, column=1, sticky="ew")
        Button(master, text="Select Destination Directory 1", command=lambda: self.select_destination_directory(1)).grid(row=1, column=1, sticky="ew")
        Button(master, text="Select Destination Directory 2", command=lambda: self.select_destination_directory(2)).grid(row=2, column=1, sticky="ew")
        Button(master, text="Next Image", command=self.load_next_image).grid(row=3, column=1, sticky="ew")
        Button(master, text="Move to Destination 1", command=lambda: self.move_image(1)).grid(row=4, column=1, sticky="ew")
        Button(master, text="Move to Destination 2", command=lambda: self.move_image(2)).grid(row=5, column=1, sticky="ew")

        # Bind arrow keys for moving images
        self.master.bind('<Left>', lambda event: self.move_image(1))
        self.master.bind('<Right>', lambda event: self.move_image(2))
        
        # Configure rows for buttons to not expand
        for i in range(7):
            self.master.grid_rowconfigure(i, weight=0)

        # Add an empty row at the end that takes up any extra space
        self.master.grid_rowconfigure(7, weight=1)  # This row will absorb all extra vertical space

    def select_source_directory(self):
        self.source_directory = filedialog.askdirectory()
        if self.source_directory:
            all_files = os.listdir(self.source_directory)
            #print("All files in directory:", all_files)
            self.images = [os.path.join(self.source_directory, f) for f in os.listdir(self.source_directory) if f.endswith('.png')]
            #print("Filtered image files:", self.images)
            self.current_image_index = -1
            self.load_next_image()

    def select_destination_directory(self, number):
        if number == 1:
            self.destination_directory1 = filedialog.askdirectory()
        else:
            self.destination_directory2 = filedialog.askdirectory()

    def load_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.current_image_path = self.images[self.current_image_index]
            img = Image.open(self.current_image_path)

            # Get the size of the image
            width, height = img.size

            # Optionally resize if the image is larger than a certain size or screen
            max_width = self.master.winfo_screenwidth()
            max_height = self.master.winfo_screenheight()
            if width > max_width or height > max_height:
                # Maintain aspect ratio
                ratio = min(max_width/width, max_height/height)
                img = img.resize((int(width * ratio), int(height * ratio)), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference to avoid garbage collection
            self.label.config(text=f"Previewing: {os.path.basename(self.current_image_path)}")
        else:
            self.label.config(text="No more images or no images to display.")
            self.master.quit()

    def load_next_imagex(self):
        print("Selected source directory:", self.source_directory)
        print("self.current_image_index:", self.current_image_index)
        print("len(self.images):", len(self.images))

        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.current_image_path = self.images[self.current_image_index]
            img = Image.open(self.current_image_path)
            img.thumbnail((600, 400), Image.ANTIALIAS)  # Resize the image
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference!
            self.label.config(text=f"Previewing: {os.path.basename(self.current_image_path)}")
        else:
            self.label.config(text="No more images or no images to display.")
            self.master.quit()

    def move_image(self, destination):
        if destination == 1:
            dest_path = self.destination_directory1
        elif destination == 2:
            dest_path = self.destination_directory2
        else:
            self.label.config(text="Destination directory not set.")
            return

        # Check if the file still exists
        if os.path.exists(self.current_image_path):
            try:
                shutil.move(self.current_image_path, os.path.join(dest_path, os.path.basename(self.current_image_path)))
                self.label.config(text=f"Moved to {dest_path}.")
                self.load_next_image()
            except Exception as e:
                self.label.config(text=f"Error moving file: {e}")
        else:
            self.label.config(text="File not found. It may have been moved or deleted.")
            self.load_next_image()

    def move_imagex(self, destination):
        if destination == 1 and self.destination_directory1:
            dest_path = self.destination_directory1
        elif destination == 2 and self.destination_directory2:
            dest_path = self.destination_directory2
        else:
            self.label.config(text="Destination directory not set.")
            return

        shutil.move(self.current_image_path, os.path.join(dest_path, os.path.basename(self.current_image_path)))
        self.load_next_image()

if __name__ == "__main__":
    root = Tk()
    app = ImageMover(root)
    root.mainloop()
