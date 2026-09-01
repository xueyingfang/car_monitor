import random
from dto.car_data_dto import CarDataDTO


class CarDataService:
    """车辆数据服务：模拟采集车辆上传指标；支持从窗体UI文本解析成DTO"""
    def __init__(self):
        self.mileage_acc = 0.0
        self.car_id = "CAR_2026_001"

    def mock_fetch_car_data(self) -> CarDataDTO:
        """模拟从车辆设备获取实时数据，随机制造异常测试"""
        self.mileage_acc += round(random.uniform(0.1, 0.8), 2)

        speed = round(random.uniform(0, 130), 1)
        voltage = round(random.uniform(300, 440), 1)
        temp = round(random.uniform(20, 95), 1)

        fault_code = ""
        if random.random() < 0.12:
            fault_code = f"ERR{random.randint(1001,1010)}"

        dto = CarDataDTO(
            car_id=self.car_id,
            timestamp=CarDataDTO.now_time(),
            car_speed=speed,
            battery_voltage=voltage,
            motor_temp=temp,
            mileage=round(self.mileage_acc, 2),
            fault_code=fault_code
        )
        return dto

    @staticmethod
    def parse_from_ui_text(ui_text_dict: dict) -> CarDataDTO:
        """
        从窗体UI读取的文本字典，解析为DTO
        ui_text_dict: {car_id:"", timestamp:"", car_speed:"",...}
        """
        return CarDataDTO(
            car_id=ui_text_dict["car_id"],
            timestamp=ui_text_dict["timestamp"],
            car_speed=float(ui_text_dict["car_speed"]),
            battery_voltage=float(ui_text_dict["battery_voltage"]),
            motor_temp=float(ui_text_dict["motor_temp"]),
            mileage=float(ui_text_dict["mileage"]),
            fault_code=ui_text_dict["fault_code"]
        )
