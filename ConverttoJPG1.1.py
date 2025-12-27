# -----------------------------------------------------------------------------
# Convert_to_JPG
# Copyright (C) 2025 Ayman Ali Shehab
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
import threading
from tkinter import Tk, filedialog, Label, Button, ttk, messagebox
from PIL import Image

class ImageConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Universal Image to JPG Converter")
        master.geometry("500x350")
        master.resizable(False, False)

        # Variables
        self.input_path = ""
        self.output_path = ""
        self.is_running = False
        self.stop_requested = False
        self.image_extensions = (
            '.png', '.jpeg', '.jpg', '.gif', '.bmp', '.tiff', '.tif', 
            '.webp', '.ico', '.pcx', '.pnm', '.ppm', '.pgm', '.pbm'
        )

        # UI Elements
        Label(master, text="Image Converter (Transparent to White JPG)", font=("Arial", 12, "bold")).pack(pady=10)

        # Input Selection
        self.btn_input = Button(master, text="Select Input Folder", command=self.select_input)
        self.btn_input.pack(pady=5)
        self.lbl_input = Label(master, text="No folder selected", fg="gray", wraplength=400)
        self.lbl_input.pack()

        # Output Selection
        self.btn_output = Button(master, text="Select Output Folder", command=self.select_output)
        self.btn_output.pack(pady=5)
        self.lbl_output = Label(master, text="No folder selected", fg="gray", wraplength=400)
        self.lbl_output.pack()

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.lbl_status = Label(master, text="Ready", fg="blue")
        self.lbl_status.pack()

        # Action Button (Start/Pause)
        self.btn_action = Button(master, text="Start Conversion", bg="green", fg="white", 
                                 width=20, height=2, command=self.toggle_conversion)
        self.btn_action.pack(pady=10)

    def select_input(self):
        self.input_path = filedialog.askdirectory()
        if self.input_path:
            self.lbl_input.config(text=self.input_path, fg="black")

    def select_output(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.lbl_output.config(text=self.output_path, fg="black")

    def toggle_conversion(self):
        if not self.input_path or not self.output_path:
            messagebox.showwarning("Selection Missing", "Please select both input and output folders.")
            return

        if not self.is_running:
            # Start Processing
            self.is_running = True
            self.stop_requested = False
            self.btn_action.config(text="Pause", bg="orange")
            self.lbl_status.config(text="Processing...")
            
            # Run in thread to keep GUI responsive
            threading.Thread(target=self.process_images, daemon=True).start()
        else:
            # Request Pause
            self.stop_requested = True
            self.is_running = False
            self.btn_action.config(text="Start Conversion", bg="green")
            self.lbl_status.config(text="Paused")

    def process_images(self):
        files = [f for f in os.listdir(self.input_path) if f.lower().endswith(self.image_extensions)]
        total_files = len(files)
        self.progress["maximum"] = total_files
        
        PURE_WHITE = (255, 255, 255)
        count = 0

        for filename in files:
            if self.stop_requested:
                break
            
            input_file = os.path.join(self.input_path, filename)
            name, _ = os.path.splitext(filename)
            output_file = os.path.join(self.output_path, f"{name}.jpg")

            try:
                img = Image.open(input_file)
                
                # Handle Transparency
                if 'A' in img.getbands() or img.mode == 'P':
                    img = img.convert('RGBA')
                
                if 'A' in img.getbands():
                    background = Image.new('RGB', img.size, PURE_WHITE)
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                img.save(output_file, 'JPEG', quality=95)
                
            except Exception as e:
                print(f"Error skipping {filename}: {e}")

            count += 1
            self.progress["value"] = count
            self.lbl_status.config(text=f"Converting: {count}/{total_files}")
            self.master.update_idletasks()

        if not self.stop_requested:
            self.is_running = False
            self.btn_action.config(text="Start Conversion", bg="green")
            self.lbl_status.config(text=f"Completed! {count} images processed.")
            messagebox.showinfo("Done", f"Successfully processed {count} images.")

if __name__ == "__main__":
    root = Tk()
    app = ImageConverterGUI(root)
    root.mainloop()