from view.monitor_gui import MonitorGuiView
from service.car_data_service import CarDataService



class MonitorController:
    """控制器：串联view、各个service；主业务调度，相当于Java Controller"""
    def __init__(self, root):
        self.view = MonitorGuiView(root)
        self.car_data_service = CarDataService()
        self.root = root

    def loop_refresh(self):
        # 1.模拟获取车辆数据
        car_dto = self.car_data_service.mock_fetch_car_data()
        # 2.更新GUI窗体
        self.view.set_display_data(car_dto)
        # 3.【模拟从窗体取数】读取窗体UI文本，解析DTO
        ui_text = self.view.get_ui_text_dict()
        read_dto = self.car_data_service.parse_from_ui_text(ui_text)

