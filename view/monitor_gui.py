import tkinter as tk
from tkinter import ttk


class MonitorGuiView:
    """GUI视图层，只负责渲染窗体，不写业务逻辑；对外提供获取界面文本的接口"""
    def __init__(self, root):
        self.root = root
        self.root.title("汽车实时指标监控窗体")
        self.root.geometry("540x440")

        self.ui_labels = dict()
        self.status_label = None
        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        items = [
            ("车辆编号", "car_id"),
            ("采集时间", "timestamp"),
            ("车速(km/h)", "car_speed"),
            ("电池电压(V)", "battery_voltage"),
            ("电机温度(℃)", "motor_temp"),
            ("总里程(km)", "mileage"),
            ("故障码", "fault_code")
        ]
        for row, (show_name, key) in enumerate(items):
            ttk.Label(main_frame, text=f"{show_name}：").grid(row=row, column=0, sticky="w", pady=4)
            lbl = ttk.Label(main_frame, text="--")
            lbl.grid(row=row, column=1, sticky="w", padx=10, pady=4)
            self.ui_labels[key] = lbl

        self.status_label = ttk.Label(main_frame, text="等待启动...", foreground="green")
        self.status_label.grid(row=len(items)+3, column=0, columnspan=2, pady=15)

    def set_display_data(self, dto):
        """把CarDataDTO数据渲染到窗体"""
        self.ui_labels["car_id"].config(text=dto.car_id)
        self.ui_labels["timestamp"].config(text=dto.timestamp)
        self.ui_labels["car_speed"].config(text=str(dto.car_speed))
        self.ui_labels["battery_voltage"].config(text=str(dto.battery_voltage))
        self.ui_labels["motor_temp"].config(text=str(dto.motor_temp))
        self.ui_labels["mileage"].config(text=str(dto.mileage))
        self.ui_labels["fault_code"].config(text=dto.fault_code)

    def get_ui_text_dict(self) -> dict:
        """读取窗体上显示的全部文本，返回字典，交给controller解析"""
        return {
            "car_id": self.ui_labels["car_id"]["text"],
            "timestamp": self.ui_labels["timestamp"]["text"],
            "car_speed": self.ui_labels["car_speed"]["text"],
            "battery_voltage": self.ui_labels["battery_voltage"]["text"],
            "motor_temp": self.ui_labels["motor_temp"]["text"],
            "mileage": self.ui_labels["mileage"]["text"],
            "fault_code": self.ui_labels["fault_code"]["text"],
        }

    def set_status(self, text: str, color: str):
        """设置底部状态文字"""
        self.status_label.config(text=text, foreground=color)
