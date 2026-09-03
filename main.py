import tkinter as tk
from controller.monitor_controller import MonitorController

if __name__ == "__main__":
    main_root = tk.Tk()
    app = MonitorController(main_root)
    app.start()
    main_root.mainloop()
