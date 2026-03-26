#pNotes
#Copyright (C) 2026 TheProjectDark
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

import tkinter as tk
from tkinter import filedialog, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("pNotes")
        self.geometry("800x600")
        self.current_path = None

        self._build_menu()
        self._build_ui()

        self.mainloop()

    #UI
    def _build_menu(self):
        menubar = tk.Menu(self)
        menu_help = tk.Menu(menubar, tearoff=0)
        menu_help.add_command(label="About", command=self.on_about)
        menubar.add_cascade(label="Help", menu=menu_help)
        self.config(menu=menubar)

    def _build_ui(self):
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(top_frame, text="Save as", command=self.on_save_as).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(top_frame, text="Save", command=self.on_save).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(top_frame, text="Open", command=self.on_open).pack(side=tk.LEFT, padx=5, pady=5)

        self.field = tk.Text(self, wrap=tk.NONE, undo=True)
        self.field.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.field.bind("<Tab>", self.on_tab)

    #Functions/Logic
    def on_tab(self, event):
        try:
            sel_start = self.field.index(tk.SEL_FIRST)
            sel_end   = self.field.index(tk.SEL_LAST)
            self.field.delete(sel_start, sel_end)
            self.field.insert(sel_start, "    ")
        except tk.TclError:
            self.field.insert(tk.INSERT, "    ")
        return "break"

    def on_save_as(self):
        path = filedialog.asksaveasfilename(
            title="Save file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.field.get("1.0", tk.END))
            self.current_path = path  # запоминаем путь
            messagebox.showinfo("Saving", "File saved successfully")
        except IOError:
            messagebox.showerror("Error", f"Could not save file: {path}")

    def on_save(self):
        if self.current_path:
            try:
                with open(f"{self.current_path}", "w", encoding="utf-8") as f:
                    f.write(self.field.get("1.0", tk.END))
            except IOError:
                messagebox.showerror("Error", f"Could not save file: {self.current_path}")
        else:
            self.on_save_as()

    def on_open(self):
        path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.field.delete("1.0", tk.END)
                self.field.insert("1.0", f.read())
                self.current_path = path
        except IOError:
            messagebox.showerror("Error", f"Could not open file: {path}")

    def on_about(self):
        messagebox.showinfo("About", "pNotes\nTkinter")


App()