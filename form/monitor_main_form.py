import tkinter as tk
from tkinter import ttk
from dto.car_metric_dto import CarMetricDTO

class MonitorMainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("汽车实时指标监控面板")
        self.root.geometry("1100x420")

        # 最大界面可见数据条数，15条，超过自动删掉最旧的
        self.max_show_rows = 15
        self.data_row_ids = []

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

        # 布局
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    def append_one_row(self, dto: CarMetricDTO):
        """新增一行数据到表格底部；控制最多15行，自动向上滚动"""
        row_values = dto.to_table_row()
        insert_id = self.table.insert("", tk.END, values=row_values)
        self.data_row_ids.append(insert_id)

        # 超过最大行数，删除最顶部旧数据，实现向上滚动效果
        if len(self.data_row_ids) > self.max_show_rows:
            old_id = self.data_row_ids.pop(0)
            self.table.delete(old_id)

        # 自动滚动到最底部，看到最新数据
        self.table.yview_moveto(1.0)
