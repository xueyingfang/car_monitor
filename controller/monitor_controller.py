from form.monitor_main_form import MonitorMainForm
from service.car_data_service import CarDataService

class MonitorController:
    def __init__(self, root):
        self.ui_form = MonitorMainForm(root)
        self.data_service = CarDataService()
        self.root = root
        self.interval_ms = 800  # 每隔800毫秒生成一条模拟车辆数据

    def loop_fetch_data(self):
        """定时循环：生成数据 ->业务处理 ->追加到窗体表格"""
        car_dto = self.data_service.generate_mock_car_data()
        handled_dto = self.data_service.filter_and_handle_data(car_dto)
        self.ui_form.append_one_row(handled_dto)
        # 继续下一次定时任务
        self.root.after(self.interval_ms, self.loop_fetch_data)

    def start(self):
        self.loop_fetch_data()
