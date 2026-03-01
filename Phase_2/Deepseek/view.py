import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import plot_diagram

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagramme de Voronoi")
        self.controller = None

        self.menubar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Charger des points")
        self.file_menu.add_command(label="Exporter en SVG")
        self.file_menu.add_command(label="Exporter en image")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=root.quit)
        self.menubar.add_cascade(label="Fichier", menu=self.file_menu)
        root.config(menu=self.menubar)

        self.figure_frame = tk.Frame(root)
        self.figure_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = None
        self.canvas = None

        self.status_label = tk.Label(root, text="Aucun fichier chargé", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def set_controller(self, controller):
        self.controller = controller
        self.file_menu.entryconfig(0, command=controller.on_load_points)
        self.file_menu.entryconfig(1, command=controller.on_export_svg)
        self.file_menu.entryconfig(2, command=controller.on_export_image)

    def update_display(self, model):
        if self.figure:
            self.figure.clear()
        else:
            self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = self.figure.add_subplot(111)
        plot_diagram(ax, model)
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.figure_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def set_status(self, message):
        self.status_label.config(text=message)

    def ask_open_filename(self):
        return filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])

    def ask_save_filename(self, extension, filetypes):
        return filedialog.asksaveasfilename(defaultextension=extension, filetypes=filetypes)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)