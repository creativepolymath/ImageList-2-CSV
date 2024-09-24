import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk

def images_to_csv(folder_path, output_csv):
    """
    Create a CSV file containing information about all images in a specified folder.
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    images = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(root, file)
                file_stats = os.stat(file_path)
                
                image_info = {
                    'filename': file,
                    'path': file_path,
                    'size_bytes': file_stats.st_size,
                    'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                images.append(image_info)
    
    if not images:
        return 0

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'path', 'size_bytes', 'last_modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for image in images:
            writer.writerow(image)
    
    return len(images)

class ImageToCsvApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="morph")
        self.title("Image Folder to CSV")
        self.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        # Folder selection
        folder_frame = ttk.Frame(self)
        folder_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(folder_frame, text="Image Folder:").pack(side='left')
        self.folder_entry = ttk.Entry(folder_frame)
        self.folder_entry.pack(side='left', expand=True, fill='x', padx=(10, 0))
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side='left', padx=(10, 0))

        # Output file selection
        output_frame = ttk.Frame(self)
        output_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(output_frame, text="Output CSV:").pack(side='left')
        self.output_entry = ttk.Entry(output_frame)
        self.output_entry.pack(side='left', expand=True, fill='x', padx=(10, 0))
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side='left', padx=(10, 0))

        # Generate button
        ttk.Button(self, text="Generate CSV", command=self.generate_csv).pack(pady=20)

        # Status label
        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def browse_output(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)

    def generate_csv(self):
        folder_path = self.folder_entry.get()
        output_csv = self.output_entry.get()

        if not folder_path or not output_csv:
            messagebox.showerror("Error", "Please select both an image folder and an output CSV file.")
            return

        try:
            image_count = images_to_csv(folder_path, output_csv)
            if image_count > 0:
                self.status_label.config(text=f"CSV created successfully. {image_count} images processed.")
                messagebox.showinfo("Success", f"CSV file created: {output_csv}\nTotal images found: {image_count}")
            else:
                self.status_label.config(text="No images found in the selected folder.")
                messagebox.showwarning("Warning", "No images found in the selected folder.")
        except Exception as e:
            self.status_label.config(text="An error occurred.")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = ImageToCsvApp()
    app.mainloop()