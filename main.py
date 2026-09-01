import tkinter as tk
from controller.monitor_controller import MonitorController

if __name__ == "__main__":
    window = tk.Tk()
    controller = MonitorController(window)
    controller.loop_refresh()
    window.mainloop()
