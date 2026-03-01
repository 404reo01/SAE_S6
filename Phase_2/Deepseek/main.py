import tkinter as tk
from model import VoronoiModel
from view import MainView
from controller import VoronoiController

def main():
    root = tk.Tk()
    model = VoronoiModel()
    view = MainView(root)
    controller = VoronoiController(model, view)
    view.set_controller(controller)
    root.mainloop()

if __name__ == "__main__":
    main()