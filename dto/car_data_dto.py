from dataclasses import dataclass
from datetime import datetime

@dataclass
class CarDataDTO:
    """车辆实时指标 DTO，对应窗体展示的数据"""
    car_id: str
    timestamp: str
    car_speed: float
    battery_voltage: float
    motor_temp: float
    mileage: float
    fault_code: str

    @staticmethod
    def now_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
