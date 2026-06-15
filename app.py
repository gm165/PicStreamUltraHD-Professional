import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageTk
from rembg import remove

# UI Theme Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Professional App Branding
        self.title("PicStreamUltraHD Professional By: GM Tech Solutions")
        self.geometry("900x650")
        self.iconbitmap("app_icon.ico")
        self.resizable(True, True)

        # Variables
        self.input_path = ""
        self.input_folder = ""
        self.bg_color_rgb = (255, 255, 255) # Default White
        self.preview_img_obj = None

        self.create_widgets()

    def create_widgets(self):
        # --- Upper Title ---
        self.title_label = ctk.CTkLabel(self, text="PicStreamUltraHD Professional", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)
        
        self.subtitle_label = ctk.CTkLabel(self, text="Powered by GM Tech Solutions", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
        self.subtitle_label.pack(pady=0)

        # --- Tab View (Single vs Bulk vs About Us) ---
        self.tab_view = ctk.CTkTabview(self, width=860, height=530)
        self.tab_view.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.tab_single = self.tab_view.add("Single Image Mode")
        self.tab_bulk = self.tab_view.add("Bulk / Folder Mode")
        self.tab_about = self.tab_view.add("About Us")

        self.setup_single_mode()
        self.setup_bulk_mode()
        self.setup_about_tab()

    # ================= SINGLE IMAGE MODE =================
    def setup_single_mode(self):
        # Left Side: Controls
        self.left_frame = ctk.CTkFrame(self.tab_single, width=400, height=430)
        self.left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.file_btn = ctk.CTkButton(self.left_frame, text="📁 Select Image", command=self.browse_image, fg_color="#2b81d6", font=ctk.CTkFont(weight="bold"))
        self.file_btn.pack(pady=15, padx=20, fill="x")

        self.path_label = ctk.CTkLabel(self.left_frame, text="No file selected...", text_color="gray", wraplength=350)
        self.path_label.pack(pady=5, padx=20)

        # Options
        self.options_frame = ctk.CTkFrame(self.left_frame, corner_radius=10)
        self.options_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkLabel(self.options_frame, text="Background Mode:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.bg_option = ctk.CTkComboBox(self.options_frame, values=["White Background", "Keep Original", "Custom Color"], command=self.toggle_color_button)
        self.bg_option.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Color Picker Button - Fixed (Replaced fill="x" with sticky="ew")
        self.color_btn = ctk.CTkButton(self.options_frame, text="🎨 Choose Color", command=self.pick_color, fg_color="#6c757d", state="disabled")
        self.color_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Format
        ctk.CTkLabel(self.options_frame, text="Output Format:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ext_option = ctk.CTkComboBox(self.options_frame, values=["JPG", "PNG", "WEBP"])
        self.ext_option.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Target Size info
        self.size_info = ctk.CTkLabel(self.left_frame, text="Target File Size: Smart Auto-Optimize (≤ 19 KB)", text_color="#24a0ed", font=ctk.CTkFont(size=12, weight="bold"))
        self.size_info.pack(pady=5)

        self.process_btn = ctk.CTkButton(self.left_frame, text="🚀 Process & Save Image", command=self.process_single_image, fg_color="#2eb872", hover_color="#1da05e", height=40, font=ctk.CTkFont(size=15, weight="bold"))
        self.process_btn.pack(pady=15, padx=20, fill="x")

        # Right Side: Live Preview
        self.right_frame = ctk.CTkFrame(self.tab_single, width=420, height=430)
        self.right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.preview_title = ctk.CTkLabel(self.right_frame, text="Live Image Preview", font=ctk.CTkFont(weight="bold"))
        self.preview_title.pack(pady=10)

        self.preview_label = ctk.CTkLabel(self.right_frame, text="[ Image Preview Area ]", text_color="gray", width=380, height=320, fg_color=("#dbdbdb", "#2b2b2b"), corner_radius=8)
        self.preview_label.pack(pady=10, padx=20)

    # ================= BULK / FOLDER MODE =================
    def setup_bulk_mode(self):
        self.bulk_frame = ctk.CTkFrame(self.tab_bulk)
        self.bulk_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.folder_btn = ctk.CTkButton(self.bulk_frame, text="📂 Select Input Folder", command=self.browse_folder, fg_color="#2b81d6", font=ctk.CTkFont(weight="bold"))
        self.folder_btn.pack(pady=20, padx=50, fill="x")

        self.folder_label = ctk.CTkLabel(self.bulk_frame, text="No folder selected...", text_color="gray", wraplength=600)
        self.folder_label.pack(pady=5)

        # Bulk Settings
        self.bulk_opt_frame = ctk.CTkFrame(self.bulk_frame)
        self.bulk_opt_frame.pack(pady=20, padx=50, fill="x")

        ctk.CTkLabel(self.bulk_opt_frame, text="Bulk Background:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.bulk_bg_option = ctk.CTkComboBox(self.bulk_opt_frame, values=["White Background", "Keep Original", "Custom Color"], command=self.toggle_bulk_color_button)
        self.bulk_bg_option.grid(row=0, column=1, padx=20, pady=15, sticky="w")

        self.bulk_color_btn = ctk.CTkButton(self.bulk_opt_frame, text="🎨 Choose Bulk Color", command=self.pick_color, fg_color="#6c757d", state="disabled")
        self.bulk_color_btn.grid(row=0, column=2, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(self.bulk_opt_frame, text="Bulk Format:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=20, pady=15, sticky="w")
        self.bulk_ext_option = ctk.CTkComboBox(self.bulk_opt_frame, values=["JPG", "PNG", "WEBP"])
        self.bulk_ext_option.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        # Progress Label
        self.progress_label = ctk.CTkLabel(self.bulk_frame, text="Status: Ready", font=ctk.CTkFont(weight="bold"), text_color="#24a0ed")
        self.progress_label.pack(pady=10)

        self.bulk_process_btn = ctk.CTkButton(self.bulk_frame, text="⚡ Start Bulk Processing", command=self.process_bulk_images, fg_color="#2eb872", hover_color="#1da05e", height=45, font=ctk.CTkFont(size=16, weight="bold"))
        self.bulk_process_btn.pack(pady=20, padx=50, fill="x")

    # ================= ABOUT US TAB =================
    def setup_about_tab(self):
        self.about_frame = ctk.CTkFrame(self.tab_about, corner_radius=15)
        self.about_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Company Name
        about_title = ctk.CTkLabel(self.about_frame, text="GM Tech Solutions", font=ctk.CTkFont(size=26, weight="bold"), text_color="#2b81d6")
        about_title.pack(pady=(30, 10))

        # Software Version Block
        version_label = ctk.CTkLabel(self.about_frame, text="Software: PicStreamUltraHD Professional\nVersion: 2.5 (Stable Build)", font=ctk.CTkFont(size=14, weight="bold"))
        version_label.pack(pady=10)

        # Description text
        desc_text = (
            "PicStreamUltraHD is an advanced enterprise-grade utility tool designed for instant "
            "AI-powered background removal, image format conversion, and automated file-size "
            "optimization. Engineered to strictly maintain constraints under 19KB for professional "
            "and official portal uploads while retaining maximum possible resolution."
        )
        desc_label = ctk.CTkLabel(self.about_frame, text=desc_text, font=ctk.CTkFont(size=13), wraplength=650, justify="center")
        desc_label.pack(pady=20, padx=40)

        # Separation Line
        sep_label = ctk.CTkLabel(self.about_frame, text="----------------------------------------------------------------", text_color="gray")
        sep_label.pack(pady=5)

        # Footer Copyright
        copyright_label = ctk.CTkLabel(self.about_frame, text="© 2026 GM Tech Solutions. All Rights Reserved.\nDesigned for high compatibility from Windows 7 up to Windows 11.", font=ctk.CTkFont(size=11), text_color="gray")
        copyright_label.pack(pady=15)

    # ================= LOGIC & UTILITIES =================
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp")])
        if file_path:
            self.input_path = file_path
            self.path_label.configure(text=os.path.basename(file_path), text_color=["black", "white"])
            self.show_preview(file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_folder = folder_path
            self.folder_label.configure(text=folder_path, text_color=["black", "white"])

    def show_preview(self, path):
        img = Image.open(path)
        img.thumbnail((360, 300))
        self.preview_img_obj = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=self.preview_img_obj, text="")

    def toggle_color_button(self, value):
        if value == "Custom Color":
            self.color_btn.configure(state="normal", fg_color="#2b81d6")
        else:
            self.color_btn.configure(state="disabled", fg_color="#6c757d")

    def toggle_bulk_color_button(self, value):
        if value == "Custom Color":
            self.bulk_color_btn.configure(state="normal", fg_color="#2b81d6")
        else:
            self.bulk_color_btn.configure(state="disabled", fg_color="#6c757d")

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Select Background Color")
        if color_code[0]:
            self.bg_color_rgb = tuple(map(int, color_code[0]))
            hex_color = color_code[1]
            if self.bg_option.get() == "Custom Color":
                self.color_btn.configure(fg_color=hex_color)
            if self.bulk_bg_option.get() == "Custom Color":
                self.bulk_color_btn.configure(fg_color=hex_color)

    def remove_background(self, img, bg_mode):
        if bg_mode == "Keep Original":
            return img.convert("RGBA")
        
        no_bg = remove(img)
        
        if bg_mode == "White Background":
            bg_color = (255, 255, 255, 255)
        elif bg_mode == "Custom Color":
            bg_color = (self.bg_color_rgb[0], self.bg_color_rgb[1], self.bg_color_rgb[2], 255)
        else:
            bg_color = (255, 255, 255, 255)

        background = Image.new("RGBA", no_bg.size, bg_color)
        background.paste(no_bg, (0, 0), no_bg)
        return background

    def save_under_19kb(self, img, output_path, ext):
        quality = 95
        if ext in ["JPG", "JPEG"]:
            img = img.convert("RGB")
            fmt = "JPEG"
        elif ext == "WEBP":
            img = img.convert("RGB")
            fmt = "WEBP"
        else:
            fmt = "PNG"

        img.save(output_path, format=fmt, quality=quality)
        
        while os.path.getsize(output_path) > 19456 and quality > 10:
            if fmt == "PNG":
                w, h = img.size
                img = img.resize((int(w * 0.9), int(h * 0.9)), Image.Resampling.LANCZOS)
                img.save(output_path, format=fmt)
                if img.size[0] < 100: break
            else:
                quality -= 5
                img.save(output_path, format=fmt, quality=quality)

    def process_single_image(self):
        if not self.input_path:
            messagebox.showerror("Error", "Pehle koi image select karen!")
            return

        bg_mode = self.bg_option.get()
        target_ext = self.ext_option.get().lower()

        save_path = filedialog.asksaveasfilename(defaultextension=f".{target_ext}", filetypes=[(f"{target_ext.upper()} File", f"*.{target_ext}")])
        if not save_path: return

        try:
            img = Image.open(self.input_path)
            processed_img = self.remove_background(img, bg_mode)
            self.save_under_19kb(processed_img, save_path, target_ext.upper())
            
            final_size = os.path.getsize(save_path) / 1024
            messagebox.showinfo("Success", f"Image kamyabi sy save ho gai hai!\nFinal Size: {final_size:.2f} KB")
        except Exception as e:
            messagebox.showerror("Error", f"Kuch ghalti hoi: {str(e)}")

    def process_bulk_images(self):
        if not self.input_folder:
            messagebox.showerror("Error", "Pehle Input Folder select karen!")
            return

        output_folder = os.path.join(self.input_folder, "Optimized_Outputs")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        bg_mode = self.bulk_bg_option.get()
        target_ext = self.bulk_ext_option.get().lower()

        all_files = os.listdir(self.input_folder)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
        image_files = [f for f in all_files if f.lower().endswith(valid_extensions)]

        if not image_files:
            messagebox.showinfo("No Images", "Is folder mien koi tasveer nahi mili!")
            return

        success_count = 0
        total_files = len(image_files)

        for i, filename in enumerate(image_files):
            try:
                self.progress_label.configure(text=f"Processing {i+1}/{total_files}: {filename}", text_color="orange")
                self.update_idletasks()

                input_file_path = os.path.join(self.input_folder, filename)
                raw_name, _ = os.path.splitext(filename)
                output_file_path = os.path.join(output_folder, f"{raw_name}_optimized.{target_ext}")

                img = Image.open(input_file_path)
                processed_img = self.remove_background(img, bg_mode)
                self.save_under_19kb(processed_img, output_file_path, target_ext.upper())
                
                success_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

        self.progress_label.configure(text="Status: Completed!", text_color="#2eb872")
        messagebox.showinfo("Bulk Done", f"Mukammal ho gaya!\n{success_count} out of {total_files} images process ho kar '{os.path.basename(output_folder)}' folder mien save ho gayi hain.")

if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()