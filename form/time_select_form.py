import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TimeSelectForm:
    """纯原生tk 时间选择弹窗，不依赖任何第三方UI库"""
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("选择导出时间范围")
        self.win.geometry("420x260")
        self.win.transient(parent)
        self.win.grab_set()

        self.result_start: datetime | None = None
        self.result_end: datetime | None = None

        now = datetime.now()

        # 开始时间行
        ttk.Label(self.win, text="开始时间").grid(row=0, column=0, columnspan=6, padx=10, pady=(12,4), sticky="w")
        self.sy = ttk.Entry(self.win, width=6); self.sy.grid(row=1,column=0,padx=3)
        ttk.Label(self.win, text="-").grid(row=1,column=1)
        self.sm = ttk.Entry(self.win, width=4); self.sm.grid(row=1,column=2,padx=3)
        ttk.Label(self.win, text="-").grid(row=1,column=3)
        self.sd = ttk.Entry(self.win, width=4); self.sd.grid(row=1,column=4,padx=3)

        ttk.Label(self.win, text="  ").grid(row=1,column=5)
        self.sh = ttk.Entry(self.win, width=4); self.sh.grid(row=1,column=6,padx=3)
        ttk.Label(self.win, text=":").grid(row=1,column=7)
        self.smi = ttk.Entry(self.win, width=4); self.smi.grid(row=1,column=8,padx=3)
        ttk.Label(self.win, text=":").grid(row=1,column=9)
        self.ss = ttk.Entry(self.win, width=4); self.ss.grid(row=1,column=10,padx=3)

        # 结束时间行
        ttk.Label(self.win, text="结束时间").grid(row=2, column=0, columnspan=6, padx=10, pady=(12,4), sticky="w")
        self.ey = ttk.Entry(self.win, width=6); self.ey.grid(row=3,column=0,padx=3)
        ttk.Label(self.win, text="-").grid(row=3,column=1)
        self.em = ttk.Entry(self.win, width=4); self.em.grid(row=3,column=2,padx=3)
        ttk.Label(self.win, text="-").grid(row=3,column=3)
        self.ed = ttk.Entry(self.win, width=4); self.ed.grid(row=3,column=4,padx=3)

        ttk.Label(self.win, text="  ").grid(row=3,column=5)
        self.eh = ttk.Entry(self.win, width=4); self.eh.grid(row=3,column=6,padx=3)
        ttk.Label(self.win, text=":").grid(row=3,column=7)
        self.emi = ttk.Entry(self.win, width=4); self.emi.grid(row=3,column=8,padx=3)
        ttk.Label(self.win, text=":").grid(row=3,column=9)
        self.es = ttk.Entry(self.win, width=4); self.es.grid(row=3,column=10,padx=3)

        # 默认赋值：今天 00:00:00 ~ 当前时刻
        self.sy.insert(0, str(now.year))
        self.sm.insert(0, str(now.month))
        self.sd.insert(0, str(now.day))
        self.sh.insert(0, "00")
        self.smi.insert(0, "00")
        self.ss.insert(0, "00")

        self.ey.insert(0, str(now.year))
        self.em.insert(0, str(now.month))
        self.ed.insert(0, str(now.day))
        self.eh.insert(0, str(now.hour))
        self.emi.insert(0, str(now.minute))
        self.es.insert(0, str(now.second))

        # 按钮
        btn_frame = ttk.Frame(self.win)
        btn_frame.grid(row=4, column=0, columnspan=12, pady=20)
        ttk.Button(btn_frame, text="确定", command=self._ok).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="取消", command=self._cancel).pack(side="left", padx=8)

    def _ok(self):
        try:
            start_str = f"{self.sy.get()}-{self.sm.get()}-{self.sd.get()} {self.sh.get()}:{self.smi.get()}:{self.ss.get()}"
            end_str = f"{self.ey.get()}-{self.em.get()}-{self.ed.get()} {self.eh.get()}:{self.emi.get()}:{self.es.get()}"
            self.result_start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            self.result_end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("输入错误", "时间格式不正确，请检查年月日时分秒数字")
            return
        self.win.destroy()

    def _cancel(self):
        self.result_start = None
        self.result_end = None
        self.win.destroy()

    def get_selected(self) -> tuple[datetime|None, datetime|None]:
        """外部调用，阻塞等待弹窗关闭，返回 (start,end)，取消返回(None,None)"""
        self.parent.wait_window(self.win)
        return self.result_start, self.result_end
