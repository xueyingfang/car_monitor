import tkinter as tk
from tkinter import ttk, messagebox
from dto.car_metric_dto import CarMetricDTO
from form.time_select_form import TimeSelectForm


class MonitorMainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("汽车实时指标监控面板")
        self.root.geometry("1100x480")

        # 最大界面可见数据条数，15条，超过自动删掉最旧的
        self.max_show_rows = 15
        self.data_row_ids = []

        # ========== 按钮回调钩子，由controller注入 ==========
        self.export_all_callback = None
        self.export_increment_callback = None
        self.export_by_time_callback = None

        # 定义表格列 横向列表
        self.columns = ("car_id", "time", "speed", "temp", "voltage", "mileage", "status")
        self.table = ttk.Treeview(root, columns=self.columns, show="headings", height=15)

        # 设置每一列标题和宽度
        self.table.heading("car_id", text="车辆编号")
        self.table.column("car_id", width=110, anchor=tk.CENTER)

        self.table.heading("time", text="上报时间")
        self.table.column("time", width=180, anchor=tk.CENTER)

        self.table.heading("speed", text="车速(km/h)")
        self.table.column("speed", width=110, anchor=tk.CENTER)

        self.table.heading("temp", text="电机温度")
        self.table.column("temp", width=110, anchor=tk.CENTER)

        self.table.heading("voltage", text="电池电压")
        self.table.column("voltage", width=110, anchor=tk.CENTER)

        self.table.heading("mileage", text="总里程")
        self.table.column("mileage", width=110, anchor=tk.CENTER)

        self.table.heading("status", text="状态")
        self.table.column("status", width=90, anchor=tk.CENTER)

        # 垂直滚动条
        scroll_bar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_bar.set)

        # -------- 按钮容器【3个按钮】 --------
        btn_frame = ttk.Frame(root)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=8, pady=4)

        self.btn_export_all = ttk.Button(
            btn_frame,
            text="导出全部异常Excel",
            command=self._on_export_all_click
        )
        self.btn_export_all.pack(side=tk.LEFT, padx=(0,5))

        self.btn_export_inc = ttk.Button(
            btn_frame,
            text="增量导出(上次导出后新增)",
            command=self._on_export_inc_click
        )
        self.btn_export_inc.pack(side=tk.LEFT, padx=(0,5))

        self.btn_export_time = ttk.Button(
            btn_frame,
            text="按时间范围导出",
            command=self._on_export_time_click
        )
        self.btn_export_time.pack(side=tk.LEFT)

        # 表格+滚动条布局
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_export_all_click(self):
        """导出全部"""
        if self.export_all_callback is None:
            messagebox.showwarning("提示", "导出功能未初始化")
            return
        success = self.export_all_callback()
        if success:
            messagebox.showinfo("完成", "全部异常数据已导出为 abnormal_export.xlsx")
        else:
            messagebox.showerror("失败", "导出失败，暂无异常数据或发生错误")

    def _on_export_inc_click(self):
        """增量导出"""
        if self.export_increment_callback is None:
            messagebox.showwarning("提示", "导出功能未初始化")
            return
        success = self.export_increment_callback()
        if success:
            messagebox.showinfo("完成", "增量数据已导出为 abnormal_increment.xlsx")
        else:
            messagebox.showinfo("提示", "上次导出后没有新异常数据，无需导出")

    def _on_export_time_click(self):
        """打开时间选择弹窗，选完把datetime对象传给controller回调"""
        if self.export_by_time_callback is None:
            messagebox.showwarning("提示", "导出功能未初始化")
            return
        select_win = TimeSelectForm(self.root)
        start_dt, end_dt = select_win.get_selected()
        if start_dt is None or end_dt is None:
            return
        success = self.export_by_time_callback(start_dt, end_dt)
        if success:
            messagebox.showinfo("完成", "所选时间范围数据已导出为 abnormal_timerange.xlsx")
        else:
            messagebox.showinfo("提示", "该时间范围无异常数据")

    def append_one_row(self, dto: CarMetricDTO):
        row_values = dto.to_table_row()
        insert_id = self.table.insert("", tk.END, values=row_values)
        self.data_row_ids.append(insert_id)

        if len(self.data_row_ids) > self.max_show_rows:
            old_id = self.data_row_ids.pop(0)
            self.table.delete(old_id)
        self.table.yview_moveto(1.0)
