!/usr/bin/env python3
import tkinter as tk
from tkinter import font, filedialog, messagebox
import re
import json  # Changed from pickle to json for security

class MagicNotepadLinux:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic Notepad")
        self.root.geometry("800x600")
        self.root.configure(bg="#2d2d2d") # Dark mode for Kali feel!

        # --- 1. MINIMAL TOOLBAR (Dark Theme) ---
        self.toolbar = tk.Frame(root, bg="#2d2d2d", height=40)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        def create_text_btn(text, command):
            lbl = tk.Label(self.toolbar, text=text, bg="#2d2d2d", fg="#ffffff", 
                           font=("Segoe UI", 10), padx=10, pady=10, cursor="hand2")
            lbl.pack(side=tk.LEFT)
            # Hover effects
            lbl.bind("<Button-1>", lambda e: command())
            lbl.bind("<Enter>", lambda e: lbl.config(fg="#00b0ff")) # Kali Blue
            lbl.bind("<Leave>", lambda e: lbl.config(fg="#ffffff"))
            return lbl

        create_text_btn("New", self.new_file)
        create_text_btn("Open", self.open_file)
        create_text_btn("Save", self.save_file)

        tk.Label(self.toolbar, text="Tip: **bold** or blue::text::", 
                 bg="#2d2d2d", fg="#808080", padx=10).pack(side=tk.RIGHT)

        tk.Frame(root, height=1, bg="#404040").pack(fill=tk.X)

        # --- 2. TEXT AREA ---
        # Dark mode colors
        self.text_area = tk.Text(root, font=("Consolas", 12), undo=True, wrap="word", 
                                 bd=0, padx=10, pady=10, 
                                 bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # --- 3. STYLES SETUP ---
        self.bold_font = font.Font(family="Consolas", size=12, weight="bold")
        self.italic_font = font.Font(family="Consolas", size=12, slant="italic")
        
        self.text_area.tag_configure("bold_style", font=self.bold_font)
        self.text_area.tag_configure("italic_style", font=self.italic_font)

        self.text_area.bind("<KeyRelease>", self.check_formatting)

        # --- MAGIC LOGIC ---
        self.dynamic_tag_limit = 100  # Limit the number of dynamic tags

    def check_formatting(self, event=None):
        # Only trigger on relevant keys
        if event and event.keysym not in ("space", "Return") and event.char not in (":", " "):
            return
        self.process_text_logic()

    def process_text_logic(self):
        current_index = self.text_area.index(tk.INSERT)
        line_num = current_index.split('.')[0]

        while True:
            line_text = self.text_area.get(f"{line_num}.0", f"{line_num}.end")

            # BOLD
            bold_match = re.search(r"\*\*(.+?)\*\*", line_text)
            if bold_match:
                self.apply_style(bold_match, "bold_style", line_num)
                continue

            # ITALIC
            italic_match = re.search(r"//(.+?)//", line_text)
            if italic_match:
                self.apply_style(italic_match, "italic_style", line_num)
                continue

            # COLOR
            color_match = re.search(r"(\w+)::(.+?)::", line_text)
            if color_match:
                color_name = color_match.group(1).lower()
                try:
                    self.root.winfo_rgb(color_name)  # Validate color
                    if len(self.text_area.tag_names()) > self.dynamic_tag_limit:
                        messagebox.showwarning("Tag Limit Reached", "Too many dynamic tags. Clear some text.")
                        break
                    tag_name = f"dynamic_color_{color_name}"
                    self.text_area.tag_configure(tag_name, foreground=color_name)
                    self.apply_color_style(color_match, tag_name, line_num)
                except tk.TclError:
                    messagebox.showerror("Invalid Color", f"'{color_name}' is not a valid color.")
                continue
            break

    def apply_style(self, match, tag_name, line_num):
        self._replace_text(match, tag_name, line_num, match.group(1))

    def apply_color_style(self, match, tag_name, line_num):
        self._replace_text(match, tag_name, line_num, match.group(2))

    def _replace_text(self, match, tag_name, line_num, inner_text):
        start_char = match.start()
        end_char = match.end()
        start_index = f"{line_num}.{start_char}"
        end_index = f"{line_num}.{end_char}"

        # Save cursor position
        cursor_index = self.text_area.index(tk.INSERT)

        self.text_area.delete(start_index, end_index)
        self.text_area.insert(start_index, inner_text)

        new_end_index = f"{line_num}.{start_char + len(inner_text)}"
        self.text_area.tag_add(tag_name, start_index, new_end_index)

        # Restore cursor position
        self.text_area.mark_set(tk.INSERT, cursor_index)

    # --- SECURE FILE OPERATIONS (JSON) ---
    def new_file(self):
        if self.text_area.get("1.0", tk.END).strip():
            confirm = messagebox.askyesno("New File", "Clear current text?")
            if not confirm: return
        self.text_area.delete("1.0", tk.END)
        self.root.title("Magic Notepad")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".ntp", filetypes=[("Magic Files", "*.ntp")])
        if not filepath: return

        text_content = self.text_area.get("1.0", tk.END)
        tags_data = {}
        
        # Collect tags
        for tag in self.text_area.tag_names():
            if tag in ["bold_style", "italic_style"] or tag.startswith("dynamic_color_"):
                ranges = self.text_area.tag_ranges(tag)
                if ranges:
                    # Convert Tkinter tuples to strings for JSON compatibility
                    tags_data[tag] = [str(r) for r in ranges]

        data = {"text": text_content, "tags": tags_data}
        
        try:
            # SECURE: Using JSON instead of Pickle
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.root.title(f"Magic Notepad - {filepath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Magic Files", "*.ntp")])
        if not filepath: return

        try:
            # SECURE: Using JSON instead of Pickle
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", data["text"])
            
            saved_tags = data.get("tags", {})
            for tag_name, ranges in saved_tags.items():
                if tag_name.startswith("dynamic_color_"):
                    color = tag_name.replace("dynamic_color_", "")
                    self.text_area.tag_configure(tag_name, foreground=color)
                
                # Apply tags
                for i in range(0, len(ranges), 2):
                    self.text_area.tag_add(tag_name, ranges[i], ranges[i+1])
            self.root.title(f"Magic Notepad - {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"File error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MagicNotepadLinux(root)
    root.mainloop()
