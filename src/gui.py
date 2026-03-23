import os
import threading
import queue
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from .config import FORMATS_IMAGE, FORMATS_VIDEO
from .utils import is_image, is_video, MOVIEPY_AVAILABLE, MOVIEPY_ERROR
from .server import file_queue
from .core_conversion import convert_file

class FileRow(ctk.CTkFrame):
    def __init__(self, master, file_path, remove_callback):
        super().__init__(master)
        self.file_path = file_path
        self.remove_callback = remove_callback
        
        # Determine type (VIDEO/IMAGE/OTHER)
        self.packet_type = "UNKNOWN"
        if is_video(file_path):
             self.packet_type = "VIDEO"
             self.formats = FORMATS_VIDEO
             default_val = ".mp4"
             type_symbol = "🎬"
        elif is_image(file_path):
             self.packet_type = "IMAGE"
             self.formats = FORMATS_IMAGE
             default_val = ".jpg"
             type_symbol = "📷"
        else:
             self.packet_type = "OTHER"
             self.formats = []
             default_val = ""
             type_symbol = "📄"

        # Layout: Column 0 for icon, Column 1 (weight=1) for name, Column 2/3 for controls
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1)

        # Icon
        self.lbl_icon = ctk.CTkLabel(self, text=type_symbol, width=30, font=("Segoe UI", 16))
        self.lbl_icon.grid(row=0, column=0, padx=5, pady=5)
        
        # Filename
        filename = os.path.basename(file_path)
        if len(filename) > 40:
            filename = filename[:37] + "..."
        
        self.lbl_name = ctk.CTkLabel(self, text=filename, anchor="w", font=("Segoe UI", 13))
        self.lbl_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.combo = ctk.CTkComboBox(self, values=self.formats, width=100)
        if default_val:
            self.combo.set(default_val)
        self.combo.grid(row=0, column=2, padx=10, pady=5)

        self.btn_remove = ctk.CTkButton(self, text="X", width=30, fg_color="#FF5555", hover_color="#CC0000", command=self.remove)
        self.btn_remove.grid(row=0, column=3, padx=10, pady=5)

        self.preview_window = None
        self.is_hovering = False
        
        if self.packet_type == "IMAGE":
            # Start hover check on Enter
            for w in [self, self.lbl_icon, self.lbl_name]:
                w.bind("<Enter>", self.on_start_hover)

    def on_start_hover(self, event):
        if self.is_hovering: return
        self.is_hovering = True
        self.show_preview()
        self.monitor_hover()

    def monitor_hover(self):
        if not self.is_hovering: return
        
        try:
            if not self.winfo_exists():
                return
                
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            
            fx = self.winfo_rootx()
            fy = self.winfo_rooty()
            fw = self.winfo_width()
            fh = self.winfo_height()
            
            # Check if mouse is still roughly inside the row
            if not (fx <= x <= fx + fw and fy <= y <= fy + fh):
                self.stop_hover()
            else:
                self.after(100, self.monitor_hover)
        except Exception:
            self.stop_hover()

    def stop_hover(self):
        self.is_hovering = False
        self.hide_preview()

    def show_preview(self):
        if self.preview_window: return
        try:
            self.preview_window = ctk.CTkToplevel(self)
            self.preview_window.wm_overrideredirect(True)
            self.preview_window.attributes("-topmost", True)
            
            # Load and Resize Image
            img = Image.open(self.file_path)
            img.thumbnail((300, 300))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            label = ctk.CTkLabel(self.preview_window, image=ctk_img, text="")
            label.pack(padx=2, pady=2)
            
            self.preview_window.configure(fg_color="#333333") 

            x = self.winfo_pointerx() + 20
            y = self.winfo_pointery() + 20
            self.preview_window.geometry(f"+{x}+{y}")
            
        except Exception:
            self.hide_preview()

    def hide_preview(self):
        if self.preview_window:
            self.preview_window.destroy()
            self.preview_window = None

    def remove(self):
        self.stop_hover()
        self.remove_callback(self)

    def get_target_ext(self):
        return self.combo.get()

class App(ctk.CTk):
    def __init__(self, initial_files=None):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.title("Convertisseur Média Pro")
        self.geometry("700x500")
        
        self.rows = [] 
        
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_top, text="Fichiers sélectionnés", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(frame_top, text="+ Ajouter", command=self.browse_files, width=100).pack(side="right", padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        frame_bottom = ctk.CTkFrame(self)
        frame_bottom.pack(fill="x", padx=10, pady=10)

        # "Global" Settings logic
        ctk.CTkLabel(frame_bottom, text="Tout mettre en :").pack(side="left", padx=10)
        
        all_formats = sorted(list(set(FORMATS_IMAGE + FORMATS_VIDEO)))
        self.combo_global = ctk.CTkComboBox(frame_bottom, values=all_formats, width=100)
        self.combo_global.set("...")
        self.combo_global.pack(side="left", padx=5)
        
        ctk.CTkButton(frame_bottom, text="Appliquer", width=80, command=self.apply_global_format).pack(side="left", padx=5)

        # Action Button
        self.btn_convert = ctk.CTkButton(frame_bottom, text="CONVERTIR TOUT", fg_color="#2CC985", hover_color="#229966", font=("Segoe UI", 14, "bold"), command=self.process_all)
        self.btn_convert.pack(side="right", padx=10, pady=5)
        
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=10, pady=(0, 10))

        if initial_files:
            if isinstance(initial_files, list):
                for f in initial_files:
                    self.add_file(f)
            else:
                self.add_file(initial_files)

        # Queue Check
        self.after(100, self.check_queue)

    def check_queue(self):
        try:
            while True:
                file_path = file_queue.get_nowait()
                self.add_file(file_path)
                self.attributes("-topmost", True)
                self.attributes("-topmost", False)
        except queue.Empty:
            pass
        self.after(500, self.check_queue)

    def add_file(self, path):
        if path and os.path.exists(path):
            # Check if already added
            for r in self.rows:
                if r.file_path == path:
                    return
            
            row = FileRow(self.scroll_frame, path, self.remove_row)
            row.pack(fill="x", pady=2)
            self.rows.append(row)

    def remove_row(self, row_instance):
        row_instance.pack_forget()
        row_instance.destroy()
        if row_instance in self.rows:
            self.rows.remove(row_instance)

    def browse_files(self):
        filenames = filedialog.askopenfilenames(title="Sélectionner des fichiers")
        for f in filenames:
            self.add_file(f)

    def apply_global_format(self):
        target = self.combo_global.get()
        if target == "...": return
        
        count = 0
        for row in self.rows:
            # Check if target is valid for this row
            if target in row.formats:
                row.combo.set(target)
                count += 1
        
        if count == 0:
            messagebox.showinfo("Info", f"Aucun fichier compatible avec le format {target}")

    def process_all(self):
        if not self.rows:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
            return

        self.btn_convert.configure(state="disabled")
        self.progress.set(0)
        
        # Collect jobs
        jobs = []
        for row in self.rows:
            jobs.append({
                'path': row.file_path,
                'target': row.get_target_ext(),
            })

        threading.Thread(target=self.run_conversion_thread, args=(jobs,), daemon=True).start()

    def run_conversion_thread(self, jobs):
        success_count = 0
        errors = []
        total = len(jobs)

        for i, job in enumerate(jobs):
            input_path = job['path']
            target_ext = job['target']
            
            try:
                # delegate to core_conversion
                convert_file(input_path, target_ext)
                success_count += 1
            except Exception as e:
                errors.append(f"{os.path.basename(input_path)}: {e}")
            
            self.after(0, self.update_progress, (i + 1) / total)

        # Finish
        msg = f"Terminé !\n{success_count}/{total} réussis."
        if errors:
            msg += "\n\nErreurs :\n" + "\n".join(errors)
        
        self.after(0, lambda: messagebox.showinfo("Rapport", msg))
        self.after(0, lambda: self.reset_ui())

    def update_progress(self, val):
        self.progress.set(val)

    def reset_ui(self):
        self.btn_convert.configure(state="normal")
        self.progress.set(0)
