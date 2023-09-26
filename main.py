#image_compression_using_dct
import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image, ImageTk
import os
import io

class ImageCompressionUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Image Compression with DCT")
        self.pack()

        # Create widgets
        self.load_btn = tk.Button(self, text="Load Image", command=self.load_image,height=4, width=20)
        self.load_btn.pack(side="top")

        self.compress_btn = tk.Button(self, text="Compress", command=self.compress_image,height=4, width=20)
        self.compress_btn.pack(side="top")

        self.save_btn = tk.Button(self, text="Save Image", command=self.save_image,height=4, width=20)
        self.save_btn.pack(side="top")


        self.status_label = tk.Label(self, text="Load an image to compress")
        self.status_label.pack(side="bottom")

        self.original_image_label = tk.Label(master)
        self.original_image_label.pack(side="left", padx=10, pady=10)

        self.original_image_size_label = tk.Label(master)
        self.original_image_size_label.pack(side="left",padx=10, pady=10)


        self.compressed_image_size_label = tk.Label(master,text="compressed image size")
        self.compressed_image_size_label.pack(side="right", padx=10, pady=10)

        self.compressed_image_label = tk.Label(master)
        self.compressed_image_label.pack(side="right",padx=10, pady=10)
        

        self.image = None
        self.compressed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            # Get size of the image
            size = os.path.getsize(file_path)
            size_kb = round(size / 1024, 2)
            size_mb = round(size_kb / 1024, 2)
            if size_mb > 1:
             self.original_image_size_label.config(text=f"Original Image Size: {size_mb} MB.")
            else:
             self.original_image_size_label.config(text=f"Original Image Size: {size_kb} KB.")
        

        # Resize the original image
        self.image1=self.image
        self.original_image_tk = ImageTk.PhotoImage(self.image.resize((300, 300), Image.BILINEAR))

        
        self.original_image_label.config(image=self.original_image_tk)
        self.original_image_label.config(width=self.image.width(), height=self.image.height)
        self.status_label.config(text="Image loaded. Click 'Compress' to compress it.")
        self.status_label.pack(side="right", anchor="w", padx=70, pady=70)
        self.save_btn.config(state="normal")

    def compress_image(self):
        if not self.image:
          self.status_label.config(text="Load an image first!")
          return
        
        # Convert the image to YCbCr color space
        img_ycbcr = self.image.convert("YCbCr")
        y, cb, cr = img_ycbcr.split()

        # Convert Y channel to numpy array
        y_arr = np.array(y)
        M, N = y_arr.shape

        # DCT transform
        dct_coef = dct(dct(y_arr.T, norm="ortho").T, norm="ortho")

        # Set lower frequency coefficients to zero to compress the image
        threshold = 0.1
        dct_coef[abs(dct_coef) < threshold] = 0

        # IDCT transform
        compressed_y_arr = idct(idct(dct_coef.T, norm="ortho").T, norm="ortho")

        # Create compressed Y channel image object
        compressed_y = Image.fromarray(np.uint8(compressed_y_arr))

        # Replace Y channel in YCbCr image with compressed Y channel
        compressed_ycbcr = Image.merge("YCbCr", (compressed_y, cb, cr))

        # Convert compressed YCbCr image back to RGB
        compressed_rgb = compressed_ycbcr.convert("RGB")

        # Update status and display compressed image
        #self.status_label.config(text=f"Compression complete")
        self.compressed_image_tk = ImageTk.PhotoImage(compressed_rgb.resize((300, 300), Image.BILINEAR))

        #self.compressed_image_tk = ImageTk.PhotoImage(compressed_rgb.resize((300, 300), Image.ANTIALIAS))
        self.compressed_image_label.config(image=self.compressed_image_tk)

        # Get size of the compressed image
        buffer = io.BytesIO()
        compressed_rgb.save(buffer, format="JPEG")
        size = buffer.getbuffer().nbytes
        size_kb = round(size / 1024, 2)
        size_mb = round(size_kb / 1024, 2)
        if size_mb > 1:
         self.compressed_image_size_label.config(text=f"Compressed image size: {size_mb} MB.")
        else:
         self.compressed_image_size_label.config(text=f" Compressed image size: {size_kb} KB.")

        # Save compressed image
        self.compressed_image = compressed_rgb




    def save_image(self):
        if not self.compressed_image:
            self.status_label.config(text="Compress an image first!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("JPEG", "*.jpeg"), ("JPEG", "*.jpg;*.jpeg")])
        if file_path:
            self.compressed_image.save(file_path)
            self.status_label.config(text="Image saved.")

root = tk.Tk()
app = ImageCompressionUI(root)
app.mainloop()

